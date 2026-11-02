# Sources and provenance

FP5A is built from public data only. No confidential AMI C5X material is used.

## Process and device models

- MOSIS parametric reports for the AMI/onsemi C5 0.5 um process (105 lots;
  T89Y is the typical lot). Public course copies and Wayback snapshots.
- Baker, *CMOS Circuit Design, Layout, and Simulation* - public C5 model card
  used as a cross-check.
- MOSIS SCMOS design rules, as encoded in the public qflow
  `SCN3ME_SUBM.30.tech` Magic technology (lambda = 0.30 um).
- onsemi C5 datasheet and the public AMI500 databook for process summaries.

## Standard cells

- OSU 0.5 um standard-cell library from the qflow project
  (`osu050_stdcells.lef`, `osu05_stdcells.gds2`, `osu05_stdcells.lib`,
  `osu050_stdcells.sp`, `osu05_stdcells.v`).
  The OSU/qflow files retain their original copyright and license terms.
- FP5 re-characterization of the OSU Liberty views; TIEHI/TIELO cells added.
- FP5 DRC/LVS checks use KLayout 0.30.x.

## Validation references

- Kerstetter, UNLV EE420 course project (2019), C5 rail-to-rail op-amp.
- Butler, Boise State MS report (2005), low-voltage Schottky bandgap;
  digitized measured data in `validation/butler/fig42_digitized.csv`.
- MOSIS T89Y ring-oscillator measurements.

## Build-time data

Two build scripts expect data that is not redistributed here:

- `models/build_corners.py` needs the gatearray comparison helper via
  `FP5_BUILD_HELPER`.
- `passives/extract_passives.py` needs the MOSIS parameter extracts via
  `FP5_MOSIS_PARAMS`.

The checked-in model and passive files are the released outputs; the scripts
are not required to use the PDK.

## License notes

Original FP5A work: Apache-2.0. OSU/qflow material: see the qflow project.
Public MOSIS reports and papers are cited, not redistributed, except for the
small digitized measurement table noted above.
