* Butler 2005 low-voltage Schottky BGR (Appendix A "Final Design Netlist") on FP5 (PERSONAL USE)
* Topology, sizes (lambda, scale 0.3u) and resistors exactly as published; MOSFET models T4BP -> FP5 tt/ff/ss,
* SCHOTTKY -> fp5_schottky, RMODEL kept as published (TC1 = 0.002).
.option scale=0.3u
.lib /home/fpga/pdks/fp5/models/fp5.lib tt
.lib /home/fpga/pdks/fp5/passives/fp5_passives.lib devices
.model RMODEL R TC1=0.002
VDD VDD 0 DC 2.5
M1 V1 Vbs VDD VDD fp5p L=2 W=30
M2 V1 Vbs 0 0 fp5n L=100 W=10
M3 V2 V1 VDD VDD fp5p L=2 W=12
M4 V2 Vbs VDD VDD fp5p L=2 W=30
M5 Vbs V4 VDD VDD fp5p L=2 W=30
M6 V4 V4 VDD VDD fp5p L=2 W=30
M7 Vbs V2 V3 0 fp5n L=2 W=15
M8 V4 V5 V3 0 fp5n L=2 W=10
M9 V3 V4 0 0 fp5n L=2 W=20
M10 V5 Vbs VDD VDD fp5p L=2 W=30
M11 Vrf Vbs VDD VDD fp5p L=2 W=30
R1 V2 0 172k RMODEL
R2 V5 V6 22k RMODEL
R3 V5 0 172k RMODEL
R4 Vrf 0 53993
* R4 = external trimmed Rref (TC 0)
D1 V2 0 fp5_schottky
D2 V6 0 fp5_schottky 8
* start-up: Butler toggled an external start-up in at ~1.1 V; here a nodeset starts the loop
.nodeset v(Vbs)=1.0 v(V4)=1.6
.control
set wr_singlescale
foreach t 0 25 70
  set temp=$t
  op
  print v(vrf)
  print i(vdd)
end
set temp=25


.endc
.end
