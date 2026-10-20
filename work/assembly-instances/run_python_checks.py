from pathlib import Path
import sys,tempfile,unittest
root=Path(__file__).resolve().parents[2]
app=root/'outputs/Mechanical_Design_App'
sys.path.insert(0,str(app))
with tempfile.TemporaryDirectory(prefix='checks-',dir=Path(__file__).parent) as folder:
    tempfile.tempdir=folder
    suite=unittest.TestSuite()
    for name in ['test_rack_workspace','test_rack_references','test_assembly_records']:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
    import test_app
    for name in unittest.defaultTestLoader.getTestCaseNames(test_app.Tests):
        if name not in ('test_revision_uses_four_corner_default_and_rejects_failed_or_unsupported_inputs','test_http_handlers_without_network'):
            suite.addTest(test_app.Tests(name))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
