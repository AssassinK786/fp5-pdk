* FP5 tie cells (research PDK): INVX1 with the gate strapped to a rail in metal1
.subckt TIEHI Y vdd gnd
M0 Y gnd vdd vdd pfet w=6u l=0.6u
M1 Y gnd gnd gnd nfet w=3u l=0.6u
.ends TIEHI
.subckt TIELO Y vdd gnd
M0 Y vdd vdd vdd pfet w=6u l=0.6u
M1 Y vdd gnd gnd nfet w=3u l=0.6u
.ends TIELO
