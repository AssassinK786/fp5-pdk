# FP5 KLayout files
- layers.txt: GDS layer numbers (MOSIS SCMOS numbering, as used by the OSU 0.5 um cells and the qflow Magic tech).
- fp5.drc: DRC deck, public MOSIS SCMOS SUBM rules at lambda 0.30 um (widths, spacings, enclosures, gate extension,
  select, contacts, metal1-3, vias, poly2). Run: klayout -b -r fp5.drc -rd input=x.gds -rd report=x.lyrdb
- Not included: antenna, density, latch-up spacing, pad rules; LVS (not yet).
