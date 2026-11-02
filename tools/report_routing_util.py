#!/usr/bin/env python3
"""Report FP5A LibreLane routing-utilization metrics for the latest run."""
import argparse
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def latest_run():
    runs = sorted(glob.glob(os.path.join(ROOT, "examples/librelane/cnt8/runs/RUN_*")))
    runs = [r for r in runs if os.path.isfile(os.path.join(r, "final/metrics.json"))]
    if not runs:
        raise SystemExit("no completed LibreLane run found; run `make smoke` first")
    return runs[-1]


def count_cells(def_path, cell):
    if not os.path.isfile(def_path):
        return None
    text = open(def_path, encoding="utf8").read()
    return len(re.findall(r"^\s*-\s+\S+\s+" + re.escape(cell) + r"\s+", text, re.M))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", nargs="?", default=None, help="RUN directory")
    args = ap.parse_args()
    run = args.run or latest_run()
    metrics_path = os.path.join(run, "final/metrics.json")
    if not os.path.isfile(metrics_path):
        raise SystemExit(f"missing {metrics_path}")
    m = json.load(open(metrics_path, encoding="utf8"))
    core = m.get("design__core__area")
    wire = m.get("route__wirelength")
    ratio = (wire / core) if core and wire else None
    print(f"run                     {os.path.basename(run)}")
    print(f"core area (um^2)        {core}")
    print(f"routed wirelength (um)  {wire}")
    print(f"wirelength/core (1/um)  {ratio:.4f}" if ratio else "wirelength/core         n/a")
    print(f"route DRC errors        {m.get('route__drc_errors')}")
    print(f"KLayout DRC errors      {m.get('klayout__drc_error_count', m.get('klayout__drc_error__count'))}")
    print(f"power-grid violations   {m.get('design__power_grid_violation__count')}")
    print(f"setup / hold WNS        {m.get('timing__setup__wns')} / {m.get('timing__hold__wns')}")
    print(f"vdd / gnd worst drop    {m.get('design_powergrid__drop__worst__net:vdd__corner:nom_tt_5v00_25c')} / {m.get('design_powergrid__drop__worst__net:gnd__corner:nom_tt_5v00_25c')} V")
    def_path = os.path.join(run, "final/def/cnt8.def")
    for cell in ("TAP", "ENDCAP", "DECAP", "FILL"):
        print(f"{cell:<8} count          {count_cells(def_path, cell)}")


if __name__ == "__main__":
    main()
