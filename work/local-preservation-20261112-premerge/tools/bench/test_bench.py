"""All tests create disposable roots; no test writes or scans the real repository."""
import concurrent.futures
import datetime as dt
import hashlib
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from tools.bench import bench as b


def fixture(root, newline='\n'):
    files = {
        b.PROJECTS: json.dumps({'version': 1, 'projects': [
            dict(id='csb', title='Cable span bracket', prefixes=['CSB'], status='printing', notes='', updated='2020-01-01', device_cards=['docs/devices/post.md'], sources=['work/span.scad'], workflow_log='Cable bracket'),
            dict(id='cm', title='Modem', prefixes=['CM1P', 'CM6'], status='draft', notes='', updated='2026-11-06', device_cards=[], sources=[], workflow_log=''),
            dict(id='scr', title='Screen', prefixes=['SCR5'], status='draft', notes='', updated='2026-11-06', device_cards=[], sources=[], workflow_log='')]}),
        b.FIT: '# Fit log\n\n- 2026-11-01 CSB-A: fits, but rails a tad short. Strength UNKNOWN.\n- 2026-11-02 CM1P-T10: Too tight.\n',
        b.WORKFLOW: '# Workflow\n\n## Cable bracket\n\n| Date | Step | What happened | Friction | App idea |\n| --- | --- | --- | --- | --- |\n| 2026-11-01 | Print | Started | | |\n\n## Another project\n\nKeep this section exactly.\n',
        'HANDOFF.md': '# Current\nCSB-B printing. CM6A too tight. CM1P-T1 unprinted. SCR5-H and SCR5-H10.\nCM1P-T10 dropped, do not print.\n',
        'docs/devices/post.md': '# Post\n\n| Value | Status |\n| --- | --- |\n| Depth | UNKNOWN |\n| Width | Measured |\n\n<script>alert(1)</script>\n',
        'outputs/Bracket_CSB-A_2026-11-01/README.md': '# CSB-A\nStrength UNKNOWN\n',
        'outputs/Bracket_CSB-A_2026-11-01/release_report.md': '# Release CSB-A\nNo fails\n',
        'outputs/Bracket_CSB-B_2026-11-02/README.md': '# CSB-B\nDriver clearance UNKNOWN\n',
        'outputs/Final_3MF/README.md': '| File | Bracket | Source folder |\n| --- | --- | --- |\n| CSB-A_set.3mf | superseded by CSB-B | Bracket_CSB-A_2026-11-01 |\n',
        'outputs/Final_3MF/CSB-A_set.3mf': 'not a mesh; filenames only',
        'work/mesh-viewer/CSB-A.html': '<!doctype html><title>CSB-A fixture</title><p>Viewer</p>',
        'work/span.scad': 'never execute this',
        'data/untouched.txt': 'user data',
        'lib/untouched.txt': 'library data',
    }
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.replace('\n', newline).encode('utf-8'))


def tree_hashes(root):
    return {p.relative_to(root).as_posix(): b.digest(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='bench-test-')
        self.root = Path(self.temp.name)
        fixture(self.root)
        self.app = b.Bench(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def body(self, **kw):
        return {'hashes': self.app.hashes(), **kw}

    def report_body(self, **kw):
        return self.body(revision='CSB-A', result='Fits', where='Rails', walls='2', infill='10', notes='No sag', **kw)

    def assert_problem(self, call, code=400):
        before = tree_hashes(self.root)
        with self.assertRaises(b.Problem) as cm:
            call()
        self.assertEqual(cm.exception.status, code)
        self.assertEqual(before, tree_hashes(self.root))


class DiscoveryTests(Base):
    def test_cache_reused_until_refresh(self):
        first = self.app.snapshot()
        (self.root/'HANDOFF.md').write_text('CSB-C', encoding='utf-8')
        self.assertIs(first, self.app.snapshot())
        self.assertIn('CSB-C', [r['id'] for r in self.app.refresh()['projects'][0]['revisions']])

    def test_revisions_deduplicate_sources(self):
        p = self.app.snapshot()['projects'][0]
        self.assertEqual([r['id'] for r in p['revisions']], ['CSB-B','CSB-A'])
        self.assertEqual(len(p['revisions'][1]['three_mf']),1)

    def test_newest_readme_unknowns(self):
        p = self.app.snapshot()['projects'][0]
        self.assertTrue(any('Driver clearance' in u['text'] for u in p['unknowns']))
        self.assertFalse(any(u['text'] == 'Strength UNKNOWN' for u in p['unknowns']))

    def test_device_unknown_rows_visible(self):
        p = self.app.snapshot()['projects'][0]
        self.assertTrue(any('Depth' in u['text'] for u in p['unknowns']))
        self.assertFalse(any('Width' in u['text'] for u in p['unknowns']))

    def test_attention_printing_and_release(self):
        text = str(self.app.snapshot()['attention'])
        self.assertIn('printing for more than 3 days',text)
        self.assertIn('CSB-B: released',text)
        self.assertNotIn('CSB-A: released',text)

    def test_attention_report_due(self):
        self.app.update('csb',self.body(status='report-due'))
        self.assertIn('report due',str(self.app.snapshot()['attention']))

    def test_attention_draft_unknowns(self):
        self.app.update('csb',self.body(status='draft'))
        self.assertIn('dependencies need review',str(self.app.snapshot()['attention']))

    def test_fit_matching_whole_id(self):
        p = self.app.snapshot()['projects'][1]
        revisions = {r['id']:r for r in p['revisions']}
        self.assertEqual(revisions['CM1P-T1']['fit_lines'],[])
        self.assertEqual(revisions['CM1P-T10']['status'],'problem')

    def test_replacement_mention_not_positive_fit(self):
        path=self.root/b.FIT
        path.write_text('- CSB-A fits. CSB-B is the next unprinted revision.\n',encoding='utf-8')
        r=self.app.snapshot()['projects'][0]['revisions'][0]
        self.assertEqual(r['id'],'CSB-B')
        self.assertEqual(r['status'],'not printed')
        self.assertEqual(len(r['fit_lines']),1)

    def test_supersession_evidence(self):
        p=self.app.snapshot()['projects'][0]
        self.assertIn('superseded',str(p['revisions'][1]['warnings']))

    def test_workflow_excludes_other_project(self):
        p=self.app.snapshot()['projects'][0]
        self.assertIn('Started',p['workflow_html'])
        self.assertNotIn('Keep this section',p['workflow_html'])

    def test_missing_card_is_plain(self):
        (self.root/'docs/devices/post.md').unlink()
        self.assertTrue(self.app.snapshot()['projects'][0]['cards'][0]['missing'])

    def test_bad_seed_rejected(self):
        (self.root/b.PROJECTS).write_text('{bad',encoding='utf-8')
        self.assert_problem(self.app.snapshot,500)

    def test_seed_duplicate_prefix_rejected(self):
        d=self.app.data();d['projects'][1]['prefixes'].append('CSB')
        (self.root/b.PROJECTS).write_bytes(b.json_bytes(d))
        self.assert_problem(self.app.snapshot,500)

    def test_refresh_never_writes(self):
        before=tree_hashes(self.root);self.app.refresh();self.app.refresh()
        self.assertEqual(before,tree_hashes(self.root))

    def test_walk_ignores_app_and_frozen_sources(self):
        for name in ['outputs/Mechanical_Design_App/CSB-Z/README.md','outputs/X/src/README.md']:
            p=self.root/name;p.parent.mkdir(parents=True);p.write_text('CSB-Z',encoding='utf-8')
        self.assertNotIn('CSB-Z',str(self.app.snapshot()['projects'][0]['revisions']))

    def test_date_from_folder_beats_viewer_mtime(self):
        r=self.app.snapshot()['projects'][0]['revisions'][1]
        self.assertEqual(r['date'],'2026-11-01')
        self.assertEqual(r['date_source'],'folder name')


class WriteTests(Base):
    def test_status_backup_only_expected_files(self):
        before=tree_hashes(self.root);old=(self.root/b.PROJECTS).read_bytes()
        self.app.update('csb',self.body(status='done'))
        after=tree_hashes(self.root)
        self.assertEqual({k for k in after if before.get(k)!=after[k]}, {b.PROJECTS,b.PROJECTS+'.bak'})
        self.assertEqual((self.root/(b.PROJECTS+'.bak')).read_bytes(),old)
        self.assertEqual(self.app.data()['projects'][0]['status'],'done')
        self.assertFalse(list(self.root.rglob('*.tmp')))

    def test_notes_unicode(self):
        self.app.update('csb',self.body(notes='Café — 日本\nsecond line'))
        self.assertEqual(self.app.data()['projects'][0]['notes'],'Café — 日本\nsecond line')

    def test_new_project_success(self):
        old=(self.root/b.PROJECTS).read_bytes()
        result=self.app.create(self.body(title='New bracket',prefixes=['NEW'],device_cards=['docs/devices/post.md'],sources=['work/span.scad']))
        self.assertEqual(result['id'],'new-bracket');self.assertEqual(result['status'],'idea')
        self.assertEqual((self.root/(b.PROJECTS+'.bak')).read_bytes(),old)

    def test_report_exact_append_and_backup(self):
        before={n:(self.root/n).read_bytes() for n in b.WRITABLE}
        result=self.app.report(self.report_body())
        expected=f'- {dt.date.today()} CSB-A (Brian, via Workshop Bench): Fits. Rails. 2 walls, 10% infill. No sag. Strength UNKNOWN.'
        self.assertEqual(result['text'],expected)
        self.assertEqual((self.root/b.FIT).read_bytes(),before[b.FIT]+expected.encode()+b'\n')
        for n in b.WRITABLE:
            self.assertEqual((self.root/(n+'.bak')).read_bytes(),before[n])
        self.assertTrue((self.root/b.WORKFLOW).read_bytes().startswith(before[b.WORKFLOW]))
        self.assertEqual(self.app.data()['projects'][0]['status'],'draft')
        self.assertFalse(list(self.root.rglob('*.tmp')))

    def test_report_crlf(self):
        fixture(self.root,'\r\n');self.app=b.Bench(self.root)
        old=(self.root/b.FIT).read_bytes();self.app.report(self.report_body())
        new=(self.root/b.FIT).read_bytes()
        self.assertTrue(new.startswith(old));self.assertNotIn(b'\n',new.replace(b'\r\n',b''))
        workflow=(self.root/b.WORKFLOW).read_bytes();self.assertNotIn(b'\n',workflow.replace(b'\r\n',b''))

    def test_missing_final_newline_preserves_bytes(self):
        p=self.root/b.FIT;p.write_bytes(b'old text')
        self.app.report(self.report_body())
        self.assertTrue(p.read_bytes().startswith(b'old text\n- '))

    def test_workflow_continuation_visible(self):
        self.app.report(self.report_body())
        p=self.app.snapshot()['projects'][0]
        self.assertIn('Started',p['workflow_html']);self.assertIn('Report',p['workflow_html'])
        self.assertNotIn('Keep this section',p['workflow_html'])

    def test_no_workflow_section_no_workflow_write(self):
        before=(self.root/b.WORKFLOW).read_bytes()
        body=self.report_body();body['revision']='CM1P-T1'
        self.app.report(body)
        self.assertEqual((self.root/b.WORKFLOW).read_bytes(),before)
        self.assertFalse((self.root/(b.WORKFLOW+'.bak')).exists())

    def test_report_changed_only_allowlist(self):
        before=tree_hashes(self.root);self.app.report(self.report_body());after=tree_hashes(self.root)
        self.assertEqual({k for k in after if before.get(k)!=after[k]},set(b.WRITABLE)|{n+'.bak' for n in b.WRITABLE})

    def test_preview_writes_nothing(self):
        before=tree_hashes(self.root);self.app.fit_preview(self.report_body())
        self.assertEqual(before,tree_hashes(self.root))

    def test_blank_process_fields_unknown(self):
        body=self.report_body();body.update(walls='',infill='',notes='',where='')
        self.assertIn('UNKNOWN walls, UNKNOWN infill. Strength UNKNOWN.',self.app.fit_preview(body)['text'])

    def test_report_escape_markdown(self):
        body=self.report_body();body['where']='<script>| [x](javascript:evil)'
        text=self.app.fit_preview(body)['text']
        self.assertNotIn('<script>',text);self.assertNotIn('|',text);self.assertNotIn('[x]',text)

    def test_status_stale(self):
        body=self.body(status='done');(self.root/b.PROJECTS).write_bytes((self.root/b.PROJECTS).read_bytes()+b' ')
        self.assert_problem(lambda:self.app.update('csb',body),409)

    def test_create_stale(self):
        body=self.body(title='New',prefixes=['NEW']);body['hashes'][b.PROJECTS]='old'
        self.assert_problem(lambda:self.app.create(body),409)

    def test_fit_stale_each_file_preflight(self):
        for name in b.WRITABLE:
            body=self.report_body();body['hashes'][name]='old'
            self.assert_problem(lambda:self.app.report(body),409)

    def test_missing_hashes(self):
        self.assert_problem(lambda:self.app.update('csb',{'status':'done'}),409)

    def test_concurrent_save_one_wins(self):
        body=self.body(status='done')
        def attempt():
            try:self.app.update('csb',body);return 200
            except b.Problem as e:return e.status
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda _:attempt(),range(2)))
        self.assertEqual(sorted(results),[200,409])

    def test_atomic_replace_failure_rolls_back(self):
        before={n:(self.root/n).read_bytes() for n in b.WRITABLE}
        original=os.replace;count=0
        def fail_once(src,dst):
            nonlocal count
            count+=1
            if count==5:raise OSError('injected disk failure')
            return original(src,dst)
        with patch.object(b.os,'replace',side_effect=fail_once):
            with self.assertRaises(b.Problem):self.app.report(self.report_body())
        for n in b.WRITABLE:self.assertEqual((self.root/n).read_bytes(),before[n])
        self.assertFalse(list(self.root.rglob('*.tmp')))

    def test_failed_staging_leaves_originals(self):
        before=tree_hashes(self.root)
        with patch.object(b.tempfile,'mkstemp',side_effect=OSError('full')):
            with self.assertRaises(b.Problem):self.app.update('csb',self.body(status='done'))
        self.assertEqual(before,tree_hashes(self.root))

    def test_disallowed_write_target(self):
        self.assert_problem(lambda:self.app.replace({'data/untouched.txt':b'oops'},self.app.hashes()),403)

    def test_hardlink_target_refused(self):
        p=self.root/'work/linked.json';os.link(self.root/b.PROJECTS,p)
        self.assert_problem(lambda:self.app.update('csb',self.body(status='done')),409)


class MarkdownTests(Base):
    def test_headings_lists_tables_code(self):
        rendered=b.markdown('# Title\n- One\n- Two\n\n| A | B |\n| --- | --- |\n| `x` | y |')
        for expected in ['<h2>Title</h2>','<li>One</li>','<table>','<th>A</th>','<code>x</code>']:
            self.assertIn(expected,rendered)

    def test_script_escaped(self):
        rendered=b.markdown('<script>alert(1)</script>')
        self.assertNotIn('<script>',rendered);self.assertIn('&lt;script&gt;',rendered)

    def test_onerror_escaped(self):
        self.assertNotIn('<img',b.markdown('<img src=x onerror=alert(1)>'))

    def test_javascript_link_inert(self):
        self.assertNotIn('href=',b.markdown('[open](javascript:alert)'))

    def test_data_link_inert(self):
        self.assertNotIn('href=',b.markdown('[open](data:text/html,hello)'))

    def test_https_link_safe(self):
        self.assertIn('rel="noopener noreferrer"',b.markdown('[source](https://example.com/a)'))

    def test_unapproved_local_link_inert(self):
        self.app.snapshot();self.assertNotIn('href=',self.app.render('[secret](../secrets.txt)',b.FIT))

    def test_approved_local_link(self):
        self.app.snapshot();self.assertIn('/text?path=',self.app.render('[fit](Fit_Findings.md)',b.FIT))

    def test_workflow_continuation_merge(self):
        text='## A\nfirst\n## B\nsecret\n## A (continued)\nlast'
        result=b.workflow_section(text,'A');self.assertIn('first',result);self.assertIn('last',result);self.assertNotIn('secret',result)


class HttpTests(Base):
    def setUp(self):
        super().setUp();self.server=b.make_server(self.root,0)
        self.thread=threading.Thread(target=self.server.serve_forever,kwargs={'poll_interval':.01},daemon=True);self.thread.start()

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();super().tearDown()

    def request(self,path,method='GET',body=None,headers=None):
        connection=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        raw=json.dumps(body).encode() if body is not None else None
        h={'Content-Type':'application/json','X-Bench-Token':self.server.bench.token};h.update(headers or {})
        connection.request(method,path,body=raw,headers=h);response=connection.getresponse()
        result=response.status,response.read(),dict(response.getheaders());connection.close();return result

    def test_bind_loopback(self):
        self.assertEqual(self.server.server_address[0],'127.0.0.1')

    def test_state_and_project(self):
        code,raw,_=self.request('/api/state');self.assertEqual(code,200)
        data=json.loads(raw);self.assertEqual(len(data['projects']),3)
        self.assertEqual(self.request('/api/projects/csb')[0],200)

    def test_static_offline(self):
        for path in ['/','/static/bench.css','/static/bench.js']:
            code,raw,headers=self.request(path);self.assertEqual(code,200);self.assertTrue(raw)
            self.assertIn("default-src 'none'",headers['Content-Security-Policy'])

    def test_viewer_is_sandboxed(self):
        code,raw,headers=self.request('/viewer/CSB-A.html');self.assertEqual(code,200)
        self.assertIn('sandbox allow-scripts;',headers['Content-Security-Policy'])
        self.assertNotIn('allow-same-origin',headers['Content-Security-Policy'])

    def test_unknown_project_http(self):
        self.assertEqual(self.request('/api/projects/nope')[0],404)

    def test_patch_http(self):
        body=self.body(status='done');self.assertEqual(self.request('/api/projects/csb','PATCH',body)[0],200)
        self.assertEqual(self.request('/api/projects/csb','PATCH',body)[0],409)

    def test_create_http(self):
        self.assertEqual(self.request('/api/projects','POST',self.body(title='New',prefixes=['NEW']))[0],201)

    def test_fit_preview_and_commit_http(self):
        body=self.report_body();self.assertEqual(self.request('/api/fit-report/preview','POST',body)[0],200)
        self.assertEqual(self.request('/api/fit-report','POST',body)[0],200)

    def test_refresh_http(self):
        self.assertEqual(self.request('/api/refresh','POST',{})[0],200)

    def test_encoded_document_link(self):
        code,raw,_=self.request('/text?path=docs%2FFit_Findings.md')
        self.assertEqual(code,200);self.assertIn(b'# Fit log',raw)

    def test_unknown_project_write(self):
        self.assertEqual(self.request('/api/projects/nope','PATCH',self.body(status='done'))[0],404)

    def test_invalid_json_http(self):
        connection=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        connection.request('POST','/api/projects',body=b'{bad',headers={'Content-Type':'application/json','X-Bench-Token':self.server.bench.token})
        response=connection.getresponse();self.assertEqual(response.status,400);response.read();connection.close()

    def test_oversize_http(self):
        self.assertEqual(self.request('/api/projects','POST',{'x':'z'*65536})[0],413)

    def test_wrong_origin(self):
        self.assertEqual(self.request('/api/projects','POST',{}, {'Origin':'https://evil.invalid'})[0],403)

    def test_wrong_host(self):
        self.assertEqual(self.request('/api/state',headers={'Host':'evil.invalid'})[0],403)

    def test_wrong_token(self):
        self.assertEqual(self.request('/api/projects','POST',{}, {'X-Bench-Token':'wrong'})[0],403)

    def test_wrong_content_type(self):
        self.assertEqual(self.request('/api/projects','POST',{}, {'Content-Type':'text/plain'})[0],415)

    def test_json_list_rejected(self):
        self.assertEqual(self.request('/api/projects','POST',[])[0],400)

    def test_bad_status_http(self):
        self.assertEqual(self.request('/api/projects/csb','PATCH',self.body(status='approved'))[0],400)

    def test_disallowed_method(self):
        self.assertEqual(self.request('/api/projects/csb','DELETE',{})[0],405)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target=Path(outside)/'private.html';target.write_text('secret',encoding='utf-8')
            try:os.symlink(target,self.root/'work/mesh-viewer/escape.html')
            except OSError as exc:self.skipTest('OS does not permit symlink creation: '+str(exc))
            self.assertEqual(self.request('/viewer/escape.html')[0],403)


# Independent parameterized regressions, each with its own disposable fixture.
ID_CASES = ['CM6A','CM6B','CM6C','CM6A-F','CM1P-A','CM1P-Q','CM1P-T1','CM1P-T10','CM1P-T5A','SCR5-H','SCR5-H10','SCR5-H11','SCR5-J5','SCR5-WP-A','SG8-M6-F','SG8-C1','SG8-PB-A','HDT-M6-A','HP4-M6-B','OPX-G','OPX-D-FRONT','OPX-G-L','SLV-F-REAR-O','MRT-H','MRT-T7','MRT-H-RIU','MRT-E-P','TFE-A','TRE-A','TSR-T1','TFG-A','RW-WP-A','MOCA-BC-A','CBL-A','RX5-B','RX4-C','PHX-C','PSB-A','ER6-H']
PREFIXES = ['CM6','CM1P','SCR5','SG8','HDT','HP4','OPX','SLV','MRT','TFE','TRE','TSR','TFG','RW','MOCA','CBL','RX5','RX4','PHX','PSB','ER6']


def id_case(value):
    def test(self):
        found=b.revision_ids(f'({value}) {value}_set.3mf **{value}**',PREFIXES)
        self.assertEqual(found,[value])
    return test


for value in ID_CASES:
    setattr(DiscoveryTests,'test_id_'+value.replace('-','_'),id_case(value))


def phrase_case(text, expected):
    def test(self):self.assertEqual(b.guess_fit([text]),expected)
    return test


for index,(text,expected) in enumerate([
    ('fits','fit'),('good fit','fit'),('perfect','fit'),('fits, but rails a tad short','fit'),
    ('too tight','problem'),('too loose','problem'),('did not fit','problem'),('would not go in','problem'),
    ('failed','problem'),('not printed','not printed'),('unprinted; fit UNKNOWN','not printed'),
    ('printing now','printing'),('fitment great','fit'),('hold well enough','fit'),('No report','not printed'),
    ('fits; no driver can reach screws','problem'),('not printing','not printed')]):
    setattr(DiscoveryTests,f'test_fit_phrase_{index:02}',phrase_case(text,expected))


def invalid_write(kind,fields,code=400):
    def test(self):
        if kind=='update':call=lambda:self.app.update('csb',self.body(**fields))
        elif kind=='create':call=lambda:self.app.create(self.body(**fields))
        else:
            body=self.report_body();body.update(fields);call=lambda:self.app.report(body)
        self.assert_problem(call,code)
    return test


for name,kind,fields in [
    ('bad_status','update',{'status':'approved'}),('numeric_notes','update',{'notes':42}),
    ('long_notes','update',{'notes':'x'*12001}),('empty_patch','update',{}),('extra_key','update',{'status':'done','root':'elsewhere'}),
    ('empty_title','create',{'title':'','prefixes':['NEW']}),('duplicate_prefix','create',{'title':'New','prefixes':['CSB']}),
    ('duplicate_id','create',{'id':'csb','title':'New','prefixes':['NEW']}),('bad_prefix','create',{'title':'New','prefixes':['../']}),
    ('prefix_string','create',{'title':'New','prefixes':'NEW'}),('repeated_prefix','create',{'title':'New','prefixes':['NEW','NEW']}),
    ('overlapping_prefix','create',{'title':'New','prefixes':['CM6A']}),('missing_card','create',{'title':'New','prefixes':['NEW'],'device_cards':['docs/devices/no.md']}),
    ('source_escape','create',{'title':'New','prefixes':['NEW'],'sources':['../x']}),
    ('unknown_revision','report',{'revision':'CSB-Z'}),('unknown_project_revision','report',{'revision':'ZZZ-A'}),
    ('bad_result','report',{'result':'approved'}),('negative_walls','report',{'walls':'-1'}),('decimal_walls','report',{'walls':'2.5'}),
    ('excess_infill','report',{'infill':'101'}),('nan_infill','report',{'infill':'NaN'}),('newline_where','report',{'where':'a\nb'}),
    ('control_notes','report',{'notes':'bad\x00'})]:
    setattr(WriteTests,'test_reject_'+name,invalid_write(kind,fields,403 if name=='source_escape' else 400))


def path_case(path):
    def test(self):self.assertIn(self.request(path)[0],(403,404))
    return test


for index,path in enumerate(['/../HANDOFF.md','/%2e%2e/HANDOFF.md','/%252e%252e/HANDOFF.md',
    '/viewer/../HANDOFF.md','/viewer/%2e%2e/HANDOFF.md','/viewer/C:\\secret','/viewer/a\\b.html',
    '/C:/secret','//evil.invalid/a','/static/../../HANDOFF.md','/static/secret.txt','/outputs/Final_3MF/CSB-A_set.3mf',
    '/text?path=../secret','/text?path=data/untouched.txt','/viewer/CSB-A.scad','/viewer/missing.html']):
    setattr(HttpTests,f'test_path_block_{index:02}',path_case(path))


def nonid_case(value):
    def test(self):self.assertEqual(b.revision_ids(value,PREFIXES),[])
    return test


for value in ['M6','U5','FP44','SCR5','CM6','NOTCM6A','CSB','2026-11-06']:
    setattr(DiscoveryTests,'test_non_revision_'+value.replace('-','_'),nonid_case(value))


if __name__=='__main__':
    unittest.main()
