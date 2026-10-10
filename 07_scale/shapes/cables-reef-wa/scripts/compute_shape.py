"""cables-reef-wa: pixel polygons -> canonical metres, areas, angles. Run: python3 scripts/compute_shape.py  (from the shape folder)
Inputs: scripts/p05_toe_pixels.json (silhouette trace of the RWR design plan, native px) + hand-picked points below.
Outputs: scripts/computed.json"""
import json, numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
here = __file__.rsplit('/', 1)[0]
P05 = np.array(json.load(open(here + '/p05_toe_pixels.json'))['polys'][0])
S05 = 3.6        # px per metre, img-05 native (see METHOD.md step 6)
S05_LO, S05_HI = 2.7, 4.5
# --- extension triangle (img-06 native -> img-05 native by 2-point similarity P2,P1)
P2_05, P1_05 = np.array([23.0, 261.5]), np.array([146.5, 300.0])
P2_06, P1_06, N_06 = np.array([76.7, 190.0]), np.array([165.0, 212.7]), np.array([111.7, 248.3])
def sim2(a0, a1, b0, b1):
    za0, za1, zb0, zb1 = [complex(*p) for p in (a0, a1, b0, b1)]
    k = (zb1 - zb0) / (za1 - za0)
    return lambda p: (lambda z: np.array([z.real, z.imag]))(zb0 + k * (complex(*p) - za0)), abs(k), np.degrees(np.angle(k))
f, k, rot = sim2(P2_06, P1_06, P2_05, P1_05)
N_05 = f(N_06)
TRI05 = np.array([P2_05, P1_05, N_05])
orig = Polygon(P05); tri = Polygon(TRI05)
asb = unary_union([orig, tri]).buffer(0)
asb_px = np.array(asb.exterior.coords)[:-1]
# --- canonical frame: x alongshore toward north (= sheet right), y offshore (= sheet up); origin = shoreline point nearest centroid;
# centroid of as-built polygon placed at Y_CEN m offshore (Fig 7 measurement, see METHOD.md step 8)
Y_CEN = 270.0
cen = np.array(asb.centroid.coords[0])
def to_m(poly_px, s=S05, c=cen, ycen=Y_CEN):
    return [[round((u - c[0]) / s, 2), round(ycen + (c[1] - v) / s, 2)] for u, v in poly_px]
def stats(poly_m):
    Pg = Polygon(poly_m); b = Pg.bounds
    return {"area_m2": round(Pg.area, 1), "alongshore_m": round(b[2] - b[0], 1), "crossshore_m": round(b[3] - b[1], 1)}
out = {}
out['v_asbuilt_px'] = asb_px.round(2).tolist(); out['v_asbuilt_m'] = to_m(asb_px); out['v_asbuilt'] = stats(out['v_asbuilt_m'])
out['v_orig_m'] = to_m(P05); out['v_orig'] = stats(out['v_orig_m'])
out['tri_px_05'] = TRI05.round(2).tolist(); out['tri_m'] = to_m(TRI05); out['tri'] = stats(out['tri_m'])
out['reg06_to_05'] = {"scale": round(k, 3), "rot_deg": round(rot, 2)}
for nm, s in (('lo', S05_HI), ('hi', S05_LO)):   # area range: bigger px/m -> smaller area
    out['area_' + nm + '_m2'] = round(Polygon(to_m(asb_px, s)).area, 0)
# --- arm angles (outer edges), canonical frame of the original polygon
M = np.array(out['v_orig_m'])
def fit_dir(idx):
    pts = M[idx]; c = pts.mean(0); u, s, vt = np.linalg.svd(pts - c); d = vt[0]
    return d if d[0] > 0 else -d
dS = fit_dir(list(range(24, 56))); dN = fit_dir(list(range(70, 91)))
angS = float(np.degrees(np.arctan2(dS[1], dS[0])))   # S arm outer edge: heading toward apex goes +x? check sign below
angN = float(np.degrees(np.arctan2(dN[1], dN[0])))
out['arm_dirs_deg_from_x_axis'] = {"south_arm_outer_edge": round(angS, 1), "north_arm_outer_edge": round(angN, 1)}
# --- Pitt concept sketch (native px of img-07) scale 0.855 px/m
PITT = np.array([(123,92.4),(114,109),(107.6,133),(93.5,159),(70,192),(52,212),(51,218),(61,224),(79,228.5),(90.6,227),(105,209),(120,193),(123,189),(143.5,203.5),(152,209),(167,224),(182,228.5),(196,218),(184.7,200.6),(167,177),(149.4,150.6),(140.6,130),(133,106.5)])
SP = 0.855
pc = np.array(Polygon(PITT).centroid.coords[0])
out['pitt_px'] = PITT.tolist()
out['pitt_m'] = [[round((u - pc[0]) / SP, 2), round(Y_CEN + (pc[1] - v) / SP, 2)] for u, v in PITT]   # centroid placed at Y_CEN for comparison only
out['pitt'] = stats(out['pitt_m'])
# --- Fig 7 V (rotated native px, north up, west left), 2 m/px if grid = 100 m
F7 = np.array([(124,121),(130,113),(140,100),(146,97),(152,103),(155,108),(153,113),(150,118),(148,124),(155,131),(160,139),(162,146),(162,151),(157,157),(156,158),(146,148),(135,137),(127,129)])
S7 = 0.5
fc = np.array(Polygon(F7).centroid.coords[0])
out['fig7_px'] = F7.tolist()
out['fig7_m'] = [[round((fc[1] - v) / S7, 2), round(Y_CEN + (fc[0] - u) / S7, 2)] for u, v in F7]   # north up, west (offshore) left in the rotated figure; centroid at Y_CEN (Fig 7 itself puts it at ~271 m from the shore line)
out['fig7'] = stats(out['fig7_m'])
json.dump(out, open(here + '/computed.json', 'w'))
for k_ in ('v_asbuilt', 'v_orig', 'tri', 'pitt', 'fig7'): print(k_, out[k_])
print(out['reg06_to_05'], out['arm_dirs_deg_from_x_axis'], out['area_lo_m2'], out['area_hi_m2'], 'cen_px', cen.round(1))
