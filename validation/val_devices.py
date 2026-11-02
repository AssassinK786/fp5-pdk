"""FP5 validation 1: small-signal device parameters vs Kerstetter (UNLV EE420 2019, C5 op-amp, Baker C5 card), 5 V, 27 C.
NMOS 27u/0.6u, PMOS 54u/0.6u: VGS at ID = 5 uA (no body effect), gm at 10 uA, ro / lambda at 5 uA (VDS = 1 V)."""
import os, subprocess, tempfile, re, numpy as np
PDK_ROOT = os.environ.get('FP5PDK', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
LIB = os.path.join(PDK_ROOT, 'fp5A', 'libs.tech', 'ngspice', 'fp5.lib')
def run(deck):
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/a.sp', 'w').write(deck); o = subprocess.run(['ngspice', '-b', 'a.sp'], cwd=td, capture_output=True, text=True).stdout
        return o, td
def dev(corner, typ, W, L):
    s = 1 if typ == 'n' else -1; m = 'fp5n' if typ == 'n' else 'fp5p'
    d = f"""* dev
.lib "{LIB}" {corner}
M1 d g 0 0 {m} W={W}u L={L}u AS={W*1.5}p AD={W*1.5}p PS={2*W+3}u PD={2*W+3}u
Vd d 0 {s*1.0}
Vg g 0 0
.control
dc Vg 0 {s*2.0} {s*0.0005}
wrdata vg.txt i(Vd)
.endc
.end
"""
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/a.sp', 'w').write(d); subprocess.run(['ngspice', '-b', 'a.sp'], cwd=td, capture_output=True)
        a = np.loadtxt(f'{td}/vg.txt'); vg, idd = np.abs(a[:, 0]), np.abs(a[:, 1])
    vgs5 = np.interp(5e-6, idd, vg); vgs10 = np.interp(10e-6, idd, vg)
    gm10 = np.interp(vgs10, vg, np.gradient(idd, vg))
    # output resistance at VGS(5uA)
    d2 = f"""* ro
.lib "{LIB}" {corner}
M1 d g 0 0 {m} W={W}u L={L}u AS={W*1.5}p AD={W*1.5}p PS={2*W+3}u PD={2*W+3}u
Vd d 0 0
Vg g 0 {s*vgs5}
.control
dc Vd 0 {s*3} {s*0.01}
wrdata vd.txt i(Vd)
.endc
.end
"""
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/b.sp', 'w').write(d2); subprocess.run(['ngspice', '-b', 'b.sp'], cwd=td, capture_output=True)
        b = np.loadtxt(f'{td}/vd.txt'); vd, idd2 = np.abs(b[:, 0]), np.abs(b[:, 1])
    k = (vd > 0.8) & (vd < 1.5); slope = np.polyfit(vd[k], idd2[k], 1)[0]; id1 = np.interp(1.0, vd, idd2)
    return vgs5, gm10 * 1e6, 1 / slope / 1e6, slope / id1
print('Kerstetter (Baker C5 card): NMOS VGS 0.663 V, gm 106 uA/V, ro 11 MOhm, lambda 0.018 | PMOS VSG 0.912, gm 121, ro 12.5, lambda 0.016')
for c in ('tt', 'ff', 'ss'):
    for t, W in (('n', 27), ('p', 54)):
        v, g, r, l = dev(c, t, W, 0.6)
        print(f'FP5 {c} {"NMOS" if t=="n" else "PMOS"} {W}/0.6: V(G)S {v:.3f} V, gm {g:.0f} uA/V, ro {r:.1f} MOhm, lambda {l:.3f} 1/V', flush=True)
