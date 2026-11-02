"""Refresh changed diagnostics and independently finalize Task 52 evidence; stdlib only."""
import concurrent.futures as cf
import csv,hashlib,importlib.util,itertools,json,math,struct,subprocess,sys,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent;ROOT=HERE.parent.parent;C=HERE/'checks'
sp=importlib.util.spec_from_file_location('build',HERE/'src/build_check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);g.CHECKS=C
head=f'include <{(C/"geometry.scad").as_posix()}>\n'
def vol(dst):return 0.0 if dst is None or dst.stat().st_size==84 else abs(g.mesh(dst)['volume_mm3'])
def main():
 rows=json.loads((C/'pairwise_intersections.json').read_text(encoding='utf-8'))
 names=list(dict.fromkeys(n for r in rows for n in (r['a'],r['b'])))
 if 'pi_dsi' not in names:names.append('pi_dsi')
 boxes={};items={}
 for n in names:
  f=C/f'dummy_{n}.stl'
  if n in ('ribbon_path','pi_dsi'):f=g.render('dummy_'+n,head+n+'();')
  boxes[n]=g.mesh(f)['bounds'];items[n]=f'import("{f.as_posix()}")'
 def pair(ab):
  a,b=ab;name='intersect_'+a+'_'+b
  if any(boxes[a][k][1]<=boxes[b][k][0] or boxes[b][k][1]<=boxes[a][k][0] for k in range(3)):
   (C/(name+'.stl')).unlink(missing_ok=True);v=0.;method='AABB separation/contact'
  else:v=vol(g.render(name,head+f'intersection(){{{items[a]};{items[b]};}}',True));method='OpenSCAD CGAL'
  return dict(a=a,b=b,volume_mm3=v,method=method)
 affected=[(a,b) for a,b in itertools.combinations(names,2) if a in ('ribbon_path','pi_dsi') or b in ('ribbon_path','pi_dsi')]
 rows=[r for r in rows if not {'ribbon_path','pi_dsi'}.intersection((r['a'],r['b']))]
 with cf.ThreadPoolExecutor(max_workers=3) as pool:rows.extend(pool.map(pair,affected))
 assert len(rows)==len(names)*(len(names)-1)//2
 rows.sort(key=lambda r:(names.index(r['a']),names.index(r['b'])))
 (C/'pairwise_intersections.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 with (C/'pairwise_intersections.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['a','b','volume_mm3','method']);w.writeheader();w.writerows(rows)
 physical=set(['plate','frame','floor','deck','pin1','pin2','pin3','glass','lcd','pcb','standoffs','buttons','dsi','touch','pi','hue','fan'])
 hard_names=set(['frame','glass','lcd','pcb','standoffs','buttons','dsi','touch','leaves','dsi_keepout','screw_heads','screw_drivers','pin_stroke1','pin_stroke2','pin_stroke3'])
 hard=[r for r in rows if (r['a'] in ('floor','deck') and r['b'] in hard_names) or (r['b'] in ('floor','deck') and r['a'] in hard_names)]
 physical_clashes=[r for r in rows if r['a'] in physical and r['b'] in physical and r['volume_mm3']>=1e-5]
 ribbon_clashes=[r for r in rows if 'ribbon_path' in (r['a'],r['b']) and ('floor' in (r['a'],r['b']) or 'deck' in (r['a'],r['b'])) and r['volume_mm3']>=1e-5]
 # Concatenated diagnostic keeps independent interfaces visible; it is never a printable union.
 files=[C/f'dummy_{n}.stl' for n in names if n in physical]
 chunks=[f.read_bytes() for f in files];total=sum(struct.unpack_from('<I',b,80)[0] for b in chunks)
 (C/'SCR5-H_assembled_reference.stl').write_bytes(b'SCR5-H diagnostic independent meshes; not for manufacture'.ljust(80,b' ')+struct.pack('<I',total)+b''.join(b[84:] for b in chunks))
 g.render('SCR5-H_ribbon_route',head+'ribbon_path();')
 subprocess.run([sys.executable,str(HERE/'src/SCR5-H_pack3mf.py')],check=True)
 subprocess.run([sys.executable,str(HERE/'src/SCR5-H_verify_geometry.py')],check=True)
 with zipfile.ZipFile(HERE/'SCR5-H_screen_pi_hue_set.3mf') as z:xml=z.read('3D/3dmodel.model').decode('utf-8')
 tags=dict(vertex_tags=xml.count('<vertex '),triangle_tags=xml.count('<triangle '),ns0='ns0' in xml,objects=xml.count('<object '))
 assert tags['vertex_tags'] and tags['triangle_tags'] and not tags['ns0'] and tags['objects']==7
 points=[[-24,14.5,44],[-40,24,44],[-40,32,33],[-74,85,22]];lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];length=sum(lengths)
 meshes=json.loads((C/'meshes.json').read_text(encoding='utf-8'))
 for n in meshes:
  m=g.mesh(HERE/f'SCR5-H_{n}.stl');assert m['shells']==1 and m['bad_edges']==m['degenerate']==0
  assert m['bounds']==meshes[n]['bounds']
 before=json.loads((C/'protected_before.json').read_text(encoding='utf-8'));changed=[p for p,h in before.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed,changed
 hard_pass=all(r['volume_mm3']<1e-5 for r in hard)
 out=dict(meshes=meshes,hard_tray_clearance_pass=hard_pass,hard_tray_rows=hard,physical_envelope_clashes=physical_clashes,ribbon_tray_clashes=ribbon_clashes,strict_acceptance_pass=hard_pass and not physical_clashes and not ribbon_clashes,three_mf=tags,ribbon=dict(points_mm=points,segment_lengths_mm=lengths,centreline_length_mm=length,bend_and_endpoint_allowance_mm=15,total_estimate_mm=length+15,stock_slack_mm=160-length-15,endpoint_status='Pi connector approximate, inherited F layout; bend/twist and connector registration UNKNOWN'),pair_count=len(rows),nonzero_rows=[r for r in rows if r['volume_mm3']>=1e-5],protected_files=len(before),protected_unchanged=True)
 if not out['strict_acceptance_pass']:
  target=C/'SCR5-H_UNVALIDATED_candidate_set.3mf';(HERE/'SCR5-H_screen_pi_hue_set.3mf').replace(target);tags['status']='WITHHELD: diagnostic candidate only; failed acceptance blocks proposed export';tags['candidate_path']=str(target.relative_to(HERE))
 (C/'acceptance.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 (C/'Pairwise_Intersections.md').write_text('# SCR5-H complete pairwise intersection table\n\nAll 378 pairs, including overlaid diagnostic envelopes. Nonzero diagnostic containment is not a physical assembled-part collision. No rows suppressed. See acceptance report for interpretation. Units mm³.\n\n| A | B | Volume mm³ | Method |\n|---|---|---:|---|\n'+''.join(f"| {r['a']} | {r['b']} | {r['volume_mm3']:.9f} | {r['method']} |\n" for r in rows),encoding='utf-8')
 print(json.dumps({k:v for k,v in out.items() if k not in ('meshes','hard_tray_rows','nonzero_rows')},indent=2))
 return 0 if out['strict_acceptance_pass'] else 2
if __name__=='__main__':sys.exit(main())
