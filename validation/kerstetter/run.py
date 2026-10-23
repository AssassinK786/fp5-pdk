#!/usr/bin/env python3
"""Kerstetter EE420 (2019) C5 rail-to-rail op-amp: netlist generator + runner.
PERSONAL USE (FP5). Usage: python3 run.py  -> writes kerstetter_opamp.sp, decks in runs/, results.txt"""
import subprocess, re, os, itertools
D=os.path.dirname(os.path.abspath(__file__)); os.makedirs(D+'/runs',exist_ok=True)

def M(name,d,g,s,b,typ,w,l,m=1):
    # typ 'n'/'p'; model names via {N}/{P} placeholders; junction geometry W*1.5u
    return (f"{name} {d} {g} {s} {b} {{{typ.upper()}}} w={w} l={l} m={m} "
            f"as={{{w}*1.5u}} ad={{{w}*1.5u}} ps={{2*{w}+3u}} pd={{2*{w}+3u}}")

NW,NL,PW,PL='{NW}','{NL}','{PW}','{PL}'
# LTspice 3-terminal nmos/pmos symbols tie bulk to source; Kerstetter's NMOS are all 3-terminal,
# PMOS are drawn with bulk strapped to source. MCN (decap) bulk = VDD.
bmr=[".subckt bmr vdd vbiasp",
 M('MSU1','nsu','nsu','vdd','vdd','p','1.2u','200u'),
 M('MSU2','nsu','n1','0','0','n','200u','1.2u'),
 M('MSU3','vbiasp','nsu','n1','n1','n','65u','1.2u'),
 M('M1','n1','vbiasp','vdd','vdd','p',PW,PL),
 M('M2','n1','n1','0','0','n',NW,NL),
 M('M3','n2','vbiasp','vdd','vdd','p',PW,PL),
 M('M4','n2','n2','nr','nr','n',NW,NL,4),
 "RI nr 0 9.25k tc1=0.002",
 M('MA1','na','na','vdd','vdd','p',PW,PL),
 M('MA3','vbiasp','na','vdd','vdd','p',PW,PL),
 M('MA2','na','n2','0','0','n','12u',NL),
 M('MA4','vbiasp','n1','0','0','n','12u',NL),
 M('MCN','vdd','vbiasp','vdd','vdd','p','100u','100u'),
 ".ends bmr"]
bias=[".subckt bias vdd vbiasp vbias1 vbias2 vbias3 vbias4 vpcas vncas vlow vhigh",
 M('M5','vbias3','vbiasp','vdd','vdd','p',PW,PL),
 M('M6','vbias3','vbias3','0','0','n','50u','2.4u'),
 M('M7','vbias4','vbiasp','vdd','vdd','p',PW,PL),
 M('M8','vbias4','vbias3','vlow','vlow','n',NW,NL),
 M('M9','vlow','vbias4','0','0','n',NW,NL),
 M('M10','x10','x11','vdd','vdd','p',PW,PL),
 M('M11','x11','vbias2','x10','x10','p',PW,PL),
 M('M12','vpcas','vpcas','x11','x11','p',PW,PL),
 M('M13','vpcas','vbias3','x13','x13','n',NW,NL),
 M('M14','x13','vbias4','0','0','n',NW,NL),
 M('M15','vbias2','vbias2','vdd','vdd','p','121.5u','2.9u'),
 M('M16','vbias2','vbias3','x16','x16','n',NW,NL),
 M('M17','x16','vbias4','0','0','n',NW,NL),
 M('M18','vhigh','vbias1','vdd','vdd','p',PW,PL),
 M('M19','vbias1','vbias2','vhigh','vhigh','p',PW,PL),
 M('M20','vbias1','vbias3','x20','x20','n',NW,NL),
 M('M21','x20','vbias4','0','0','n',NW,NL),
 M('M22','x22','vbias1','vdd','vdd','p',PW,PL),
 M('M23','vncas','vbias2','x22','x22','p',PW,NL),   # drawn l=NL w=PW
 M('M24','vncas','vncas','x24','x24','n',NW,NL),
 M('M25','x24','vbias3','x25','x25','n',NW,NL),
 M('M26','x25','x24','0','0','n',NW,NL),
 ".ends bias"]
oa=[".subckt opamp vdd vp vm vout vbias1 vbias2 vbias3 vbias4 vpcas vncas",
 # NMOS input pair, two cascoded tails
 M('M2','al','vm','tn','tn','n','{NW*diff}',NL),
 M('M3','ar','vp','tn','tn','n','{NW*diff}',NL),
 M('M6','tn','vbias3','t6','t6','n',NW,NL), M('M7','t6','vbias4','0','0','n',NW,NL),
 M('M4','tn','vbias3','t4','t4','n',NW,NL), M('M5','t4','vbias4','0','0','n',NW,NL),
 # PMOS input pair, two cascoded tails
 M('M17','s17','vbias1','vdd','vdd','p',PW,PL), M('M19','tp','vbias2','s17','s17','p',PW,PL),
 M('M18','s18','vbias1','vdd','vdd','p',PW,PL), M('M20','tp','vbias2','s18','s18','p',PW,PL),
 M('M21','cl','vm','tp','tp','p','{PW*diff}',PL),
 M('M22','cr','vp','tp','tp','p','{PW*diff}',PL),
 # PMOS wide-swing mirror (gates = bl)
 M('M13','al','bl','vdd','vdd','p',PW,PL), M('M14','al','bl','vdd','vdd','p',PW,PL),
 M('M12','ar','bl','vdd','vdd','p',PW,PL), M('M1','ar','bl','vdd','vdd','p',PW,PL),
 M('M16','bl','vbias2','al','al','p',PW,PL), M('M15','br','vbias2','ar','ar','p',PW,PL),
 # floating current sources
 M('MFCPL1','dl','vpcas','bl','bl','p','{PW/2}',PL), M('MFCNL1','bl','vncas','dl','dl','n','{NW/2}',NL),
 M('MFCPR1','dr','vpcas','br','br','p','{PW/2}',PL), M('MFCNR1','br','vncas','dr','dr','n','{NW/2}',NL),
 # NMOS wide-swing mirror (gates = dl)
 M('M10','dl','vbias3','cl','cl','n',NW,NL), M('M8','dr','vbias3','cr','cr','n',NW,NL),
 M('M11','cl','dl','0','0','n',NW,NL), M('M23','cl','dl','0','0','n',NW,NL),
 M('M9','cr','dl','0','0','n',NW,NL), M('M24','cr','dl','0','0','n',NW,NL),
 # class-AB output
 M('MOP1','vout','br','vdd','vdd','p',PW,PL,'{out}'),
 M('MON1','vout','dr','0','0','n',NW,NL,'{out}'),
 "Cc1 ar vout 6p", "Cc2 vout xz 2p", "Rz xz cr 30 tc1=0.002",
 ".ends opamp"]

def core(): return "\n".join(bmr+[""]+bias+[""]+oa)+"\n"

hdr=""".param NL=0.6u NW=27u PL=0.6u PW=54u diff=10 out=125
"""
with open(D+'/kerstetter_opamp.sp','w') as f:
    f.write("* Kerstetter UNLV EE420 2019 C5 rail-to-rail op-amp (BMR + bias + op-amp), transcribed from Fig 1/4/8.\n"
            "* Model names are parameters: define .param-free via .subckt-level {N}/{P}: set with\n"
            "*   Baker card: .include c5_baker.lib + N=NMOS P=PMOS ; FP5: .lib fp5.lib tt + N=fp5n P=fp5p\n"
            "* (ngspice cannot parametrise model names, run.py text-substitutes {N}/{P}).\n"+hdr+core())

def deck(lib,vdd,load,opt='gmin=1e-12'):
    N,P=('NMOS','PMOS') if lib=='baker' else ('fp5n','fp5p')
    inc='.include "/home/fpga/ext/mosis_cards/c5_baker/c5_baker.lib"' if lib=='baker' else f'.lib "/home/fpga/pdks/fp5/models/fp5.lib" {lib}'
    c=core().replace('{N}',N).replace('{P}',P)
    ld="RL vout 0 1k\nCL vout 0 100p" if load else ""
    return f"""* kerstetter {lib} vdd={vdd} load={load}
{inc}
{hdr}{c}
VDD vdd 0 {vdd}
Xbmr vdd vbiasp bmr
Xb vdd vbiasp vb1 vb2 vb3 vb4 vpc vnc vlo vhi bias
Xo vdd vp vm vout vb1 vb2 vb3 vb4 vpc vnc opamp
VCM vp 0 dc {vdd/2} ac 1
Lf vout vm 1e9
Cf vm 0 1
{ld}
.options {opt}
.nodeset v(vout)={vdd/2} v(vm)={vdd/2}
.control
op
echo RES $&v(vbiasp) $&v(vb1) $&v(vb2) $&v(vb3) $&v(vb4) $&v(vpc) $&v(vnc) $&v(vlo) $&v(vhi) $&v(vout) $&i(VDD)
ac dec 50 1 1e9
meas ac gdc find vdb(vout) at=1
meas ac ugf when vdb(vout)=0
meas ac ph find vp(vout) when vdb(vout)=0
.endc
.end
"""

out=[]
cases=[('baker',v,l) for v in (2,5) for l in (0,1)]+[(c,v,l) for c in ('tt','ff','ss') for v in (2,5) for l in (0,1)]
for lib,v,l in cases:
    fn=f"{D}/runs/{lib}_{v}V_{'load' if l else 'noload'}.sp"
    for opt in ('gmin=1e-12','gmin=1e-15 reltol=1e-4','gmin=1e-12 reltol=1e-4'):
        open(fn,'w').write(deck(lib,v,l,opt))
        r=subprocess.run(['ngspice','-b',fn],capture_output=True,text=True).stdout
        m=re.search(r'^RES (.*)$',r,re.M)
        if m and abs(float(m.group(1).split()[9])-v/2)<5e-3: break   # DC servo converged
    def g(k):
        m=re.search(r'^'+re.escape(k)+r'\s*=\s*([-\d.eE+]+)',r,re.M); return float(m.group(1)) if m else float('nan')
    m=re.search(r'^RES (.*)$',r,re.M); a=[float(x) for x in m.group(1).split()] if m else [float('nan')]*11
    vals=[a[0],v-a[1],v-a[2],a[3],a[4],v-a[5],a[6],a[7],v-a[8],a[9],-a[10]]
    ph=g('ph'); import math
    pm=180+math.degrees(ph) if abs(ph)<7 else 180+ph
    out.append((lib,v,l,g('gdc'),g('ugf')/1e6,pm,vals))
with open(D+'/results.txt','w') as f:
    f.write("lib vdd load gain_dB ugf_MHz PM | vbiasp vb1' vb2' vb3 vb4 vpcas' vncas vlow vhigh' vout I(uA)  (' = VDD-V)\n")
    for lib,v,l,gd,u,pm,vals in out:
        vv=vals[:]; 
        if len(vv)==11: vv[10]*=1e6
        f.write(f"{lib:5s} {v} {'1k||100p' if l else 'none':8s} {gd:7.2f} {u:6.2f} {pm:7.2f} | "+" ".join(f"{x:.3f}" for x in vv)+"\n")
print(open(D+'/results.txt').read())
