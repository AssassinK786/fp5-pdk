#!/usr/bin/env python3
# research PDK. Fit a physical diode model (n >= 1) to Butler 2005 Fig 4.2 (MOSIS 0.5 um, metal1 on n-well, 0.25 um^2).
# V = n Vt ln(I/Is + 1) + I Rs is explicit in V, so fit in the V domain by grid search (no scipy needed).
import numpy as np
d = np.loadtxt('fig42_digitized.csv', delimiter=',', comments='#'); V, I = d[:, 0], d[:, 1] * 1e-6
Vt = 0.025852
best = None
for n in np.arange(1.0, 2.501, 0.01):
    for rs in np.arange(1000, 5001, 25):
        # for fixed n, rs: Is minimizing V error -> 1-D log grid
        for lis in np.arange(-16, -5, 0.02):
            Is = 10 ** lis
            Vm = n * Vt * np.log(I / Is + 1) + I * rs
            e = np.sqrt(np.mean((Vm - V) ** 2))
            if best is None or e < best[0]:
                best = (e, n, rs, Is)
e, n, rs, Is = best
print(f"fit: n={n:.2f} Rs={rs:.0f} ohm Is={Is:.3e} A  rms V error {e*1e3:.1f} mV")
# Butler's own fit (n=0.43, Is=7e-18, Rs=2.2k) on the same data, for comparison
Vb = 0.43 * Vt * np.log(I / 7e-18 + 1) + I * 2200
print(f"Butler appendix model rms V error {np.sqrt(np.mean((Vb - V) ** 2))*1e3:.1f} mV")
open('fit_result.txt', 'w').write(f"n {n:.3f}\nrs {rs:.1f}\nis {Is:.4e}\nrms_mV {e*1e3:.2f}\n")
