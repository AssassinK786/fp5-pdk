#!/usr/bin/env python3
"""Derive FS and SF Liberty views for the FP5A OSU library.

The full cell set was characterized once by an external 'recharz' script that
is not in this repo, so a from-scratch per-cell rechar isn't reproducible.
This script instead measures the delay *ratio* of a canonical reference cell
(INVX1, fan-out-1, mid slew/load point) in ngspice at the fs and sf corners vs
tt, and produces fs/sf .lib files by scaling every delay/transition/power
table in the existing TT lib by that ratio.  Leakage is scaled by the
transistor drive ratio.  This is the documented, honest approximation for a
research PDK: absolute numbers are corner-consistent, table *shape* is kept
from the measured tt characterization.

Output: digital/lib/fp5_osu_fs_5v.lib and fp5_osu_sf_5v.lib plus a report.
"""
import os, re, subprocess, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIB  = os.path.join(ROOT, "fp5A", "libs.tech", "ngspice", "fp5.lib")
CELLS= os.path.join(ROOT, "digital", "spice", "fp5_osu_cells.sp")
TT   = os.path.join(ROOT, "digital", "lib", "fp5_osu_tt_5v.lib")
OUTD = os.path.join(ROOT, "digital", "lib")

VDD = 5.0
# mid characterization point (index_1 slew, index_2 load) matching the lib grid
SLEW, LOAD = 0.1, 0.36

def inv_delay(corner, sense):
    """50%-50% delay of INVX1 driving its own input cap (FO1)."""
    lo, hi = (0, VDD) if sense == "rise" else (VDD, 0)
    # build the canonical inverter from fp5n/fp5p directly (INVX1 sizing:
    # pfet 6u / nfet 3u).  The OSU cell netlists can't be included because
    # they instantiate nfet/pfet which ngspice scopes per-subckt.
    deck = f"""* INVX1-equivalent FO1 delay, corner {corner}
.lib "{LIB}" {corner}
* driver inverter (a -> n1)
Mpd n1 a vdd vdd fp5p W=6u L=0.6u
Mnd n1 a 0 0   fp5n W=3u L=0.6u
* DUT inverter (n1 -> y), input is the measured node
Mpu y n1 vdd vdd fp5p W=6u L=0.6u
Mnu y n1 0 0   fp5n W=3u L=0.6u
* load inverter on y (fanout 1)
Mpl nl y vdd vdd fp5p W=6u L=0.6u
Mnl nl y 0 0   fp5n W=3u L=0.6u
Vdd vdd 0 DC {VDD}
* input edge at t=1n: start = {lo}, end = {hi}
Vin a 0 DC {lo} PWL(0 {lo} 1n {lo} 1.001n {hi})
.control
tran 1p 10n
meas tran tdelay trig v(a) val={VDD/2} {'rise' if sense=='rise' else 'fall'}=1
+                  targ v(n1) val={VDD/2} {'fall' if sense=='rise' else 'rise'}=1
.endc
.end
"""
    with tempfile.TemporaryDirectory() as td:
        open(f"{td}/d.sp", "w").write(deck)
        o = subprocess.run(["ngspice", "-b", "d.sp"], cwd=td,
                           capture_output=True, text=True).stdout
    m = re.findall(r"tdelay\s*=\s*([-0-9.eE+]+)", o)
    if not m:
        raise RuntimeError(f"no delay for {corner}/{sense}:\n{o[-1200:]}")
    return float(m[-1])

def ratio(corner):
    dr = inv_delay(corner, "rise") / inv_delay("tt", "rise")
    df = inv_delay(corner, "fall") / inv_delay("tt", "fall")
    r = (dr + df) / 2
    print(f"  {corner}: rise {dr:.3f} fall {df:.3f} -> scale {r:.3f}")
    return r

def scale_lib(src, factor, corner_name, out_path):
    """Scale every numeric value inside values()/leakage/capacitance is left
    alone (caps are geometric); only delay/transition/power tables + leakage
    get the factor.  Simplest consistent rule for a lookup lib: scale all
    numbers inside `values (` blocks and `cell_leakage_power`."""
    txt = open(src).read()
    # scale values ( "a,b,c", ... )  blocks
    def scale_values(m):
        body = m.group(0)
        nums = re.sub(r"(-?\d+\.?\d*(?:[eE][+-]?\d+)?)",
                      lambda n: f"{float(n.group(1)) * factor:.6g}", body)
        return nums
    txt = re.sub(r'values \([^;]+\);', scale_values, txt, flags=re.S)
    # scale leakage power
    txt = re.sub(r"(cell_leakage_power\s*:\s*)([-0-9.eE+]+)",
                 lambda m: m.group(1) + f"{float(m.group(2)) * factor:.6g}", txt)
    # header: retitle + fix corner voltage metadata
    txt = txt.replace("fp5_osu_tt_5v", f"fp5_osu_{corner_name}_5v")
    header = f"/* {corner_name.upper()} corner (5.0 V, 25 C): delay/power = tt x {factor:.4f}, derived by digital/char_corners.py */\n"
    txt = header + txt
    open(out_path, "w").write(txt)
    print(f"  wrote {out_path}")

def main():
    print("reference INVX1 FO1 delays:")
    factors = {c: ratio(c) for c in ("fs", "sf")}
    for c, f in factors.items():
        scale_lib(TT, f, c, os.path.join(OUTD, f"fp5_osu_{c}_5v.lib"))
    print("\nNote: these are derated views (uniform scale), suitable for corner")
    print("sensitivity checks, NOT full re-characterization. See char_corners.py.")

if __name__ == "__main__":
    main()
