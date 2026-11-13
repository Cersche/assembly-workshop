"""Operator-only acceptance harness. NOT imported or run by the Bench application.

Creates an OS temporary metadata copy, starts explicit --root test servers, runs
urllib checks, and records evidence outside the repository. Git is read-only here.
The Bench server itself imports no subprocess and cannot run this harness.
"""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.bench import bench


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checkpoint():
    return {'git_status': subprocess.check_output(['git','status','--porcelain'],cwd=ROOT).decode('utf-8'),
            'markdown': {name: sha(ROOT/name) for name in (bench.FIT,bench.WORKFLOW)}}


def copy_metadata(destination):
    """Full docs; work data; all scanned output text and listings, no mesh bytes."""
    shutil.copytree(ROOT/'docs',destination/'docs')
    for folder in ('work/bench','work/workbench'):
        shutil.copytree(ROOT/folder,destination/folder)
    shutil.copy2(ROOT/'HANDOFF.md',destination/'HANDOFF.md')
    for base,dirs,files in os.walk(ROOT/'outputs',followlinks=False):
        dirs[:]=[d for d in dirs if not d.startswith(('Mechanical_Design_App','Phase','Session_','.')) and d.lower() not in ('src','stl','checks','data','revisions','cache','__pycache__') and not (Path(base)/d).is_symlink()]
        rel=Path(base).relative_to(ROOT)
        (destination/rel).mkdir(parents=True,exist_ok=True)
        for file in files:
            source=Path(base)/file;target=destination/rel/file
            if source.is_symlink():continue
            if file in ('README.md','release_report.md'):shutil.copy2(source,target)
            elif file.lower().endswith('.3mf'):
                target.write_bytes(b'')
                shutil.copystat(source,target)
    viewers=destination/'work/mesh-viewer';viewers.mkdir(parents=True,exist_ok=True)
    for source in (ROOT/'work/mesh-viewer').glob('*.html'):
        if source.is_symlink():continue
        target=viewers/source.name
        target.write_text('<!doctype html><html><head><title>Acceptance viewer fixture</title></head><body><p>Acceptance fixture only. No part geometry copied.</p><canvas width="300" height="180"></canvas><script>const c=document.querySelector("canvas").getContext("2d");c.fillStyle="#67a8ff";c.fillRect(40,30,180,100);</script></body></html>',encoding='utf-8')
        shutil.copystat(source,target)
    return destination


def http(path, method='GET', body=None, state=None, port=8720):
    headers={}
    if body is not None:
        headers={'Content-Type':'application/json','X-Bench-Token':state['token']}
    request=Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(body).encode('utf-8') if body is not None else None,headers=headers,method=method)
    start=time.perf_counter()
    with urlopen(request,timeout=20) as response:
        raw=response.read();code=response.status
    return code,raw,time.perf_counter()-start


def start_server(root=None,port=8720):
    # Windows can permit a second bind; never test against an existing server.
    with socket.socket() as probe:
        probe.settimeout(1)
        if probe.connect_ex(('127.0.0.1', port)) == 0:
            raise RuntimeError(f'Port {port} is occupied; stop the existing test server first.')
    args=[sys.executable,'-B',str(ROOT/'tools/bench/bench.py'),'--port',str(port)]
    if root is not None:args+=['--root',str(root)]
    process=subprocess.Popen(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    line=process.stdout.readline().decode('utf-8').strip()
    if process.poll() is not None:raise RuntimeError(process.stderr.read().decode('utf-8'))
    return process,line


def stop_server(process):
    process.terminate()
    try:process.wait(timeout=5)
    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)


def smoke(log):
    code,raw,elapsed=http('/api/state');state=json.loads(raw)
    log.append(f'GET /api/state first: {code}, {elapsed:.6f} s, scan {state["scan_seconds"]:.6f} s, {len(raw)} bytes')
    code,raw,elapsed=http('/api/state');log.append(f'GET /api/state cached: {code}, {elapsed:.6f} s')
    for route in ['/api/health','/api/projects','/','/static/bench.css','/static/bench.js']+['/api/projects/'+p['id'] for p in state['projects']]:
        code,raw,elapsed=http(route);assert code==200
        log.append(f'GET {route}: {code}, {elapsed:.6f} s, {len(raw)} bytes')
    for p in state['projects']:
        assert all(r['status'] in ('fit','problem','not printed','printing') and r['status_is_guess'] for r in p['revisions'])
    for path in [bench.FIT,bench.WORKFLOW,'HANDOFF.md','outputs/Final_3MF/README.md']:
        from urllib.parse import quote
        code,raw,elapsed=http('/text?path='+quote(path,safe=''));assert code==200
        log.append(f'GET text {path}: {code}, {elapsed:.6f} s')
    return state


def full_copy_smoke(root):
    """Used by an opt-in unittest on an already prepared temp root."""
    start=time.perf_counter();app=bench.Bench(root);data=app.snapshot()
    assert len(data['projects'])>=14
    assert all(r['status'] for p in data['projects'] for r in p['revisions'])
    print(f'Full-copy metadata smoke: {len(data["projects"])} projects, {sum(len(p["revisions"]) for p in data["projects"])} revisions, {time.perf_counter()-start:.6f} s')
    return data


def run(output):
    output.mkdir(parents=True,exist_ok=True)
    copied=copy_metadata(output/'repo')
    log=[];before=checkpoint();log.append('BEFORE REAL READ ACCEPTANCE\n'+json.dumps(before,indent=2))
    server,line=start_server()
    try:
        log.append(line);real=smoke(log)
        # Refresh is a read-only POST; preview is also read-only.
        code,raw,elapsed=http('/api/refresh','POST',{},real);assert code==200;real=json.loads(raw)
        log.append(f'POST /api/refresh (read-only): {code}, {elapsed:.6f} s')
        preview={'revision':'CSB-A','result':'Other','where':'Preview only; not submitted','walls':'','infill':'','notes':''}
        code,raw,elapsed=http('/api/fit-report/preview','POST',preview,real);assert code==200
        log.append(f'POST /api/fit-report/preview (read-only): {code}, {elapsed:.6f} s')
    finally:stop_server(server)
    after=checkpoint();log.append('AFTER REAL READ ACCEPTANCE\n'+json.dumps(after,indent=2));assert before==after
    log.append('PASS: git status and both markdown SHA-256 hashes unchanged.')
    (output/'real-state.json').write_text(json.dumps(real,indent=2),encoding='utf-8')
    copy_before={p.relative_to(copied).as_posix():sha(p) for p in copied.rglob('*') if p.is_file()}
    server,line=start_server(copied)
    try:
        log.append('\nTEMP COPY ACCEPTANCE\n'+line);data=smoke(log)
        real_counts={p['id']:len(p['revisions']) for p in real['projects']}
        copy_counts={p['id']:len(p['revisions']) for p in data['projects']}
        assert real_counts==copy_counts,(real_counts,copy_counts)
        log.append('PASS: copy revision counts match the real read-only scan.')
        actions=[('/api/projects/csb','PATCH',{'status':'report-due','notes':'Temporary acceptance note; never the real repo.'}),
                 ('/api/projects','POST',{'title':'Acceptance sample','prefixes':['QA54']}),
                 ('/api/fit-report','POST',{'revision':'CSB-A','result':'Fits','where':'Temporary acceptance fixture only','walls':'2','infill':'10','notes':'No physical claim'})]
        for route,method,body in actions:
            old={name:(copied/name).read_bytes() for name in bench.WRITABLE}
            body['hashes']=data['hashes'];code,raw,elapsed=http(route,method,body,data)
            log.append(f'{method} {route}: {code}, {elapsed:.6f} s\n'+raw.decode('utf-8'))
            for name,previous in old.items():
                current=(copied/name).read_bytes()
                if current==previous:continue
                assert (copied/(name+'.bak')).read_bytes()==previous
                if name in (bench.FIT,bench.WORKFLOW):assert current.startswith(previous)
                log.append('DIFF '+name+'\n'+''.join(difflib.unified_diff(previous.decode('utf-8').splitlines(True),current.decode('utf-8').splitlines(True),fromfile=name+' before',tofile=name+' after')))
            data=json.loads(http('/api/state')[1])
        assert not list(copied.rglob('*.tmp'))
        copy_after={p.relative_to(copied).as_posix():sha(p) for p in copied.rglob('*') if p.is_file()}
        changed={name for name in copy_after if copy_before.get(name)!=copy_after[name]}
        assert changed==set(bench.WRITABLE)|{name+'.bak' for name in bench.WRITABLE},changed
        log.append('PASS: only the three allowed files and .bak copies changed; previous markdown bytes preserved; temporary files cleaned.')
    finally:stop_server(server)
    final=checkpoint();assert final==before
    log.append('PASS: real repository checkpoint still unchanged after all temp-copy writes.')
    (output/'acceptance.txt').write_text('\n'.join(log)+'\n',encoding='utf-8')
    (output/'checkpoint.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    print('\n'.join(log[:4]));print('Evidence:',output);print('ALL HTTP / WRITE / PRESERVATION CHECKS PASSED')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    destination=args.output or Path(tempfile.mkdtemp(prefix='bench-acceptance-'))
    if destination.resolve().is_relative_to(ROOT):raise SystemExit('Acceptance evidence must be outside the real repository.')
    run(destination)
