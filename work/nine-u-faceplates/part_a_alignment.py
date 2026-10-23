"""Task 40 Part A: U8 switch (TL-SG108E) vs the U7 10-keystone panel. PROPOSED - UNVALIDATED.
Usage: python part_a_alignment.py [pitch_mm ...]     (default: candidate port pitches)
Keystone X = port_openings.faceplateSpacing(10): (i-4.5)*21.5. Ethernet keystones are the 4th-7th (4 Ethernet, 3 USB left of them).
Assumes 8 RJ45 ports centred on the case, numbered 1..8 left to right when facing the ports, and a case-centred device offset.
The STEP in Downloads gives 9 overlapping jack bodies at 14.2 mm pitch (physically impossible for 8 real ports), so the
real pitch is UNKNOWN until Brian measures; this script prints the table for any pitch you give it.
"""
import sys
KS = [(i - 4.5) * 21.5 for i in range(10)]
ETH = KS[3:7]                       # keystones 4..7
def table(p, off):
    ports = [(k - 4.5) * p + off for k in range(1, 9)]
    sel = ports[1:5]                # ports 2..5
    return [(round(s, 2), round(e, 2), round(s - e, 2)) for s, e in zip(sel, ETH)]
def best(p):
    # offset minimising the worst |error| for ports 2-5 vs keystones 4-7 (error is linear in offset, so centre the range)
    errs0 = [s - e for s, e, _ in table(p, 0)]
    return -(max(errs0) + min(errs0)) / 2
pitches = [float(a) for a in sys.argv[1:]] or [14.2, 15.0, 15.9, 16.0]
print('Ethernet keystone X:', [round(x, 2) for x in ETH])
for p in pitches:
    for label, off in (('best', best(p)), ('+15', 15.0)):
        t = table(p, off)
        print(f'pitch {p:5.2f}  offset {label:>4} = {off:6.2f} mm  port X vs keystone X, error: ' +
              '  '.join(f'{s:7.2f}/{e:7.2f}/{d:+5.2f}' for s, e, d in t) + f'   worst {max(abs(d) for *_, d in t):.2f} mm')
