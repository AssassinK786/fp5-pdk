# FP5A ngspice models

Use the PDK root environment variable:

```spice
.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5.lib" tt
.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5_passives.lib" devices
.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5_passives.lib" res_typ
```

Available MOS sections: `tt ff ss fs sf`. Available passive sections:
`devices`, `res_typ`, `res_low`, `res_high`.

Monte Carlo:

```spice
.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5_mc.lib" mm
.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5_mc.lib" mc_global
```

`fp5n_mm`/`fp5p_mm` draw local mismatch per instance. `fp5n_g`/`fp5p_g`
draw one global lot offset per run and share it across instances.

The corner cards `fp5_<corner>_cards.sp` are flat BSIM3 models for tools that
cannot use `.lib` sections. The `fp5.lib` file is the normal entry point.
