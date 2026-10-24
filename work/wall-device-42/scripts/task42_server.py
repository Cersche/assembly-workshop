from pathlib import Path
import sys,json,secrets
root=Path(r'D:\Projects\assembly-workshop');sys.path.insert(0,str(root/'outputs/Mechanical_Design_App'))
import app,equipment as eq,rack_workspace
data=root/'work/wall-device-42/browser-data';data.mkdir(exist_ok=False)
store=app.Store(data/'library.sqlite3');store.load_starter()
items=[]
for i,x in enumerate((-40,40)):
 s=eq.clean(dict(name='Disposable box '+str(i+1),dev_w=60,dev_d=70,dev_h=20,device_mount='straps',dev_off_x=x,dev_off_y=13,joint='screw',u=1))
 items.append(dict(id='eq-00000000420'+str(i),name=s['name'],span=1,spec=s,parts=['tray','faceplate'],status='PROPOSED — UNVALIDATED'))
(data/'equipment-library.json').write_text(json.dumps(items),encoding='utf-8')
place=dict(id='wall-pair',equipment=items[0]['id'],slot=1,span=1,second=dict(equipment=items[1]['id']))
doc=dict(version=1,generation=None,racks=[dict(id='wall-rack',name='Task 42 disposable',slots=5,width_mm=None,depth_mm=None,pitch_mm=None,placements=[place])])
rack_workspace.save(data,doc,seed_project=store.project())
server=app.WorkshopHTTPServer(('127.0.0.1',8872),app.make_handler(store,secrets.token_hex(24)))
print('Task 42 disposable server http://127.0.0.1:8872',flush=True)
try:server.serve_forever()
finally:server.server_close()
