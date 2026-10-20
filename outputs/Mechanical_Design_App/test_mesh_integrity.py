import io
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import zipfile
import mesh_revision as m

POINTS = [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
FACES = [(0,2,1),(0,1,3),(0,3,2),(1,2,3)]

def stl(faces=FACES, points=POINTS):
    lines=['solid fixture']
    for face in faces:
        lines += ['facet normal 0 0 0','outer loop']
        lines += ['vertex '+' '.join(map(str,points[i])) for i in face]
        lines += ['endloop','endfacet']
    return '\n'.join(lines+['endsolid fixture'])

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.source='// fixture — no mechanical design\ncube(1);'
        self.metadata={'status':'PROPOSED — UNVALIDATED','changed_parameter':{'insert_pilot':4},'limitations':['Physical fit UNKNOWN.']}
    def tearDown(self): self.tmp.cleanup()
    def render(self,cmd,**kwargs):
        Path(cmd[cmd.index('-o')+1]).write_text(stl(),encoding='ascii')
        return SimpleNamespace(returncode=0,stderr='fixture')
    def build(self):
        with patch.object(m,'compiler',return_value='fixture'),patch.object(m.subprocess,'run',side_effect=self.render):
            return m.build(self.source,self.metadata,self.root)
    def test_finite_closed_outward_mesh_and_bad_geometry(self):
        p=self.root/'mesh.stl';p.write_text(stl())
        self.assertAlmostEqual(m.read_mesh(p,'fixture')['signed_volume_mm3'],1/6)
        cases=[stl(FACES[:-1]),stl([FACES[0],FACES[0]]),stl([(0,0,1)]),stl([tuple(reversed(f)) for f in FACES]),stl([tuple(reversed(FACES[0])),*FACES[1:]]),stl(points=[(float('inf'),0,0),*POINTS[1:]])]
        for raw in cases:
            with self.subTest(raw=raw[:40]):
                p.write_text(raw)
                with self.assertRaises(ValueError): m.read_mesh(p,'fixture')





    def test_exact_collinear_retriangulation_preserves_surface_coordinates_and_volume(self):
        points=POINTS+[(0,.5,0)]
        faces=[FACES[0],FACES[1],(0,3,4),(4,3,2),FACES[3],(0,4,2)]
        p=self.root/'collinear.stl';p.write_text(stl(faces,points))
        with self.assertRaisesRegex(ValueError,'Degenerate'):m.read_mesh(p,'fixture')
        info=m.normalize_collinear_faces(p)
        result=m.read_mesh(p,'fixture')
        self.assertEqual(len(info['repairs']),1)
        self.assertEqual(set(map(tuple,result['vertices'])),set(points))
        self.assertAlmostEqual(result['signed_volume_mm3'],1/6)
        self.assertEqual(result['bounds'],[[0,0,0],[1,1,1]])
        before=p.read_bytes();self.assertEqual(m.normalize_collinear_faces(p)['repairs'],[])
        self.assertEqual(p.read_bytes(),before)
    def test_stacked_collinear_faces_are_repaired_longest_first(self):
        # 2026-10-19 (moved tray screw joints): two zero-area faces stacked on one edge, inner one first in the file.
        points=POINTS+[(0,.5,0),(0,.25,0)]
        faces=[FACES[0],FACES[1],(0,5,4),(0,3,5),(5,3,4),(4,3,2),FACES[3],(0,4,2)]
        p=self.root/'stacked.stl';p.write_text(stl(faces,points))
        with self.assertRaisesRegex(ValueError,'Degenerate'):m.read_mesh(p,'fixture')
        info=m.normalize_collinear_faces(p)
        result=m.read_mesh(p,'fixture')
        self.assertEqual(len(info['repairs']),2)
        self.assertEqual(set(map(tuple,result['vertices'])),set(points))
        self.assertAlmostEqual(result['signed_volume_mm3'],1/6)
    def test_normalization_refuses_ambiguous_or_repeated_vertex_repair(self):
        p=self.root/'bad.stl'
        for faces,points in [([(0,0,1)],POINTS), ([(0,4,2)],POINTS+[(0,.5,0)])]:
            p.write_text(stl(faces,points))
            before=p.read_bytes()
            with self.assertRaises(ValueError):m.normalize_collinear_faces(p)
            self.assertEqual(p.read_bytes(),before)

if __name__=='__main__':unittest.main()
