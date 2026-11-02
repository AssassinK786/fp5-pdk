# FP5 KLayout PCell library (research PDK). Devices drawn on the MOSIS SCMOS SUBM rules (lambda = 0.30 um) that fp5.drc checks.
# Load in KLayout: Macros > run this file (or put it in ~/.klayout/pymacros and set "autorun"). Library name: "FP5".
# Cells: nmos, pmos (W, L, fingers, body tap), rpoly (poly resistor), cpoly (poly1-poly2 capacitor), gring (guard ring).
import pya

LAM = 0.30                        # um
LY = {'nwell': (42, 0), 'active': (43, 0), 'psel': (44, 0), 'nsel': (45, 0), 'poly': (46, 0), 'pcon': (47, 0),
      'acon': (48, 0), 'm1': (49, 0), 'poly2': (56, 0), 'p2con': (55, 0), 'hires': (34, 0)}

def snap(v):                      # um -> integer lambda count (rounded up)
    n = v / LAM
    return int(n) if abs(n - round(n)) < 1e-6 and round(n) == int(round(n)) else int(n) + 1

class _Base(pya.PCellDeclarationHelper):
    def _lymap(self, layout):
        return {k: layout.layer(*v) for k, v in LY.items()}
    def _box(self, cell, li, x1, y1, x2, y2, u):   # coordinates in lambda
        cell.shapes(li).insert(pya.Box(int(x1 * u), int(y1 * u), int(x2 * u), int(y2 * u)))

class MOS(_Base):
    """W per finger and L in um (snapped up to the lambda grid). Source/drain columns are 6 lambda (contact + 2 lambda to gate),
    gates are tied by a poly-contact strap on metal1 above the device; S/D metal1 strips are left open for routing."""
    def __init__(self, pmos):
        super().__init__()
        self.pmos = pmos
        self.param("w", self.TypeDouble, "Width per finger (um)", default=3.0)
        self.param("l", self.TypeDouble, "Length (um)", default=0.6)
        self.param("nf", self.TypeInt, "Fingers", default=1)
        self.param("tap", self.TypeBoolean, "Body tap strip below device", default=True)
    def display_text_impl(self):
        return f"{'pmos' if self.pmos else 'nmos'} W={self.w} L={self.l} nf={self.nf}"
    def coerce_parameters_impl(self):
        self.w = max(self.w, 4 * LAM); self.l = max(self.l, 2 * LAM); self.nf = max(1, self.nf)
    def produce_impl(self):
        ly = self.layout; u = 1.0 / ly.dbu * LAM / 1.0; L = self._lymap(ly); c = self.cell
        W, Lg, nf, SD = snap(self.w), snap(self.l), self.nf, 6
        X = nf * Lg + (nf + 1) * SD
        self._box(c, L['active'], 0, 0, X, W, u)
        self._box(c, L['psel' if self.pmos else 'nsel'], -2, -2, X + 2, W + 2, u)
        if self.pmos: self._box(c, L['nwell'], -6, -14 if self.tap else -6, X + 6, W + 6, u)
        if self.tap:                                      # body tap: p+ in substrate (nmos) or n+ in n-well (pmos), 4 lambda tall
            self._box(c, L['active'], 0, -8, X, -4, u)
            self._box(c, L['nsel' if self.pmos else 'psel'], -2, -10, X + 2, -2, u)
            for x in range(1, X - 2, 5): self._box(c, L['acon'], x, -7, x + 2, -5, u)
            self._box(c, L['m1'], 0, -8, X, -4, u)
        ncut = max(1, (W - 2 + 3) // 5)                     # contacts along each S/D column: 2 cut + 3 space, 1 lambda margin
        for k in range(nf + 1):
            x0 = k * (SD + Lg)                              # S/D column [x0, x0+SD]; contact at x0+1..x0+3 (2 lambda to gate)
            cx = x0 + 1 if k == 0 else (x0 + 3 if k == nf else x0 + 2)   # 1 lambda to active edge, >= 2 lambda to gates
            for j in range(ncut):
                cy = 1 + j * 5
                if cy + 2 > W - 1: break
                self._box(c, L['acon'], cx, cy, cx + 2, cy + 2, u)
            self._box(c, L['m1'], cx - 1, 0, cx + 3, W, u)
        for g in range(nf):
            gx = SD + g * (SD + Lg)
            self._box(c, L['poly'], gx, -2, gx + Lg, W + 3, u)
            pcx = gx + Lg / 2 - 2                             # 4 lambda poly pad above active, contact 2x2 centred
            self._box(c, L['poly'], pcx, W + 3, pcx + 4, W + 7, u)
            self._box(c, L['pcon'], pcx + 1, W + 4, pcx + 3, W + 6, u)
        first = SD + Lg / 2 - 2; last = SD + (nf - 1) * (SD + Lg) + Lg / 2 + 2
        self._box(c, L['m1'], first, W + 3, last, W + 7, u)

class NMOS(MOS):
    def __init__(self): super().__init__(False)
class PMOS(MOS):
    def __init__(self): super().__init__(True)

class RPOLY(_Base):
    """Poly resistor: body W x L (um), contact heads with one 2x2 contact each.
    R ~ Rsh x L/W + 2 x contact resistance.  Subclasses switch the body and
    contact layers for poly2 and hi-res poly2."""
    LAYER = 'poly'
    CONTACT = 'pcon'
    MINW = 2 * LAM
    MINL = 4 * LAM
    HEAD = 4
    HEADLEN = 4
    NAME = 'rpoly'
    def __init__(self):
        super().__init__()
        self.param("w", self.TypeDouble, "Width (um)", default=1.2)
        self.param("l", self.TypeDouble, "Length (um)", default=12.0)
    def display_text_impl(self): return f"{self.NAME} W={self.w} L={self.l}"
    def coerce_parameters_impl(self): self.w = max(self.w, self.MINW); self.l = max(self.l, self.MINL)
    def produce_impl(self):
        ly = self.layout; u = 1.0 / ly.dbu * LAM; L = self._lymap(ly); c = self.cell
        W, Ln = snap(self.w), snap(self.l); H = max(W, self.HEAD)
        body, con = L[self.LAYER], L[self.CONTACT]
        self._box(c, body, 0, 0, Ln, W, u)
        for x0 in (-self.HEADLEN, Ln):
            self._box(c, body, x0, (W - H) / 2, x0 + self.HEADLEN, (W + H) / 2, u)
            self._box(c, con, x0 + 1, W / 2 - 1, x0 + 3, W / 2 + 1, u)
            self._box(c, L['m1'], x0, W / 2 - 2, x0 + self.HEADLEN, W / 2 + 2, u)

class RPOLY2(RPOLY):
    """Poly2 resistor (40 ohm/sq)."""
    LAYER = 'poly2'; CONTACT = 'p2con'; MINW = 5 * LAM; MINL = 5 * LAM
    HEAD = 5; HEADLEN = 5; NAME = 'rpoly2'

class RHR(RPOLY2):
    """Hi-res poly2 resistor (~1030 ohm/sq) with the hires implant marker."""
    NAME = 'rhr'
    def produce_impl(self):
        super().produce_impl()
        ly = self.layout; u = 1.0 / ly.dbu * LAM; L = self._lymap(ly); c = self.cell
        W, Ln = snap(self.w), snap(self.l)
        self._box(c, L['hires'], 0, 0, Ln, W, u)

class CPOLY(_Base):
    """Poly1-poly2 capacitor: poly2 top plate W x L (um) with a contact grid, poly1 bottom plate enclosing by 2 lambda plus a
    contact strip. C ~ 0.845 fF/um^2 x W x L (MOSIS C5 median)."""
    def __init__(self):
        super().__init__()
        self.param("w", self.TypeDouble, "Width (um)", default=10.0)
        self.param("l", self.TypeDouble, "Length (um)", default=10.0)
    def display_text_impl(self): return f"cpoly {self.w}x{self.l} um (~{0.845*self.w*self.l:.0f} fF)"
    def coerce_parameters_impl(self): self.w = max(self.w, 5 * LAM); self.l = max(self.l, 5 * LAM)
    def produce_impl(self):
        ly = self.layout; u = 1.0 / ly.dbu * LAM; L = self._lymap(ly); c = self.cell
        W, Ln = snap(self.w), snap(self.l)
        self._box(c, L['poly'], -2, -2, Ln + 2 + 8, W + 2, u)            # bottom plate, extended right for its contacts
        self._box(c, L['poly2'], 0, 0, Ln, W, u)
        for x in range(1, Ln - 2, 5):
            for y in range(1, W - 2, 5):
                self._box(c, L['p2con'], x, y, x + 2, y + 2, u)
        self._box(c, L['m1'], 0, 0, Ln, W, u)
        for y in range(0, W - 2, 5):                                     # bottom-plate contacts 3 lambda right of poly2 + 2
            self._box(c, L['pcon'], Ln + 5, y, Ln + 7, y + 2, u)
        self._box(c, L['m1'], Ln + 4, -1, Ln + 8, max(W - 2, 3) + 1, u)

class GRING(_Base):
    """Guard ring around a W x H (um) opening: p+ ring in substrate (ptype=True, tie to gnd) or n+ ring in n-well (tie to vdd).
    Ring 4 lambda wide, contacts every 5 lambda, metal1 on top."""
    def __init__(self):
        super().__init__()
        self.param("w", self.TypeDouble, "Inner width (um)", default=20.0)
        self.param("h", self.TypeDouble, "Inner height (um)", default=20.0)
        self.param("ptype", self.TypeBoolean, "p+ ring (else n+ ring in n-well)", default=True)
    def display_text_impl(self): return f"guard ring {'p+' if self.ptype else 'n+'} {self.w}x{self.h} um"
    def produce_impl(self):
        ly = self.layout; u = 1.0 / ly.dbu * LAM; L = self._lymap(ly); c = self.cell
        Wi, Hi = snap(self.w), snap(self.h); R = 4
        sides = [(-R, -R, Wi + R, 0), (-R, Hi, Wi + R, Hi + R), (-R, 0, 0, Hi), (Wi, 0, Wi + R, Hi)]
        for (x1, y1, x2, y2) in sides:
            self._box(c, L['active'], x1, y1, x2, y2, u); self._box(c, L['m1'], x1, y1, x2, y2, u)
        sel = L['psel' if self.ptype else 'nsel']
        for (x1, y1, x2, y2) in [(-R - 2, -R - 2, Wi + R + 2, 2), (-R - 2, Hi - 2, Wi + R + 2, Hi + R + 2), (-R - 2, 2, 2, Hi - 2), (Wi - 2, 2, Wi + R + 2, Hi - 2)]:
            self._box(c, sel, x1, y1, x2, y2, u)
        if not self.ptype: self._box(c, L['nwell'], -R - 6, -R - 6, Wi + R + 6, Hi + R + 6, u)
        for x in range(-R + 1, Wi + R - 2, 5):
            self._box(c, L['acon'], x, -R + 1, x + 2, -R + 3, u); self._box(c, L['acon'], x, Hi + 1, x + 2, Hi + 3, u)
        for y in range(2, Hi - 3, 5):
            self._box(c, L['acon'], -R + 1, y, -R + 3, y + 2, u); self._box(c, L['acon'], Wi + 1, y, Wi + 3, y + 2, u)

class FP5Lib(pya.Library):
    def __init__(self):
        self.description = "FP5 0.5 um 5 V devices (research PDK)"
        for n, cls in (("nmos", NMOS), ("pmos", PMOS), ("rpoly", RPOLY), ("rpoly2", RPOLY2), ("rhr", RHR), ("cpoly", CPOLY), ("gring", GRING)):
            self.layout().register_pcell(n, cls())
        self.register("FP5")

FP5Lib()
