#!/bin/bash
# usage: synth.sh TOP out_dir rtl.v [more.v ...]   -> out_dir/TOP.v
# Uses the Yosys on PATH unless YOSYS is set.
set -e
. "$(dirname "$0")/env.sh"
TOP=$1; OUT=$2; shift 2; mkdir -p "$OUT"
YOSYS=${YOSYS:-yosys}
"$YOSYS" -q -l "$OUT/$TOP.synth.log" -p "read_verilog $*; synth -top $TOP -flatten; dfflibmap -liberty $FP5_LIB; abc -liberty $FP5_LIB; setundef -zero; opt_clean -purge; hilomap -singleton -hicell TIEHI Y -locell TIELO Y; opt_clean -purge; stat -liberty $FP5_LIB; write_verilog -noattr $OUT/$TOP.v"
grep -E 'Chip area' "$OUT/$TOP.synth.log" | tail -1
