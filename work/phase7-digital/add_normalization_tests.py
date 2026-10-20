from pathlib import Path
p=Path('outputs/Mechanical_Design_App/test_mesh_integrity.py');s=p.read_text(encoding='utf-8');i=s.index("\nif __name__")
s=s[:i]+'''
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
    def test_normalization_refuses_ambiguous_or_repeated_vertex_repair(self):
        p=self.root/'bad.stl'
        for faces,points in [([(0,0,1)],POINTS), ([(0,4,2)],POINTS+[(0,.5,0)])]:
            p.write_text(stl(faces,points))
            before=p.read_bytes()
            with self.assertRaises(ValueError):m.normalize_collinear_faces(p)
            self.assertEqual(p.read_bytes(),before)
''' +s[i:];p.write_text(s,encoding='utf-8')
p=Path('outputs/Mechanical_Design_App/README.md');s=p.read_text(encoding='utf-8');s=s.replace('New renders use the separate `pi4-mesh-v2` identity namespace','New renders use the separate `pi4-mesh-v2-triangulation1` identity namespace')
s=s.replace('Older immutable cache entries are preserved without modification.', 'OpenSCAD can emit an exact zero-area collinear triangle. A bounded export step removes that empty face and splits its unique long-edge neighbor at the same existing interior vertex. Coordinates, surface and orientation stay unchanged; ambiguous repairs are rejected. Both raw renderer and processed STL hashes and the repair trace are recorded in revision.json. Strict mesh checks run afterward. This is not general mesh repair.\n\nOlder immutable cache entries are preserved without modification.')
p.write_text(s,encoding='utf-8')
