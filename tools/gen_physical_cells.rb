# Generate FP5A TAP and DECAP GDS cells (4.8 x 30 um, two core sites).
ly = RBA::Layout::new
ly.dbu = 0.001
def layer(ly, n) ly.layer(n, 0) end
def box(cell, li, x1, y1, x2, y2)
  cell.shapes(li).insert(RBA::Box::new(x1, y1, x2, y2))
end

# ---------------- TAP ----------------
tap = ly.create_cell("TAP")
nwell = layer(ly, 42); active = layer(ly, 43); psel = layer(ly, 44); nsel = layer(ly, 45)
acon = layer(ly, 48); m1 = layer(ly, 49)
box(tap, m1, -600, -900, 5400, 900)
box(tap, m1, -600, 29100, 5400, 30900)
# p+ substrate tap (bottom)
box(tap, active, 1800, 1500, 3000, 4500)
box(tap, psel, 0, 900, 4800, 5100)
box(tap, acon, 2100, 2400, 2700, 3000)
box(tap, m1, 1800, 2100, 3000, 3300)
box(tap, m1, 1800, 300, 3000, 3300)
# n+ n-well tap (top), nwell only around the top tap
box(tap, nwell, 0, 14400, 4800, 31500)
box(tap, active, 1800, 26100, 3000, 27900)
box(tap, nsel, 0, 25500, 4800, 28500)
box(tap, acon, 2100, 26400, 2700, 27000)
box(tap, m1, 1800, 26100, 3000, 27300)
box(tap, m1, 1800, 26100, 3000, 29700)

# ---------------- DECAP ----------------
decap = ly.create_cell("DECAP")
poly = layer(ly, 46); pcon = layer(ly, 47); poly2 = layer(ly, 56); p2con = layer(ly, 55)
box(decap, nwell, 0, 14400, 4800, 30000)
box(decap, m1, -600, -900, 5400, 900)
box(decap, m1, -600, 29100, 5400, 30900)
# poly1 bottom plate, gnd
box(decap, poly, 1500, 1500, 3300, 27000)
box(decap, pcon, 2100, 1800, 2700, 2400)
box(decap, m1, 1800, 1500, 3000, 2700)
box(decap, m1, 1800, 300, 3000, 2700)
# poly2 top plate, vdd
box(decap, poly2, 1650, 4500, 3150, 27600)
box(decap, p2con, 2100, 26700, 2700, 27300)
box(decap, m1, 1800, 26400, 3000, 27600)
box(decap, m1, 1800, 26400, 3000, 29700)

# ---------------- ENDCAP ----------------
endcap = ly.create_cell("ENDCAP")
box(endcap, nwell, 0, 14400, 4800, 31500)
box(endcap, m1, -600, -900, 5400, 900)
box(endcap, m1, -600, 29100, 5400, 30900)

ly.write("fp5A/libs.ref/fp5_osu/gds/fp5_physical.gds")
puts "wrote fp5_physical.gds"
