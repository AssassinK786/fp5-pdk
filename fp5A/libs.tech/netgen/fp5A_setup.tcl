# FP5A Netgen setup
# The standard cells are compared as MOS devices.  Geometry (W/L) is the
# contract; AD/AS/PD/PS are layout-only and are removed before comparison.
# Resistor and capacitor endpoints are interchangeable.

permute transistors
permute resistors
property default

property {-circuit1 nfet} remove ad pd as ps
property {-circuit1 pfet} remove ad pd as ps

# Analog passives: compare drawn W/L, not the evaluated resistance/capacitance.
if {[lsearch -nocase -exact [cells list -all] rpoly] >= 0} {
    property rpoly tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] rpoly2] >= 0} {
    property rpoly2 tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] rhr] >= 0} {
    property rhr tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] rnwell] >= 0} {
    property rnwell tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] rndiff] >= 0} {
    property rndiff tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] rpdiff] >= 0} {
    property rpdiff tolerance {w 0.0} {l 0.0}
}
if {[lsearch -nocase -exact [cells list -all] cpoly] >= 0} {
    property cpoly tolerance {w 0.0} {l 0.0}
}
