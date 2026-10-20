from pathlib import Path
import re, zipfile, xml.etree.ElementTree as E
root=Path(__file__).resolve().parents[1]
out=root/'outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix'
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',ns)
def elem(parent,tag,**attrs): return E.SubElement(parent,'{'+ns+'}'+tag,attrs)
model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
resources=elem(model,'resources')
for oid,name in [(1,'faceplate'),(2,'tray')]:
    raw=(out/(name+'.stl')).read_text()
    vs=[tuple(map(float,m)) for m in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',raw)]
    obj=elem(resources,'object',id=str(oid),type='model',name=name)
    mesh=elem(obj,'mesh'); ve=elem(mesh,'vertices'); tr=elem(mesh,'triangles')
    unique={}; ids=[]
    for v in vs:
        if v not in unique:
            unique[v]=len(unique);elem(ve,'vertex',**dict(zip(['x','y','z'],map(str,v))))
        ids.append(unique[v])
    for i in range(0,len(ids),3):elem(tr,'triangle',v1=str(ids[i]),v2=str(ids[i+1]),v3=str(ids[i+2]))
obj=elem(resources,'object',id='3',type='model',name='Pi4 assembly - corrected gussets')
cs=elem(obj,'components')
for oid in [1,2]:elem(cs,'component',objectid=str(oid))
build=elem(model,'build');elem(build,'item',objectid='3')
with zipfile.ZipFile(out/'assembly_review.3mf','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))
print(out/'assembly_review.3mf')
