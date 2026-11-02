#!/bin/bash
# Lightweight local validation for the FP5A PDK tree.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PDK=${PDK:-fp5A}
SCL=${SCL:-fp5_osu}
P=$ROOT/$PDK
TMP=${TMPDIR:-/tmp}/fp5a_check
mkdir -p "$TMP"
fail=0

check_file() { [ -s "$1" ] || { echo "MISSING $1"; fail=1; }; }
for f in \
  "$P/libs.tech/librelane/config.tcl" \
  "$P/libs.tech/librelane/$SCL/config.tcl" \
  "$P/libs.tech/klayout/drc/$PDK.drc" \
  "$P/libs.tech/klayout/lvs/$PDK.lvs" \
  "$P/libs.tech/klayout/tech/$PDK.lyt" \
  "$P/libs.tech/klayout/tech/$PDK.lyp" \
  "$P/libs.tech/klayout/tech/$PDK.map" \
  "$P/libs.tech/klayout/pex/$PDK.rcx" \
  "$P/libs.tech/magic/$PDK.tech" \
  "$P/libs.tech/netgen/${PDK}_setup.tcl" \
  "$P/libs.ref/fp5_osu/gds/fp5_osu.gds" \
  "$P/libs.ref/fp5_osu/lef/fp5_osu.lef" \
  "$P/libs.ref/fp5_osu/techlef/fp5_osu_tech.lef" \
  "$P/libs.ref/fp5_osu/lib/fp5_osu__tt_5v00_25c.lib" \
  "$P/libs.ref/fp5_osu/spice/fp5_osu_cells.spice" \
  "$P/libs.ref/fp5_osu/verilog/fp5_osu.v"; do
  check_file "$f"
done

if [ "$fail" -ne 0 ]; then exit 1; fi

G=$P/libs.ref/fp5_osu/gds/fp5_osu.gds
S=$P/libs.ref/fp5_osu/spice/fp5_osu_cells.spice
echo "== KLayout DRC NAND2X1"
klayout -b -zz -r "$P/libs.tech/klayout/drc/$PDK.drc" \
  -rd input="$G" -rd topcell=NAND2X1 -rd report="$TMP/nand2.drc.lyrdb" \
  > "$TMP/nand2.drc.log" 2>&1
items=$(grep -c '<item>' "$TMP/nand2.drc.lyrdb" 2>/dev/null || true)
echo "DRC items: ${items:-report-missing}"
[ "${items:-1}" = "0" ] || fail=1

for cell in TAP DECAP ENDCAP; do
  echo "== KLayout DRC $cell"
  klayout -b -zz -r "$P/libs.tech/klayout/drc/$PDK.drc" \
    -rd input="$P/libs.ref/fp5_osu/gds/fp5_physical.gds" \
    -rd topcell=$cell -rd report="$TMP/$cell.drc.lyrdb" \
    > "$TMP/$cell.drc.log" 2>&1
  items=$(grep -c '<item>' "$TMP/$cell.drc.lyrdb" 2>/dev/null || true)
  echo "DRC items: ${items:-report-missing}"
  [ "${items:-1}" = "0" ] || fail=1
done

echo "== KLayout LVS NAND2X1"
klayout -b -zz -r "$P/libs.tech/klayout/lvs/$PDK.lvs" \
  -rd input="$G" -rd schematic="$S" -rd topcell=NAND2X1 \
  -rd report="$TMP/nand2.lvsdb" > "$TMP/nand2.lvs.log" 2>&1
grep -q "LVS MATCH" "$TMP/nand2.lvs.log" || { echo "LVS failed"; fail=1; }

echo "== ngspice model sanity"
cat > "$TMP/dev.sp" <<SPICE
.lib "$P/libs.tech/ngspice/fp5.lib" tt
M1 d g 0 0 fp5n W=15u L=0.6u
Vd d 0 5
Vg g 0 5
.control
op
print i(Vd)
.endc
.end
SPICE
ngspice -b "$TMP/dev.sp" > "$TMP/dev.log" 2>&1
id=$(grep -oE 'i\(vd\) = [-0-9.eE+]+' "$TMP/dev.log" | tail -1 | awk '{print $3}')
echo "NMOS Idss (A) = ${id:-missing}"
[ -n "${id:-}" ] || fail=1

if [ "$fail" -ne 0 ]; then
  echo "FP5A check FAILED"
  exit 1
fi
echo "FP5A check PASSED"
