* Kerstetter UNLV EE420 2019 C5 rail-to-rail op-amp (BMR + bias + op-amp), transcribed from Fig 1/4/8.
* Model names are parameters: define .param-free via .subckt-level {N}/{P}: set with
*   Baker card: .include c5_baker.lib + N=NMOS P=PMOS ; FP5: .lib fp5.lib tt + N=fp5n P=fp5p
* (ngspice cannot parametrise model names, run.py text-substitutes {N}/{P}).
.param NL=0.6u NW=27u PL=0.6u PW=54u diff=10 out=125
.subckt bmr vdd vbiasp
MSU1 nsu nsu vdd vdd {P} w=1.2u l=200u m=1 as={1.2u*1.5u} ad={1.2u*1.5u} ps={2*1.2u+3u} pd={2*1.2u+3u}
MSU2 nsu n1 0 0 {N} w=200u l=1.2u m=1 as={200u*1.5u} ad={200u*1.5u} ps={2*200u+3u} pd={2*200u+3u}
MSU3 vbiasp nsu n1 n1 {N} w=65u l=1.2u m=1 as={65u*1.5u} ad={65u*1.5u} ps={2*65u+3u} pd={2*65u+3u}
M1 n1 vbiasp vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M2 n1 n1 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M3 n2 vbiasp vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M4 n2 n2 nr nr {N} w={NW} l={NL} m=4 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
RI nr 0 9.25k tc1=0.002
MA1 na na vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
MA3 vbiasp na vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
MA2 na n2 0 0 {N} w=12u l={NL} m=1 as={12u*1.5u} ad={12u*1.5u} ps={2*12u+3u} pd={2*12u+3u}
MA4 vbiasp n1 0 0 {N} w=12u l={NL} m=1 as={12u*1.5u} ad={12u*1.5u} ps={2*12u+3u} pd={2*12u+3u}
MCN vdd vbiasp vdd vdd {P} w=100u l=100u m=1 as={100u*1.5u} ad={100u*1.5u} ps={2*100u+3u} pd={2*100u+3u}
.ends bmr

.subckt bias vdd vbiasp vbias1 vbias2 vbias3 vbias4 vpcas vncas vlow vhigh
M5 vbias3 vbiasp vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M6 vbias3 vbias3 0 0 {N} w=50u l=2.4u m=1 as={50u*1.5u} ad={50u*1.5u} ps={2*50u+3u} pd={2*50u+3u}
M7 vbias4 vbiasp vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M8 vbias4 vbias3 vlow vlow {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M9 vlow vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M10 x10 x11 vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M11 x11 vbias2 x10 x10 {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M12 vpcas vpcas x11 x11 {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M13 vpcas vbias3 x13 x13 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M14 x13 vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M15 vbias2 vbias2 vdd vdd {P} w=121.5u l=2.9u m=1 as={121.5u*1.5u} ad={121.5u*1.5u} ps={2*121.5u+3u} pd={2*121.5u+3u}
M16 vbias2 vbias3 x16 x16 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M17 x16 vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M18 vhigh vbias1 vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M19 vbias1 vbias2 vhigh vhigh {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M20 vbias1 vbias3 x20 x20 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M21 x20 vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M22 x22 vbias1 vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M23 vncas vbias2 x22 x22 {P} w={PW} l={NL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M24 vncas vncas x24 x24 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M25 x24 vbias3 x25 x25 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M26 x25 x24 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
.ends bias

.subckt opamp vdd vp vm vout vbias1 vbias2 vbias3 vbias4 vpcas vncas
M2 al vm tn tn {N} w={NW*diff} l={NL} m=1 as={{NW*diff}*1.5u} ad={{NW*diff}*1.5u} ps={2*{NW*diff}+3u} pd={2*{NW*diff}+3u}
M3 ar vp tn tn {N} w={NW*diff} l={NL} m=1 as={{NW*diff}*1.5u} ad={{NW*diff}*1.5u} ps={2*{NW*diff}+3u} pd={2*{NW*diff}+3u}
M6 tn vbias3 t6 t6 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M7 t6 vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M4 tn vbias3 t4 t4 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M5 t4 vbias4 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M17 s17 vbias1 vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M19 tp vbias2 s17 s17 {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M18 s18 vbias1 vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M20 tp vbias2 s18 s18 {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M21 cl vm tp tp {P} w={PW*diff} l={PL} m=1 as={{PW*diff}*1.5u} ad={{PW*diff}*1.5u} ps={2*{PW*diff}+3u} pd={2*{PW*diff}+3u}
M22 cr vp tp tp {P} w={PW*diff} l={PL} m=1 as={{PW*diff}*1.5u} ad={{PW*diff}*1.5u} ps={2*{PW*diff}+3u} pd={2*{PW*diff}+3u}
M13 al bl vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M14 al bl vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M12 ar bl vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M1 ar bl vdd vdd {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M16 bl vbias2 al al {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
M15 br vbias2 ar ar {P} w={PW} l={PL} m=1 as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
MFCPL1 dl vpcas bl bl {P} w={PW/2} l={PL} m=1 as={{PW/2}*1.5u} ad={{PW/2}*1.5u} ps={2*{PW/2}+3u} pd={2*{PW/2}+3u}
MFCNL1 bl vncas dl dl {N} w={NW/2} l={NL} m=1 as={{NW/2}*1.5u} ad={{NW/2}*1.5u} ps={2*{NW/2}+3u} pd={2*{NW/2}+3u}
MFCPR1 dr vpcas br br {P} w={PW/2} l={PL} m=1 as={{PW/2}*1.5u} ad={{PW/2}*1.5u} ps={2*{PW/2}+3u} pd={2*{PW/2}+3u}
MFCNR1 br vncas dr dr {N} w={NW/2} l={NL} m=1 as={{NW/2}*1.5u} ad={{NW/2}*1.5u} ps={2*{NW/2}+3u} pd={2*{NW/2}+3u}
M10 dl vbias3 cl cl {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M8 dr vbias3 cr cr {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M11 cl dl 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M23 cl dl 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M9 cr dl 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
M24 cr dl 0 0 {N} w={NW} l={NL} m=1 as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
MOP1 vout br vdd vdd {P} w={PW} l={PL} m={out} as={{PW}*1.5u} ad={{PW}*1.5u} ps={2*{PW}+3u} pd={2*{PW}+3u}
MON1 vout dr 0 0 {N} w={NW} l={NL} m={out} as={{NW}*1.5u} ad={{NW}*1.5u} ps={2*{NW}+3u} pd={2*{NW}+3u}
Cc1 ar vout 6p
Cc2 vout xz 2p
Rz xz cr 30 tc1=0.002
.ends opamp
