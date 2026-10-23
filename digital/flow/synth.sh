#!/bin/bash
# usage: synth.sh TOP out_dir rtl.v [more.v ...]   -> out_dir/TOP.v  (Yosys 0.62, fp5 OSU cells, tt 5 V)
set -e; . "$(dirname "$0")/env.sh"; TOP=$1; OUT=$2; shift 2; mkdir -p $OUT
~/.local/bin/yosys-0.62 -q -l $OUT/$TOP.synth.log -p "read_verilog $*; synth -top $TOP -flatten; dfflibmap -liberty $FP5_LIB; abc -liberty $FP5_LIB; setundef -zero; opt_clean -purge; hilomap -singleton -hicell TIEHI Y -locell TIELO Y; opt_clean -purge; stat -liberty $FP5_LIB; write_verilog -noattr $OUT/$TOP.v"
grep -E 'Chip area' $OUT/$TOP.synth.log | tail -1
