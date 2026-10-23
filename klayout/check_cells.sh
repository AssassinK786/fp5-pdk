#!/bin/bash
# PERSONAL USE. Run FP5 DRC + LVS on every OSU 0.5 um cell in digital/gds/osu05_stdcells.gds2.
cd ~/pdks/fp5; O=klayout/cell_checks; mkdir -p $O
G=$PWD/digital/gds/osu05_stdcells.gds2; S=$PWD/digital/spice/fp5_osu_cells.sp
cells=$(python3 -c "import klayout.db as d; l=d.Layout(); l.read('$G'); print(' '.join(c.name for c in l.each_cell() if not c.is_top()))")
nd=0; nl=0; n=0
for c in $cells; do n=$((n+1))
  klayout -b -r klayout/fp5.drc -rd input=$G -rd top=$c -rd report=$O/${c}_drc.lyrdb > $O/${c}_drc.log 2>&1
  d=$(grep -c "<item>" $O/${c}_drc.lyrdb 2>/dev/null); d=${d:-0}
  if grep -q "\.subckt $c\b\|\.SUBCKT $c\b" -i $S; then
    klayout -b -r klayout/fp5.lvs -rd input=$G -rd schematic=$S -rd top=$c -rd report=$O/${c}.lvsdb > $O/${c}_lvs.log 2>&1
    grep -q "LVS MATCH" $O/${c}_lvs.log && l=MATCH || l=MISMATCH
  else l=noschem; fi
  [ "$d" != 0 ] && nd=$((nd+1)); [ "$l" = MISMATCH ] && nl=$((nl+1))
  echo "$c DRC=$d LVS=$l"
done | tee $O/summary.txt
echo "cells=$(wc -l < $O/summary.txt) drc_fail=$(grep -vc 'DRC=0 ' $O/summary.txt) lvs_mismatch=$(grep -c MISMATCH $O/summary.txt) noschem=$(grep -c noschem $O/summary.txt)" | tee -a $O/summary.txt
