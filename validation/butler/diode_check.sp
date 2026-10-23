* FP5 Schottky check vs Butler Fig 4.2 / measured TC
.lib /home/fpga/pdks/fp5/passives/fp5_passives.lib devices
V1 a 0 0
D1 a 0 fp5_schottky
.control
set wr_singlescale
dc V1 0.25 0.6 0.025
wrdata iv25.txt -i(V1)
foreach t 0 70
  set temp=$t
  op
end
.endc
.end
