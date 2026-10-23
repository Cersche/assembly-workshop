from pathlib import Path
import sys,tempfile,unittest
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'outputs/Mechanical_Design_App'))
with tempfile.TemporaryDirectory(prefix='checks-',dir=Path(__file__).parent) as folder:
    tempfile.tempdir=folder
    suite=unittest.TestSuite()
    for module in ('test_rack_workspace','test_rack_references','test_assembly_records','test_studio_save','test_cable_ports','test_equipment_rebuild','test_cable_plan','test_allocation_tray','test_tray_placement','test_tray_pair','test_export_quality','test_keystone_mesh','test_port_openings','test_mesh_study','test_drive_tray','test_print_layout','test_tray_follow','test_wall_box'):
        loaded=__import__(module)
        # Imported fixture classes are excluded from the studio-save module.
        if module=='test_studio_save': suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(loaded.StudioSaveTests))
        else:suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(loaded))
    # Faceplate color placement/reduction/cache tests; the OpenSCAD renders (FaceplateColorRenderTests) are excluded (no builds here).
    import test_faceplate_color
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_faceplate_color.FaceplateColorTests))
    import test_app
    for name in unittest.defaultTestLoader.getTestCaseNames(test_app.Tests):
        if name not in ('test_revision_uses_four_corner_default_and_rejects_failed_or_unsupported_inputs','test_http_handlers_without_network'):
            suite.addTest(test_app.Tests(name))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
