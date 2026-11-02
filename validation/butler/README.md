# Butler 2005 Schottky bandgap on FP5 (research PDK)

Source: D. L. Butler (adv. R. J. Baker), *Low-Voltage Bandgap Reference Design Utilizing Schottky Diodes*, Boise State
MS project report 2005 (+ MWSCAS 2005, doi:10.1109/MWSCAS.2005.1594470); MOSIS AMI 0.5 um lot T4BP.
Archive: VLSI/0.11-0.9um/0.5µm/. Text extract: butler_report.txt.

## 1. Schottky device (fp5_schottky, passives/fp5_passives.lib)
Metal1 directly on n-well, 0.5 x 0.5 um contact; EXPERIMENTAL (not an SCMOS device; UMD MURI slides report Schottky
contacts that did not form on some MOSIS runs).
- fig42_digitized.csv: measured I-V read from report Fig 4.2 (+-1.5 uA / +-5 mV).
- fit_schottky.py: physical fit (n >= 1): n 1.07, Rs 2575 ohm, Is 4.37e-11 A, rms 3.7 mV (Butler's own n = 0.43 model: 58 mV on this data).
- fit_tc.py: EG 0.439 eV (XTI 2) -> dV/dT -0.61 / -0.56 / -0.50 mV/C at 3 / 5 / 10 uA; measured -0.56 average.
- diode_check.sp: ngspice I-V within 1-2 uA of measured over 0.25-0.60 V.

## 2. Bandgap (Appendix A "Final Design Netlist", sizes in lambda 0.3 um), MOSFETs -> FP5 corners
| | Butler measured | FP5 tt | FP5 ff | FP5 ss |
|---|---|---|---|---|
| Supply current, 2.5 V, 25 C | 23.75 uA | 24.2 uA | 25.8 uA | 23.3 uA |
| Vref untrimmed (Rref 60k), 25 C | 0.251 V (part 1) .. ~0.40 (others, pre-trim spread) | 0.444 V | 0.444 V | 0.443 V |
| Rref for 0.400 V | 54.8 kohm (one part) | 54.0 kohm | 54.1 kohm | 54.2 kohm |
| Line: Vref 2.0 -> 3.0 V | ~0.397 -> 0.405 (Fig 4.7) | 0.441 -> 0.447 | | 0.438 -> 0.446 |
| Lowest working VDD | ~1.1 V (start-up toggled) | ~1.2 V | ~1.2 V | ~1.2 V |
| Vref TC 0-70 C (trimmed) | -107 / +214 / +286 / +500 ppm/C (4 parts) | see below | | |

TC depends on how the resistors are treated: Butler's R were external 1/8 W carbon-film parts (bgr_*.sp keep his
simulation assumption TC1 = +0.002 on-chip; the measured temperature set-up of the external resistors is not stated).
- all resistors in the chamber with TC1 = 0.002, Rref = external TC 0 (bgr_trim_*.sp): -861 (tt) / -874 (ff) / -694 (ss) ppm/C
- all resistors external at room temperature (bgr_ext_*.sp): +1226 (tt) / +1183 (ff) / +1403 (ss) ppm/C
The measured -107..+500 ppm/C lies inside this bracket. **Verdict:** current within 2 %, trim resistor within 1.5 %,
untrimmed Vref +11 % vs the trimmed target, supply range matches; TC cannot be pinned without the resistor thermal set-up.
