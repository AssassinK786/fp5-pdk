# Kerstetter C5 rail-to-rail op-amp on FP5 (PERSONAL USE, do not git commit)

Source: J. Kerstetter, UNLV EE420 course project (2019), `~/ext/cmosedu/kerstetter420courseProject.pdf`
(Fig 1 BMR + start-up, Fig 4 bias circuit, Fig 8 op-amp; Tables 2 and 3).

Files:
- `kerstetter_opamp.sp`: subcircuits `bmr`, `bias`, `opamp`. The model names are `{N}`/`{P}` placeholders.
- `run.py`: fills in the placeholders (Baker C5 card `NMOS/PMOS`, or FP5 `fp5n/fp5p` with `.lib fp5.lib tt|ff|ss`), writes `runs/*.sp`, runs ngspice and writes `results.txt`.
- Test bench: VCM = Vp = VDD/2 (AC 1 V), Vout fed back to Vm through 1 GH with 1 F to ground (DC servo, open loop in AC).
  PM = 180 deg + phase(Vout) at 0 dB. Junction geometry AS = AD = W*1.5u, PS = PD = 2W+3u. T = 27 C.

## Results (27 C; PMOS bias voltages given as VDD - V, the way Table 3 gives them)

| Quantity | Kerstetter 2V / 5V | Baker card 2V / 5V | FP5 tt 2V / 5V | FP5 ff 2V / 5V | FP5 ss 2V / 5V |
|---|---|---|---|---|---|
| DC gain, no load (dB) | 89.27 / 82.36 | 88.77 / 81.74 | 89.41 / 85.75 | 87.41 / 84.05 | 92.12 / 87.43 |
| UGF, no load (MHz) | 3.98 / 4.49 | 5.02 / 5.32 | 5.25 / 5.45 | 5.19 / 5.45 | 5.28 / 5.47 |
| PM, no load (deg) | 95 / 89.24 | 79.1 / 89.1 | 82.4 / 89.3 | 83.2 / 89.3 | 80.2 / 89.2 |
| DC gain, 1k\|\|100p (dB) | 83.20 / 78.3 | 82.35 / 76.92 | 83.26 / 80.76 | 81.36 / 79.05 | 85.99 / 82.40 |
| UGF, 1k\|\|100p (MHz) | 3.43 / 3.86 | 4.32 / 4.73 | 4.83 / 5.06 | 4.82 / 5.10 | 4.84 / 5.03 |
| PM, 1k\|\|100p (deg) | 107.48 / 98.33 | 67.9 / 80.2 | 72.1 / 80.7 | 73.5 / 81.1 | 69.3 / 80.1 |
| I(VDD) quiescent, no load (uA) | 65.5 / 81.54 | 1137 / 2696 | 1290 / 2529 | 1345 / 2701 | 1205 / 2376 |
| Vbias1 (VDD-V) | 0.912 / 0.917 | 0.924 / 0.928 | 0.925 / 0.929 | 0.881 / 0.885 | 0.970 / 0.974 |
| Vbias2 (VDD-V) | 0.994 / 1.000 | 1.008 / 1.013 | 1.016 / 1.021 | 0.965 / 0.970 | 1.067 / 1.072 |
| Vbias3 | 0.775 / 0.778 | 0.786 / 0.789 | 0.785 / 0.788 | 0.709 / 0.712 | 0.861 / 0.864 |
| Vbias4 | 0.663 / 0.666 | 0.672 / 0.674 | 0.681 / 0.682 | 0.607 / 0.608 | 0.754 / 0.755 |
| Vpcas (VDD-V) | 1.801 / 1.812 | 1.823 / 1.836 | 1.827 / 1.839 | 1.739 / 1.749 | 1.904 / 1.929 |
| Vncas | 1.449 / 1.464 | 1.329 / 1.343 | 1.344 / 1.356 | 1.199 / 1.211 | 1.489 / 1.501 |
| Vlow | 0.100 / 0.101 | 0.127 / 0.128 | 0.120 / 0.121 | 0.117 / 0.117 | 0.124 / 0.125 |
| Vhigh (VDD-V) | 0.100 / 0.101 | 0.103 / 0.103 | 0.107 / 0.108 | 0.102 / 0.103 | 0.113 / 0.114 |

The loaded-case current (with Vout = VDD/2 driving 1 mA into the 1k load) is in `results.txt`.

## Is the transcription right? (Baker card vs Kerstetter)
- Bias voltages: Vbias1 to 4, Vpcas and Vhigh are within 1.5 %. Vncas is 8 % low. Vlow is 0.127 V against 0.100 V; it is a small number, and M6 is set to w=50u as the figure reads.
- DC gain is within 0.6 dB with no load and within 1.4 dB with the load.
- UGF is 18 to 26 % high and PM is 10 to 40 deg low. This is at or a little past the agreed 10 to 20 % tolerance.
- The quiescent current is about 17x what Table 2 says. This does not look like a transcription error. The BMR and bias circuit alone draw 54 uA (16.6 + 37 uA). The four input-pair tails draw another 24 uA. So 65.5 uA total cannot be reached before the output stage is counted. The class-AB output (MOP1/MON1, m=125) carries about 1.05 mA, which is what you expect from m=125 times the roughly 8 uA set by the floating current sources. Table 2 probably measured some other branch or a different version of the schematic.
- The FP5 corners follow the Baker reproduction closely. tt is within 0.6 dB (2 V) and 4 dB (5 V) of the Baker gain. ss gives the highest gain, ff the lowest. UGF hardly moves (5.2 to 5.5 MHz), and PM is 69 to 89 deg at every corner.

## Assumptions and items I could not read for certain
1. Bulk connections: Kerstetter draws every NMOS with the 3-terminal LTspice symbol, which ties bulk to source, and draws every PMOS with bulk strapped to source. I kept this exactly, on FP5 too. This is not realistic in a p-substrate process: there, NMOS bulk would go to 0. MOP1 and MCN have bulk at VDD.
2. Rz reads "30 TC1=0.002", so I took it as 30 ohm. I tried 30k and it makes things worse (UGF 6.8 MHz).
3. M6 reads l=2.4u w=50u in Fig 4. The task brief said w=30u; I used the figure.
4. M23 in the bias circuit is drawn as a PMOS with l=NL w=PW. Both values are 0.6u, so the size does not change.
5. In Fig 8 the gates of M13/M14/M12/M1 go to the M16 drain (bl), and the gates of M11/M23/M9/M24 go to the M10 drain (dl). This is the wide-swing self-biased mirror. Cc1 goes from the M12/M1 drain node to Vout. Cc2 + Rz go from Vout to the M9/M24 drain node.
6. The floating current sources are MFCPx w=PW/2 and MFCNx w=NW/2. The output stage is MOP1 PMOS w=PW m=125 and MON1 NMOS w=NW m=125. The input pairs are w=NW*10 and w=PW*10.
7. In Fig 1, M2 and M4 are each diode-connected. The cross-coupled MA2/MA4 amplifier (gate of MA4 = M2 node, gate of MA2 = M4 node, with an MA1 diode load) drives Vbiasp. M4 has m=4 and RI = 9.25k with tc1=0.002. MCN is a 100u/100u PMOS decap.
8. Resistors are ideal with tc1. The FP5 passives were not used. There is no `.options scale`: the sizes are taken as physical (0.6 um L).
9. The no-load phase-margin difference may come from how Kerstetter measured PM (closed-loop or his own test bench); his method is not stated.
