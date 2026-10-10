"""Render overlays from computed.json. Run from the shape folder: python3 scripts/make_overlays.py"""
import json, numpy as np
from PIL import Image, ImageDraw
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = '../../../03_images/reefs/cables-reef-wa/'
C = json.load(open('scripts/computed.json'))
def draw(img, scale, polys, out, pts=(), labels=(), rot=0):
    im = Image.open(img).convert('RGB')
    if rot: im = im.rotate(rot, expand=True)
    im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS); d = ImageDraw.Draw(im, 'RGBA')
    for poly, col in polys:
        q = [(x*scale, y*scale) for x, y in poly]; d.polygon(q, fill=col+(45,)); d.line(q+[q[0]], fill=col+(255,), width=2)
    for (x, y), t, col in pts:
        d.ellipse((x*scale-4, y*scale-4, x*scale+4, y*scale+4), outline=col, width=2); d.text((x*scale+6, y*scale-12), t, fill=col)
    for (x, y), t, col in labels: d.text((x, y), t, fill=col)
    im.save(out)
RED, BLUE, GRN, ORG = (230, 0, 0), (0, 70, 220), (0, 150, 60), (255, 130, 0)
# img-05: toe polygon + extension + grid crosses
cross = [((94.8, 144), '+'), ((276, 146), '+'), ((455.2, 148), '+'), ((92, 322), '+'), ((272, 324), '+'), ((452, 324), '+')]
draw(R+'cables-reef-wa_rwr-original-design-plan_1990s.jpg', 2.5,
     [(C['v_orig_m'] and [tuple(p) for p in json.load(open('scripts/p05_toe_pixels.json'))['polys'][0]], RED), ([tuple(p) for p in C['tri_px_05']], ORG)],
     'overlays/cables-reef-wa-img-05_toe_outline_and_extension.png',
     pts=[((23, 261.5), 'P2', BLUE), ((146.5, 300), 'P1', BLUE), ((295.5, 20), 'apex', BLUE), ((466, 182.5), 'P3', BLUE)] + [(p, 'grid +', GRN) for p, _ in cross[:3]],
     labels=[((20, 20), 'RED = traced outer foot of the hatched rock bands (silhouette, scale 3.6 px/m = 180 px grid / 50 m, assumed)', RED), ((20, 36), 'ORANGE = extension triangle from img-06 (320 m3 additional fill), registered on P2-P1', ORG), ((20, 52), 'GREEN = drawing grid crosses, 180 px apart (value not legible; 50 m assumed)', GRN)])
# img-06: triangle
draw(R+'cables-reef-wa_rwr-additional-fill-area-plan_1990s.jpg', 2.5, [([(76.7, 190), (165, 212.7), (111.7, 248.3)], ORG)], 'overlays/cables-reef-wa-img-06_extension_triangle.png',
     pts=[((76.7, 190), 'P2 (reg.)', BLUE), ((165, 212.7), 'P1 (reg.)', BLUE), ((111.7, 248.3), 'N', BLUE), ((250, 16), 'apex', GRN), ((387.5, 132.5), 'P3', GRN), ((259, 136), 'inner apex', GRN), ((315, 181), 'valley', GRN)])
# Fig 7 (rotated so north is up)
draw(R+'cables-reef-wa_pattiaratchi1999-fig7-geographic-location_1999.png', 3.2, [([tuple(p) for p in C['fig7_px']], RED)], 'overlays/cables-reef-wa-img-20_fig7_V_outline_rotated.png', rot=-90)
# Pitt sketch
draw(R+'cables-reef-wa_rwr-pitt-sketch-plan_1990s.jpg', 2.5, [([tuple(p) for p in C['pitt_px']], BLUE)], 'overlays/cables-reef-wa-img-07_pitt_concept_outline.png')
# comparison in metres
fig, ax = plt.subplots(figsize=(9, 6.5))
cols = {'v_asbuilt_m': ('#d62728', 'as-built design + extension (default)', 1.8), 'v_orig_m': ('#ff7f0e', 'original design plan (before extension)', 1.2), 'fig7_m': ('#2ca02c', 'paper Fig 7 V outline (cross-check)', 1.2), 'pitt_m': ('#1f77b4', 'Pitt concept sketch (proposal)', 1.2)}
for k, (c, l, w) in cols.items():
    p = np.array(C[k]); ax.plot(*np.vstack([p, p[:1]]).T, color=c, lw=w, label=l)
ax.axhline(0, color='k', lw=0.5); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend(fontsize=8, loc='lower right')
ax.set_xlabel('alongshore, m (centred on each outline; + = north)'); ax.set_ylabel('offshore, m relative to centroid (+ = west)')
ax.set_title('cables-reef-wa outline versions in metres (scale assumptions in METHOD.md; low confidence)', fontsize=9)
fig.tight_layout(); fig.savefig('overlays/cables-reef-wa_versions_compare_m.png', dpi=110)
