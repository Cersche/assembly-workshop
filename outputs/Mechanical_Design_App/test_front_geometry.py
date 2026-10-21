"""Manual temporary image-render benchmark; no STL export or user data.
Run directly; deliberately not imported by run_checks (no automatic builds).
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import equipment as E
import mesh_revision


def main():
    folder=Path(os.environ['AW_PREVIEW_DIR']) if os.environ.get('AW_PREVIEW_DIR') else Path(tempfile.mkdtemp(prefix='aw33-image-preview-'))
    folder.mkdir(parents=True,exist_ok=True)
    print('Disposable images: '+str(folder),flush=True)
    fixtures={
        'optiplex-1u':dict(name='Dimension-only OptiPlex preview',dev_w=182.5,dev_d=194.5,dev_h=36.8,u=1,device_mount='sleeve',joint='screw',holes=[]),
        'ports-1u':dict(name='Synthetic four-port inserts tray',dev_w=150,dev_d=100,dev_h=16,u=1,device_mount='inserts',joint='screw',holes=[[10,15],[140,85]],ports=[dict(x=x,z=26,w=14,h=8,r=1) for x in (-42,-14,14,42)]),
        'flush-window':dict(name='Synthetic flush window',dev_w=85,dev_d=100,dev_h=20,u=1,device_mount='inserts',joint='single',holes=[[10,15]],front_position='flush'),
        'keepclear-rear':dict(name='Synthetic solid rear bracket',dev_w=100,dev_d=100,dev_h=20,u=1,device_mount='flat',joint='screw',holes=[],rear_support=True,protrusions=[dict(face='back',x=40,y=200,z=5,w=10,d=40,h=10,keep_clear=True)])}
    results=[]
    for name,raw in fixtures.items():
        for style in (('none',) if name=='keepclear-rear' else ('none','chamfer','rounded')):
            s=E.clean(dict(raw,bezel=style));stem=name+'-'+style
            source=folder/(stem+'.scad');source.write_text(E.source(s),encoding='utf-8')
            start=time.perf_counter()
            run=subprocess.run([mesh_revision.compiler(),'--render','--autocenter','--viewall','--imgsize=1000,600','--camera=140,-350,200,0,-2,22','-D','part="'+('rear_bracket' if name=='keepclear-rear' else 'faceplate')+'"','-o',str(folder/(stem+'.png')),str(source)],capture_output=True,text=True,timeout=180,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            row=dict(fixture=name,style=style,seconds=round(time.perf_counter()-start,3),returncode=run.returncode,notes=E.port_openings.bezel_plan(s)['notes'])
            results.append(row);print(json.dumps(row),flush=True)
            if run.returncode or 'ERROR:' in run.stderr:raise RuntimeError(run.stderr[-3000:])
    print(json.dumps(dict(folder=str(folder),results=results)),flush=True)

if __name__=='__main__':main()
