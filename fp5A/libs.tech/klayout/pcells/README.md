# FP5A KLayout PCells

Load `fp5_pcells.py` in KLayout (Macros > run file, or install as a
pymacro).  Library name: `FP5`.

Cells: `nmos`, `pmos`, `rpoly`, `rpoly2`, `rhr`, `cpoly`, `gring`.
The `rpoly2` and `rhr` cells use poly2/p2con and (for `rhr`) the `hires`
marker layer.  The PCells follow the public SCMOS SUBM 0.30 um rules checked
by `../fp5A.drc`.
