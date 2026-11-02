#!/bin/bash
# Run LibreLane against the in-tree FP5A PDK.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PDK_ROOT=${PDK_ROOT:-$ROOT}
PDK=${PDK:-fp5A}
if [ -n "${FP5_PDN_CFG:-}" ]; then
    PDN_CFG=$FP5_PDN_CFG
elif [ -f "$PDK_ROOT/$PDK/libs.tech/librelane/pdn_cfg_ring.tcl" ]; then
    PDN_CFG=$PDK_ROOT/$PDK/libs.tech/librelane/pdn_cfg_ring.tcl
else
    PDN_CFG=$ROOT/fp5A/libs.tech/librelane/pdn_cfg_ring.tcl
fi
exec librelane \
    --manual-pdk \
    --pdk-root "$PDK_ROOT" \
    -p "$PDK" \
    --skip Odb.CheckDesignAntennaProperties \
    --override-config "PDN_CFG=$PDN_CFG" \
    "$@"
