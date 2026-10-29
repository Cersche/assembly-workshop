"""Task 46 coloured split-rail 3MF component layout.

All vertices are already in their common print position from place(). Components
therefore use identity transforms; no colour mesh gets independently bed-normalized.
"""
def component_3mf(parts):
    import io
    import zipfile
    from xml.sax.saxutils import escape
    import print_layout as pl
    placed=pl.place(parts)
    colours=[name for name in parts if name.startswith(('pipe_','vector_'))]
    groups=[('faceplate assembly',[n for n in ['faceplate']+colours]),
            ('rail L',['rail_l']),('rail R',['rail_r'])]
    meshes=dict(placed);resources=[];build=[];next_id=1
    materials=['<base name="Body" displaycolor="#303238FF"/>']
    materials += [f'<base name="{escape(n)}" displaycolor="#EEEEEEFF"/>' for n in colours]
    material_ids={n:i+1 for i,n in enumerate(colours)}
    for label,names in groups:
        children=[]
        for name in names:
            if name not in meshes:continue
            idx={};verts=[]
            def vid(v):
                if v not in idx:idx[v]=len(verts);verts.append(v)
                return idx[v]
            faces=[tuple(vid(v) for v in t) for t in meshes[name]]
            resources.append(f'<object id="{next_id}" name="{escape(name)}" type="model" pid="1000" pindex="{material_ids.get(name,0)}"><mesh><vertices>'
                +''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>'%v for v in verts)+'</vertices><triangles>'
                +''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in faces)+'</triangles></mesh></object>')
            children.append(next_id);next_id+=1
        if not children:continue
        resources.append(f'<object id="{next_id}" name="{label}" type="model"><components>'
            +''.join(f'<component objectid="{i}"/>' for i in children)+'</components></object>')
        build.append(f'<item objectid="{next_id}"/>');next_id+=1
    model=('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
           +'<basematerials id="1000">'+''.join(materials)+'</basematerials>'+''.join(resources)+'</resources><build>'+''.join(build)+'</build></model>')
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',model)
    return buf.getvalue()
