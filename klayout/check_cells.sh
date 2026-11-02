#!/bin/bash
# Run FP5A DRC + LVS on every OSU macro in the new reference library.
# Reports are written to absolute paths so KLayout cannot silently drop them.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
P=$ROOT/fp5A
O=$ROOT/klayout/cell_checks
G=$P/libs.ref/fp5_osu/gds/fp5_osu.gds
GT=$P/libs.ref/fp5_osu/gds/fp5_tiecells.gds
GP=$P/libs.ref/fp5_osu/gds/fp5_physical.gds
S=$P/libs.ref/fp5_osu/spice/fp5_osu_cells.spice
ST=$P/libs.ref/fp5_osu/spice/fp5_tiecells.spice
SP=$P/libs.ref/fp5_osu/spice/fp5_physical.spice
mkdir -p "$O"

cells=$(awk '/^MACRO /{print $2}' "$P/libs.ref/fp5_osu/lef/fp5_osu.lef")
nd=0; nl=0; n=0; missing=0
: > "$O/summary.txt"
for c in $cells; do
  n=$((n+1))
  case "$c" in TIEHI|TIELO) gg=$GT; ss=$ST;; TAP|DECAP|ENDCAP) gg=$GP; ss=$SP;; *) gg=$G; ss=$S;; esac
  drc_rep=$O/${c}_drc.lyrdb
  rm -f "$drc_rep"
  klayout -b -zz -r "$P/libs.tech/klayout/drc/fp5A.drc" \
    -rd input="$gg" -rd top="$c" -rd report="$drc_rep" \
    > "$O/${c}_drc.log" 2>&1
  if [ ! -f "$drc_rep" ]; then
    d=NA; missing=$((missing+1))
  else
    d=$(grep -c "<item>" "$drc_rep" 2>/dev/null || true); d=${d:-0}
  fi

  if grep -qiE "^\.subckt $c\b" "$ss"; then
    lvs_rep=$O/${c}.lvsdb
    klayout -b -zz -r "$P/libs.tech/klayout/lvs/fp5A.lvs" \
      -rd input="$gg" -rd schematic="$ss" -rd top="$c" -rd report="$lvs_rep" \
      > "$O/${c}_lvs.log" 2>&1
    if grep -q "LVS MATCH" "$O/${c}_lvs.log"; then l=MATCH; else l=MISMATCH; nl=$((nl+1)); fi
  else
    l=noschem
  fi
  [ "$d" != "0" ] && nd=$((nd+1))
  echo "$c DRC=$d LVS=$l" | tee -a "$O/summary.txt"
done
echo "cells=$n drc_fail=$nd lvs_mismatch=$nl missing_reports=$missing" | tee -a "$O/summary.txt"
[ "$nd" -eq 0 ] && [ "$nl" -eq 0 ] && [ "$missing" -eq 0 ]
