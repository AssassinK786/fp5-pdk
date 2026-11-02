#!/usr/bin/env python3
# research PDK. Choose EG (SPICE diode) so dV/dT at 3/5/10 uA (0 -> 70 C) averages -0.56 mV/C (Butler 2005 measured), XTI = 2.
import numpy as np
f = dict(l.split() for l in open('fit_result.txt')); n, rs, Is0 = float(f['n']), float(f['rs']), float(f['is'])
k_q = 8.617333e-5; T0 = 300.15; XTI = 2.0
def V(I, T, EG):
    Vt = k_q * T
    IsT = Is0 * (T / T0) ** (XTI / n) * np.exp((T / T0 - 1) * EG / (n * Vt))
    return n * Vt * np.log(I / IsT + 1) + I * rs
def tc(EG):
    return np.mean([(V(i, 343.15, EG) - V(i, 273.15, EG)) / 70 for i in (3e-6, 5e-6, 10e-6)])
best = min(((abs(tc(eg) * 1e3 + 0.56), eg) for eg in np.arange(0.2, 1.2, 0.0005)))
EG = best[1]
print(f"EG={EG:.4f} eV -> dV/dT {tc(EG)*1e3:.3f} mV/C (target -0.56); per-current:",
      [round((V(i, 343.15, EG) - V(i, 273.15, EG)) / 70 * 1e3, 3) for i in (3e-6, 5e-6, 10e-6)])
open('fit_result.txt', 'a').write(f"eg {EG:.4f}\nxti {XTI}\n")
