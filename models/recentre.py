"""FP5 recentre (PERSONAL USE): the MOSIS T89Y card under-predicts its own lot's short-channel Idss (ngspice: N 385 vs 461,
P 224 vs 246 uA/um, W/L 15/0.6 at 5 V) because of its RDSW fit. Scale RDSW per polarity (same factor in every corner) until
the tt card hits the lot report; corners keep their deltas. Writes fp5.lib (backup fp5_pre_recentre.lib)."""
import re, os, subprocess, tempfile, numpy as np
lib = open('fp5_pre_recentre.lib').read()
def sect(c): return re.search(rf'(?is)^\.lib {c}\s*\n(.*?)^\.endl', lib, re.M).group(1)
def getp(b, k): return float(re.search(rf'(?im)\b{k}\s*=\s*([-0-9.eE+]+)', b).group(1))
def setp(b, k, v): return re.sub(rf'(?im)(\b{k}\s*=\s*)([-0-9.eE+]+)', lambda g: g.group(1) + f'{v:.6g}', b, count=1)
def blk(s, t): return re.search(rf'(?is)\.model fp5{t}\s.*?\)', s).group(0)
def idss(card, t):
    s = 1 if t == 'n' else -1; m = card.replace(f'fp5{t}', 'mm', 1)
    d = f"* i\n{m}\nM1 d d 0 0 mm W=15u L=0.6u\nVd d 0 {5 * s}\n.control\nop\nprint i(Vd)\n.endc\n.end\n"
    d = f"* i\n{m}\nM1 d g 0 0 mm W=15u L=0.6u\nVd d 0 {5 * s}\nVg g 0 {5 * s}\n.control\nop\nprint i(Vd)\n.endc\n.end\n"
    with tempfile.TemporaryDirectory() as td:
        open(f'{td}/i.sp', 'w').write(d); o = subprocess.run(['ngspice', '-b', 'i.sp'], cwd=td, capture_output=True, text=True).stdout
    return abs(float(re.findall(r'i\(vd\) = (\S+)', o)[-1])) / 15e-6
tt = sect('tt'); target = {'n': 461.0, 'p': 246.0}; f = {}
for t in 'np':
    b = blk(tt, t); r0 = getp(b, 'RDSW'); lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2; i = idss(setp(b, 'RDSW', r0 * mid), t)
        lo, hi = (mid, hi) if i > target[t] else (lo, mid)
    f[t] = (lo + hi) / 2; print(f'{t}: RDSW x {f[t]:.3f} ({r0:.0f} -> {r0 * f[t]:.0f}), tt Idss {idss(setp(b, "RDSW", r0 * f[t]), t):.0f} (target {target[t]:.0f})')
out = lib
for c in ('tt', 'ff', 'ss', 'fs', 'sf'):
    s = sect(c); s2 = s
    for t in 'np':
        b = blk(s, t); s2 = s2.replace(b, setp(b, 'RDSW', getp(b, 'RDSW') * f[t]))
    out = out.replace(s, s2)
out = out.replace('* FP5 (PERSONAL USE', f'* RECENTRED 2026-10-21: RDSW x {f["n"]:.3f} (N) / x {f["p"]:.3f} (P) in all corners so tt matches lot T89Y Idss (models/recentre.py)\n* FP5 (PERSONAL USE', 1)
open('fp5.lib', 'w').write(out)
for c in ('tt', 'ff', 'ss'):
    s = re.search(rf'(?is)^\.lib {c}\s*\n(.*?)^\.endl', out, re.M).group(1)
    print(c, 'IdN %.0f IdP %.0f' % (idss(blk(s, 'n'), 'n'), idss(blk(s, 'p'), 'p')))
