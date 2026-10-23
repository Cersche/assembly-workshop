"""Lay out STL parts flat for printing in one 3MF (one object per part): python tools/plate_layout_stl.py tray.stl faceplate.stl out.3mf

Thin wrapper around the app's print_layout module (same layout the app's STL export adds).
"""
import runpy, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'outputs' / 'Mechanical_Design_App'))
runpy.run_module('print_layout', run_name='__main__')
