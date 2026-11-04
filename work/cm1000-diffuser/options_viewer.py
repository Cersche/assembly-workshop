"""One viewer page: the 3 options side by side, each with its diffuser pulled out the way it goes in."""
import glob, os, sys, tempfile, subprocess, trimesh
names = {'A': 'A front bar', 'B': 'B rear bar', 'C': 'C rear cups'}
off = {'A': (0, -24), 'B': (80, 24), 'C': (160, 24)}
tmp = tempfile.mkdtemp(dir=sys.argv[1]); files = []
for f in sorted(glob.glob('parts/*.stl')):
    n = os.path.basename(f)[:-4]; k = n[0]; m = trimesh.load(f)
    dy = 0 if 'body' in n else off[k][1]
    m.apply_translation([off[k][0], dy, 0])
    p = os.path.join(tmp, names[k] + ' ' + n[2:].replace('_', ' ') + '.stl'); m.export(p); files.append(p)
subprocess.check_call([sys.executable, '../../tools/mesh_viewer.py', *files, '--as-is', '-o', '../mesh-viewer/CM1P-diffuser_options.html', '-t', 'CM1000 diffuser options A, B, C'])
