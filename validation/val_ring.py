"""FP5 validation 2: 31-stage ring oscillator vs MOSIS lot T89Y measured 94.47 MHz (5 V). MOSIS ring cell geometry is not
published in the report, so a range of inverter sizes is swept (MOSIS SCMOS rings use near-minimum devices)."""
import os, subprocess, tempfile, re
PDK_ROOT = os.environ.get('FP5PDK', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
LIB = os.path.join(PDK_ROOT, 'fp5A', 'libs.tech', 'ngspice', 'fp5.lib')
def ring(c, wn, wp, n=31, vdd=5.0):
    st = ''.join(f'X{i} s{i} s{(i+1)%n} vdd iv\n' for i in range(n))
    d = f"""* ring
.lib "{LIB}" {c}
.subckt iv a y vdd
mp y a vdd vdd fp5p W={wp}u L=0.6u AS={wp*1.5}p AD={wp*1.5}p PS={2*wp+3}u PD={2*wp+3}u
mn y a 0 0 fp5n W={wn}u L=0.6u AS={wn*1.5}p AD={wn*1.5}p PS={2*wn+3}u PD={2*wn+3}u
.ends
Vdd vdd 0 {vdd}
{st}.ic v(s0)=0 v(s1)={vdd}
.control
tran 10p 120n uic
meas tran t1 when v(s0)={vdd/2} rise=3
meas tran t2 when v(s0)={vdd/2} rise=8
.endc
.end
"""
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/r.sp', 'w').write(d); o = subprocess.run(['ngspice', '-b', 'r.sp'], cwd=td, capture_output=True, text=True).stdout
    t = [float(re.search(rf'{k}\s*=\s*(\S+)', o).group(1)) for k in ('t1', 't2')]
    return 5 / (t[1] - t[0]) / 1e6
for wn, wp in ((1.8, 3.6), (3.0, 6.0), (3.6, 7.2), (6.0, 12.0)):
    print(f'Wn {wn} / Wp {wp}: ' + ', '.join(f'{c} {ring(c, wn, wp):.1f} MHz' for c in ('tt', 'ff', 'ss')) + '   (T89Y measured 94.47 MHz; 105-lot range 86-122)', flush=True)
