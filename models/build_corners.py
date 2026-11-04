"""FP5 (research PDK): BSIM3 corners for AMI/onsemi C5 0.5 um from public MOSIS lot data.
Typical = MOSIS run T89Y (Jan 2009, median lot: Idss N 461 / P -246 uA/um, Vth 0.67 / -0.91 V, tox 141 A).
Corner targets = median +- 3 sigma of 105 unique C5 lots (MOSIS parametric reports, see SOURCES.md):
  sigma: Vth_short N 24 mV, P 15 mV; Idss N 9.8, P 9.4 uA/um (W/L 15/0.6, |Vgs|=|Vds|=5 V); tox 1.6 A.
Fit, per device and corner: TOX moved +-3 sigma (ff: thin, ss: thick; fs/sf keep typical), then VTH0 and U0 adjusted so the
MOSIS short-channel test device (W/L 15/0.6) hits typ + delta(Vth) and typ + delta(Idss); delta-based, so the Vth definition
cancels. Writes fp5.lib with .lib sections tt ff ss fs sf (models fp5n / fp5p) for ngspice (LEVEL 8 = BSIM3v3.1).

Self-contained: dev() below runs ngspice directly; the old external FP5_BUILD_HELPER
dependency is removed. Method: Vth = Vgs at Id = 0.1 uA * W/L (constant-current);
Idss = |Id| at |Vgs|=|Vds|=5 V. Delta-based fitting means only the *change* in
Vth/Idss matters, so the exact definition is not critical."""
import os, re, subprocess, tempfile
raw = open('t89y_raw.lib').read()
blk = {t: re.search(rf'(?is)\.model cmos{t} .*?\)', raw).group(0) for t in 'np'}
def setp(b, k, v): return re.sub(rf'(?im)(\b{k}\s*=\s*)([-0-9.eE+]+)', lambda g: g.group(1) + f'{v:.6g}', b, count=1)
def getp(b, k): return float(re.search(rf'(?im)\b{k}\s*=\s*([-0-9.eE+]+)', b).group(1))
SIG = {'n': (0.024, 9.8), 'p': (0.015, 9.4)}; STOX = 1.6e-10
CORN = {'tt': (0, 0, 0), 'ff': (-1, -1, -1), 'ss': (1, 1, 1), 'fs': (-1, 1, 0), 'sf': (1, -1, 0)}  # (N speed, P speed, tox) -1 = fast
def both(n, p): return n.replace('.MODEL CMOSN', '.model mn').replace('.model cmosn', '.model mn') + '\n' + p.replace('.MODEL CMOSP', '.model mp').replace('.model cmosp', '.model mp')

_VT_CUR = 0.1e-6   # A * W/L for constant-current Vth
def dev(cards, t, w, l, v):
    """Return (vth, idss_A) for device type t ('n'/'p') in a two-card lib.
    cards: text with .model mn and .model mp; we instantiate the matching one.
    w, l in um; v = supply volts."""
    mod = 'mn' if t == 'n' else 'mp'
    sgn = 1 if t == 'n' else -1
    id_vth = _VT_CUR * w / l            # constant-current threshold point
    deck = f"""* vth + idss measurement
{cards}
M1 d g 0 0 {mod} W={w}u L={l}u
Vd d 0 {sgn*v}
Vg g 0 0
.control
dc Vg 0 {sgn*v} {sgn*0.01}
let id = abs(i(Vd))
wrdata out.dat v(g) id
.endc
.end
"""
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/d.sp', 'w').write(deck)
        subprocess.run(['ngspice', '-b', 'd.sp'], cwd=td,
                       capture_output=True, text=True)
        rows = [l.split() for l in open(f'{td}/out.dat')]
        # wrdata: per vector (sweep, real, imag) -> cols: sweep, vg, imag, id
        data = []
        for r in rows:
            try:
                data.append((float(r[1]), float(r[3])))
            except (IndexError, ValueError):
                pass
    if not data:
        raise RuntimeError("ngspice produced no sweep data")
    data.sort(key=lambda p: abs(p[0]))
    idd = data[-1][1]                                  # Id at |Vgs| = v (A)
    vt = next((g for g, i in data if i >= id_vth), data[-1][0])
    return abs(vt), idd

def meas(n, p, t):
    vt, idd = dev(both(n, p), t, 15, 0.6, 5.0); return vt, idd * 1e6 / 15   # V, uA/um
ref = {t: meas(blk['n'], blk['p'], t) for t in 'np'}
print('typical T89Y card: N Vt %.3f Idss %.0f | P Vt %.3f Idss %.0f uA/um' % (*ref['n'], *ref['p']))
out = {}
for c, (sn, sp, so) in CORN.items():
    b = dict(blk)
    for t, s in (('n', sn), ('p', sp)):
        bb = setp(b[t], 'TOX', getp(b[t], 'TOX') + so * 3 * STOX)
        tv = ref[t][0] + s * 3 * SIG[t][0]; ti = ref[t][1] - s * 3 * SIG[t][1]   # fast: lower |Vt|, higher Idss
        sgn = 1 if t == 'n' else -1
        for it in range(10):
            b2 = dict(b); b2[t] = bb
            vt, idd = meas(b2['n'], b2['p'], t)
            if abs(vt - tv) < 0.002 and abs(idd / ti - 1) < 0.003: break
            bb = setp(bb, 'VTH0', getp(bb, 'VTH0') + sgn * (tv - vt))
            b2[t] = bb; vt, idd = meas(b2['n'], b2['p'], t)
            bb = setp(bb, 'U0', getp(bb, 'U0') * (ti / idd) ** 1.2)
        b[t] = bb
        print(f'{c} {t}: Vt {vt:.3f} (tgt {tv:.3f}) Idss {idd:.1f} (tgt {ti:.1f}) TOX {getp(bb,"TOX")*1e10:.1f} A', flush=True)
    out[c] = b
L = ['* FP5 (research PDK, not a foundry deliverable): AMI/onsemi C5 0.5 um BSIM3 corners. See build_corners.py.',
     '* Typical = MOSIS lot T89Y (2009). Corners = +-3 sigma of 105 MOSIS C5 lots. Vdd 5 V (3.3 V usable). Drawn L >= 0.6 um.',
     '* Use: .lib "fp5.lib" tt   (or ff ss fs sf); devices fp5n / fp5p (4-terminal), give AS/AD/PS/PD for junction caps.']
for c, b in out.items():
    L += [f'.lib {c}', b['n'].replace('CMOSN', 'fp5n').replace('cmosn', 'fp5n'), b['p'].replace('CMOSP', 'fp5p').replace('cmosp', 'fp5p'), f'.endl {c}', '']
open("fp5.lib", 'w').write('\n'.join(L) + '\n'); print('wrote fp5.lib')
