# FP5 validation (2026-10-19)
| check | FP5 | reference | verdict |
|---|---|---|---|
| NMOS 27/0.6 VGS at 5 uA | 0.640 V (tt) | 0.663 V Kerstetter; 0.642 V Baker C5 card same script | OK |
| PMOS 54/0.6 VSG at 5 uA | 0.886 V | 0.912 V Kerstetter; 0.891 V Baker card | OK |
| gm at 10 uA, N / P | 193 / 183 uA/V | Baker card 215 / 189; Kerstetter table 106 / 121 | OK vs card (-10 %); Kerstetter's table not reproducible from his own card |
| ro / lambda at 5 uA, L 0.6 | 0.7 MOhm, 0.27 1/V | Baker card 0.6 MOhm, 0.35; Kerstetter 11 MOhm, 0.018 | OK vs card |
| NAND2 FO1 (own input load, sharp edge) | 95-104 ps | AMI5HS NA21 silicon databook 82 ps | ~15 % slow, within C5 lot spread (14 %) |
| 31-stage ring, 5 V | 186-227 MHz (no wiring) | MOSIS T89Y measured 94.5 MHz | 2.3x fast: MOSIS ring layout parasitics unpublished; same ~2x seen for every MOSIS lot |
Scripts: val_devices.py, val_ring.py (outputs *.txt). Kerstetter op-amp full reproduction needs the schematic figures (images).

## 2026-10-23: re-run on recentred models + new checks
| check | FP5 | reference | verdict |
|---|---|---|---|
| Kerstetter op-amp 5 V, no load (tt) | 86.2 dB, 5.45 MHz, PM 89 deg | 82.4 dB, 4.49 MHz (Kerstetter); Baker card 81.7 dB, 5.32 MHz | OK (kerstetter/results.txt) |
| devices at 5 uA | unchanged (weak inversion, RDSW has no effect) | as above | OK |
| 31-stage ring, 5 V | 210-256 MHz (tt) | T89Y 94.5 MHz | ~2.4x fast, unpublished ring layout parasitics |
| Schottky diode I-V / TC | fp5_schottky fit, rms 3.7 mV; -0.56 mV/C at 5 uA | Butler 2005 measured | OK (butler/) |
| Butler Schottky bandgap | 24.2 uA, Rref 54.0 k for 0.400 V | 23.75 uA, Rref 54.8 k | OK; TC bracket -860..+1230 ppm/C contains measured -107..+500 (butler/README.md) |
