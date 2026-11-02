# FP5 digital flow environment (source me)
# Works from any checkout: the PDK root is inferred, not hard-coded.
FP5_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
export FP5PDK=${FP5PDK:-$FP5_ROOT}
export FP5_LIB=$FP5PDK/fp5A/libs.ref/fp5_osu/lib/fp5_osu__tt_5v00_25c.lib
export FP5_LEF=$FP5PDK/fp5A/libs.ref/fp5_osu/lef/fp5_osu.lef
export FP5_TECH_LEF=$FP5PDK/fp5A/libs.ref/fp5_osu/techlef/fp5_osu_tech.lef
