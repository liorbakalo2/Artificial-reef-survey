#!/usr/bin/env python3
"""figures_wave.py - Figure 3 of the surf-reef review: the wave over a gradual ramp and over an abrupt rise, to scale.

  python3 -I 08_paper/analysis/figures_wave.py            # writes fig3_wave_sketch.png / .pdf (+ caption by hand)

Inputs (read only; every number on the figure comes from these):
  08_paper/data/profiles/palm-beach-gold-coast.json, boscombe-surf-reef.json   lines.crest_line (profile + metrics), tidal planes
  08_paper/analysis/results_breaking.csv   rows crest_line, H0 = 1.0 m, T = 10 s, tide mid, gamma_mode mccowan (break point,
                                           H_b, d_b, xi_b, Y, class); the same incident wave in both panels
  08_paper/analysis/results_surf_site.csv  Boscombe site wave (0.5 m, 8 s), mid tide
  08_paper/analysis/wavelib.py             Airy shoaling and wavenumber (the water surface up to the break)
Geometry is the DERIVED 3D-model section (profiles/SUMMARY.md); the wave shapes at the break are schematic (height and
position are model values, the lip and foam shapes are drawn by hand); the sinusoids are linear theory (H = H0 Ks(d)).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S  # noqa: E402
import wavelib as W  # noqa: E402
from style import INK, INK2, SAND, SEABED, TIDE  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Ellipse, Patch, Polygon, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
H0_SHARED, T_SHARED = 1.0, 10.0          # incident wave used in both panels (FIGURE_SPECS F3)
GAMMA = 0.78                             # McCowan 1894 via Weggel 1972 (wavelib REFS)
VE = 5.0                                 # vertical exaggeration of the overview panels
ZLO, ZHI = -8.0, 2.5                     # m MSL
XSEA, XSHORE = 133.0, -32.0              # m seaward of the crest's seaward edge (positive = seaward)
INSET_HALF = 5.5                         # m, half width of the 1:1 detail window
INSET_Z = (-3.7, 1.75)
WATER = '#CFE3F2'
REEF = '#8C8C8C'
FOAM = '#FFFFFF'
FIG_H = 10.9                             # cm

PANELS = [
    dict(slug='palm-beach-gold-coast', letter='a', name='Palm Beach', kind='Long gradual ramp', site=(1.0, 10.0),
         israel=0.40),
    dict(slug='boscombe-surf-reef', letter='b', name='Boscombe', kind='Abrupt rise', site=(0.5, 8.0), israel=0.40),
]


# --------------------------------------------------------------------------------------------- data
def load(panel):
    s = panel['slug']
    pr = json.load(open(os.path.join(S.DATA_DIR, 'profiles', s + '.json'), encoding='utf-8'))
    L = pr['lines']['crest_line']
    m = L['metrics']
    p = L['profile']
    y = np.array(p['offshore_m'], float)
    bed = np.array(p['seabed_msl_m'], float)
    reef = np.array([np.nan if v is None else v for v in p['reef_msl_m']], float)
    top = np.where(np.isfinite(reef), np.maximum(bed, reef), bed)       # solid surface seen by the water
    b = pd.read_csv(os.path.join(HERE, 'results_breaking.csv'))
    r = b[(b.slug == s) & (b.line == 'crest_line') & (b.H0 == H0_SHARED) & (b['T'] == T_SHARED) & (b.tide == 'mid')
          & (b.gamma_mode == 'mccowan')].iloc[0]
    site = pd.read_csv(os.path.join(HERE, 'results_surf_site.csv'))
    rs = site[(site.slug == s) & (site.tide == 'mid')].iloc[0]
    pl = pr['tidal_planes_m_above_msl']
    lo, hi = (pl['MLWS'], pl['MHWS'])
    ce = m['crest_zone_y_m'][1]                                          # seaward edge of the crest zone (ramp starts here)
    return dict(y=y, bed=bed, reef=reef, top=top, m=m, r=r, rs=rs, lo=lo, hi=hi, ce=ce, spring=hi - lo)


def interp(y, z, yy):
    return np.interp(yy, y, z)


# --------------------------------------------------------------------------------------------- drawing helpers
def surfer_polys(x0, z0, xs=1.0):
    """Front-view standing surfer, 1.8 m from the feet to the top of the head, feet on z0 at x0.
    xs scales the horizontal coordinates only (xs = VE draws an undistorted pictogram in a vertically exaggerated panel).
    Returns (list of Polygon xy arrays, head centre, head radius)."""
    def P(pts):
        return np.array([[x0 + xs * a, z0 + b] for a, b in pts])
    body = [
        P([(-0.17, 0.0), (-0.05, 0.0), (-0.05, 0.90), (0.05, 0.90), (0.05, 0.0), (0.17, 0.0), (0.17, 0.96),     # legs
           (0.20, 1.50), (0.12, 1.55), (-0.12, 1.55), (-0.20, 1.50), (-0.17, 0.96)]),                           # hips, torso
        P([(0.18, 1.50), (0.76, 1.30), (0.78, 1.22), (0.70, 1.22), (0.16, 1.40)]),                              # arm right
        P([(-0.18, 1.50), (-0.76, 1.30), (-0.78, 1.22), (-0.70, 1.22), (-0.16, 1.40)]),                         # arm left
        P([(-0.30, -0.07), (0.30, -0.07), (0.30, 0.0), (-0.30, 0.0)]),                                          # board (end-on)
        P([(-0.04, 1.55), (0.04, 1.55), (0.04, 1.62), (-0.04, 1.62)]),                                          # neck
    ]
    head = (x0, z0 + 1.69, 0.11)
    return body, head


def draw_surfer(ax, x0, z0, xs=1.0, zorder=8):
    body, (hx, hz, hr) = surfer_polys(x0, z0, xs)
    for b in body:
        ax.add_patch(Polygon(b, closed=True, fc=INK, ec=INK, lw=0.3, zorder=zorder))
    ax.add_patch(Ellipse((hx, hz), 2 * hr * xs, 2 * hr, fc=INK, ec=INK, lw=0.3, zorder=zorder))


def bez(p0, p1, p2, p3, n=24):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def breaker_outline(H, eta, kind, back=9.0):
    """Schematic breaking-wave surface (water body upper boundary) as (u, z) points, u = distance shoreward of the crest.
    Height H (trough to crest, model value) is true; the shape is a hand-drawn plunging lip or a collapsing front.
    Returns outline points from the seaward back, over the crest, down the front face, to the foam/trough on the shoreward side,
    plus dict of face anchor points for the surfer."""
    zt = eta - H / 2.0
    uu = np.linspace(-back - 6.0, 0.0, 60)
    ub = np.where(uu < -back, -back, uu)
    zb = eta + (H / 2.0) * np.cos(np.pi * ub / back)                      # back of the wave: half cosine to the crest
    pts = list(zip(uu, zb))
    if kind == 'plunging':
        # (u, v) in units of H with v = 0 at the trough level: lip thrown forward, hollow under it, face down to the base
        o = bez((0.0, 1.0), (0.22, 1.04), (0.60, 0.98), (0.64, 0.64))      # outer surface of the lip
        i = bez((0.64, 0.64), (0.62, 0.46), (0.44, 0.34), (0.26, 0.36))    # underside of the lip (the hollow)
        f = bez((0.26, 0.36), (0.14, 0.30), (0.12, 0.12), (0.26, 0.0))     # face down to the base
        seg = np.vstack([o, i[1:], f[1:]])
        face = (0.78, 0.10)
    else:                                                                # collapsing / surging front: near-vertical face
        o = bez((0.0, 1.0), (0.10, 1.0), (0.16, 0.90), (0.18, 0.70))
        f = bez((0.18, 0.70), (0.19, 0.50), (0.17, 0.28), (0.22, 0.05))
        seg = np.vstack([o, f[1:]])
        face = (0.45, 0.10)
    pts += [(H * a, zt + H * b) for a, b in seg]
    # front trough: flat to the shoreward limit
    pts += [(H * 0.22 + 0.5, zt), (40.0, zt)]
    return np.array(pts), face, zt


def water_surface(P, y_b, eta=0.0):
    """Linear-theory surface seaward of the break: eta + H/2 cos(theta), H = H0 Ks(d), theta = integral of k dy from y_b."""
    yy = np.arange(y_b, P['y'].max(), 0.25)
    d = eta - interp(P['y'], P['top'], yy)
    d = np.maximum(d, 0.05)
    k = W.wavenumber(T_SHARED, d)
    H = H0_SHARED * W.shoaling_coefficient(T_SHARED, d)
    H = np.minimum(H, GAMMA * d)                                         # never above the breaking limit
    theta = np.concatenate([[0.0], np.cumsum(0.5 * (k[1:] + k[:-1]) * np.diff(yy))])
    return yy, eta + 0.5 * H * np.cos(theta)


# --------------------------------------------------------------------------------------------- the figure
BLUE = '#2F6E9E'
RED = '#B03A2E'


def fig3():
    S.setup()
    plt.rcParams.update({'font.size': 7, 'axes.labelsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7})
    fig = plt.figure(figsize=(S.FULL_W, FIG_H * S.CM))
    wcm, hcm = 17.0, FIG_H

    def axes_cm(l, b, w, h, **kw):
        return fig.add_axes([l / wcm, b / hcm, w / wcm, h / hcm], **kw)

    L_OV, W_OV = 1.15, 10.2                                              # overview column (cm)
    L_IN, W_IN = 12.2, 4.7                                               # detail column (cm)
    mpc = (XSEA - XSHORE) / W_OV                                         # m per cm, horizontal (both panels)
    H_OV = (ZHI - ZLO) / (mpc / VE)                                      # cm for 10.5 m of elevation
    rows = [(7.15, PANELS[0]), (2.15, PANELS[1])]
    halo = dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.88)
    dim = dict(arrowstyle='<->', lw=0.7, color=INK, shrinkA=0, shrinkB=0, mutation_scale=5)
    for (bot, pan) in rows:
        P = load(pan)
        r, m = P['r'], P['m']
        ce = P['ce']
        x_of = lambda yv: yv - ce                                        # noqa: E731  model y -> m seaward of the crest edge
        ax = axes_cm(L_OV, bot, W_OV, H_OV)
        ax.set_xlim(XSEA, XSHORE)
        ax.set_ylim(ZLO, ZHI)
        xs = x_of(P['y'])
        yb = float(r.y_break)
        xb = x_of(yb)
        Hb = float(r.H_break)
        db = float(r.d_break)
        kind = 'plunging' if (r.breaker == 'plunging' and r.vortex_Y >= 1.6) else 'collapsing'
        # water: linear train seaward of the break, still water shoreward
        yy, eta_s = water_surface(P, yb)
        shore = np.arange(P['y'].min(), yb, 0.5)
        ys_all = np.concatenate([shore, yy])
        zs_all = np.concatenate([np.zeros_like(shore), eta_s])
        ax.fill_between(x_of(ys_all), interp(P['y'], P['top'], ys_all), zs_all, color=WATER, lw=0, zorder=1)
        # local spring tide band over the water, Israeli range as thin dashed lines
        ax.axhspan(P['lo'], P['hi'], color=TIDE, alpha=0.45, lw=0, zorder=2)
        # seabed sand and reef body
        ax.fill_between(xs, ZLO, P['bed'], color=SAND, lw=0, zorder=3)
        ok = np.isfinite(P['reef'])
        ax.fill_between(xs, np.where(ok, P['bed'], np.nan), np.where(ok, P['reef'], np.nan), facecolor='#CBBE9F',
                        edgecolor=INK2, hatch='////', lw=0, zorder=4)
        ax.plot(xs, P['top'], color=SEABED, lw=0.9, zorder=5, solid_capstyle='round')
        ax.plot(x_of(ys_all), zs_all, color=BLUE, lw=0.9, zorder=6)
        ax.axhline(0, color=INK2, lw=0.5, ls=(0, (6, 3)), zorder=6)
        for sgn in (-1, 1):
            ax.axhline(sgn * pan['israel'] / 2, color=RED, lw=0.6, ls=(0, (2, 2)), zorder=6)
        # dimension lines: crest level, toe-bed level, depth gap, ramp length
        zc = m['crest_z_msl_m']
        zt_bed = m['seaward_toe_seabed_z_msl_m']
        ramp = m['ramp_length_m']
        gap = m['crest_to_toe_seabed_drop_m']
        slope = m['mean_seaward_slope']['one_in']
        ax.plot([0, XSEA - 1], [zc, zc], color=INK, lw=0.5, ls=(0, (1, 2)), zorder=7)
        ax.plot([ramp, XSEA - 1], [zt_bed, zt_bed], color=INK, lw=0.5, ls=(0, (1, 2)), zorder=7)
        ax.annotate('', xy=(0, zc), xytext=(ramp, zc), arrowprops=dim, zorder=8)
        xg = XSEA - 6
        ax.annotate('', xy=(xg, zc), xytext=(xg, zt_bed), arrowprops=dim, zorder=8)
        ax.text(xg - 3, (zc + zt_bed) / 2, 'depth gap\n%.2f m' % gap, ha='left', va='center', fontsize=7, bbox=halo, zorder=9)
        ax.text(xg - 3, zc - 0.12, 'crest depth %.2f m' % (-zc), ha='left', va='top', fontsize=7, bbox=halo, zorder=9)
        ax.text(xg - 3, zt_bed + 0.12, 'toe-bed depth %.2f m' % (-zt_bed), ha='left', va='bottom', fontsize=7, bbox=halo, zorder=9)
        rtxt = 'ramp %.0f m, mean slope 1:%.1f' % (ramp, slope)
        if ramp > 40:
            ax.text(ramp / 2.0, zc + 0.12, rtxt, ha='center', va='bottom', fontsize=7, bbox=halo, zorder=9)
        else:
            ax.text(ramp + 3, zc - 0.15, rtxt, ha='right', va='top', fontsize=7, bbox=halo, zorder=9)
        # zoom window of the 1:1 detail
        z0w, z1w = INSET_Z
        ax.add_patch(Rectangle((xb - INSET_HALF, z0w), 2 * INSET_HALF, z1w - z0w, fill=False, ec=INK, lw=0.6, ls=(0, (3, 2)),
                               zorder=9))
        ax.text(XSEA - 1.5, ZHI - 0.1, '(%s) %s: %s' % (pan['letter'], pan['kind'], pan['name']), ha='left', va='top',
                fontsize=7.5, fontweight='bold', zorder=9)
        ax.text(XSEA - 1.5, ZHI - 0.95, 'H$_0$ = %.1f m, T = %.0f s, tide MSL; local spring range %.2f m' % (H0_SHARED, T_SHARED, P['spring']),
                ha='left', va='top', fontsize=7, color=BLUE, zorder=9)
        # surfer pictogram (true height 1.8 m on the vertical axis; undistorted width) on the face at the break
        outline, face, zt = breaker_outline(Hb, 0.0, kind)
        fu, fv = face
        draw_surfer(ax, xb - Hb * fu - 0.35, zt + 0.07, xs=VE, zorder=9)
        ax.set_ylabel('Elevation (m MSL)')
        ax.set_yticks([-8, -6, -4, -2, 0, 2])
        ax.set_xticks(np.arange(120, XSHORE - 1, -20))
        ax.set_xlabel('Distance seaward of the crest edge (m); shore to the right; overview vertical exaggeration 5:1' if pan['letter'] == 'b' else '')
        ax.tick_params(length=2.5)

        # ---- 1:1 detail
        bz = z1w - z0w
        h_in = bz / (2 * INSET_HALF / W_IN)                               # cm, equal scale in x and z
        bx = axes_cm(L_IN, bot + H_OV - h_in - 0.55, W_IN, h_in)
        bx.set_xlim(INSET_HALF, -INSET_HALF)
        bx.set_ylim(z0w, z1w)
        sx = np.linspace(-45.0, 22.0, 1400)                              # s = y - y_break (positive offshore)
        ysx = yb + sx
        topx = interp(P['y'], P['top'], ysx)
        bedx = interp(P['y'], P['bed'], ysx)
        rf = interp(P['y'], np.nan_to_num(P['reef'], nan=-99.0), ysx)
        reefx = np.where(rf > bedx + 0.02, rf, bedx)
        bx.fill_between(sx, -12, bedx, color=SAND, lw=0, zorder=3)
        bx.fill_between(sx, bedx, reefx, facecolor='#CBBE9F', edgecolor=INK2, hatch='////', lw=0, zorder=4)
        bx.plot(sx, topx, color=SEABED, lw=0.9, zorder=5)
        su, zu = -outline[:, 0], outline[:, 1]                           # u is shoreward, inset x is s = -u
        zu = np.maximum(zu, np.interp(su, sx, topx))                     # the surface never dips below the solid bed
        mm = (sx >= su.min()) & (sx <= su.max())
        poly = np.vstack([np.column_stack([su, zu]), np.column_stack([sx[mm], topx[mm]])])
        bx.add_patch(Polygon(poly, closed=True, fc=WATER, ec='none', zorder=1))
        bx.axhspan(P['lo'], P['hi'], color=TIDE, alpha=0.0)              # (no tide band here: it spans the whole window)
        bx.plot(su, zu, color=BLUE, lw=1.0, zorder=7)
        bx.axhline(0, color=INK2, lw=0.5, ls=(0, (6, 3)), zorder=6)
        if kind == 'collapsing':                                         # foam of the collapsing front
            hf = Hb
            bx.add_patch(Polygon([(-(hf * 0.20), zt), (-(hf * 0.20 + 2.4), zt), (-(hf * 0.20 + 1.8), zt + 0.30 * hf),
                                  (-(hf * 0.20 + 0.7), zt + 0.55 * hf), (-(hf * 0.19), zt + 0.45 * hf)], closed=True, fc='white',
                                 ec=BLUE, lw=0.5, zorder=8))
        draw_surfer(bx, -(Hb * fu) - 0.35, zt + 0.07, xs=1.0, zorder=9)
        # height dimension (H_b) on the seaward side (guide lines from crest and trough), depth dimension (h_b) under the crest
        xh = INSET_HALF - 0.9
        bx.plot([0.1, xh + 0.2], [Hb / 2, Hb / 2], color=INK, lw=0.4, ls=(0, (1, 2)), zorder=8)
        bx.plot([xh + 0.2, xh - 0.2], [zt, zt], color=INK, lw=0.4, zorder=8)
        bx.annotate('', xy=(xh, Hb / 2), xytext=(xh, zt), arrowprops=dim, zorder=10)
        bx.text(xh - 0.45, Hb / 2 + 0.28, 'H$_b$ = %.2f m' % Hb, ha='left', va='bottom', fontsize=7, zorder=10)
        zbed_b = float(interp(P['y'], P['top'], np.array([yb]))[0])
        bx.annotate('', xy=(0.0, 0.0), xytext=(0.0, zbed_b), arrowprops=dim, zorder=10)
        bx.text(0.4, zbed_b / 2 - 0.05, 'h$_b$ = H$_b$/\u03b3\n= %.2f m' % db, ha='right', va='center', fontsize=7, bbox=halo, zorder=10)
        bx.set_xticks([4, 2, 0, -2, -4])
        bx.set_yticks([-4, -2, 0])
        bx.tick_params(length=2.0)
        bx.set_xlabel('Distance seaward of the break (m)', labelpad=1.5)
        bx.set_ylabel('m MSL', labelpad=1.0)
        bx.text(INSET_HALF, z1w + 0.1, '1:1 detail of the dashed box', ha='left', va='bottom', fontsize=7, color=INK)
        # text block under the inset
        ty = bot + H_OV - h_in - 0.55 - 0.75
        dag = '†' if bool(r.vortex_extrapolated) else ''
        bname = 'plunging' if r.breaker == 'plunging' else 'collapsing'
        vcls = {'beyond_extreme': 'beyond extreme', 'very_high': 'very high', 'extreme': 'extreme'}.get(r.vortex_class, r.vortex_class)
        lines = [
            '\u03be$_b$ = %.2f (%s)' % (r.xi_b, bname),
            'Y = %.2f%s (%s)' % (r.vortex_Y, dag, vcls),
        ]
        if pan['slug'] == 'boscombe-surf-reef':
            rs = P['rs']
            lines.append('site wave 0.5 m, 8 s: \u03be$_b$ %.2f, Y %.2f\u2020' % (rs.xi_b, rs.vortex_Y))
        fig.text(L_IN / wcm, ty / hcm, '\n'.join(lines), ha='left', va='top', fontsize=7, linespacing=1.3, color=INK)

    fig.text((L_OV + W_OV / 2) / wcm, 6.02 / hcm, 'Same depth gap (4.5 to 5.5 m), different ramp: 89 m versus 13 m', ha='center', va='center',
             fontsize=7.5, fontweight='bold', color='#7A1F1F')
    handles = [
        Patch(fc=WATER, ec=BLUE, lw=0.6, label='sea'),
        Patch(fc=SAND, ec=SEABED, lw=0.6, label='seabed'),
        Patch(fc='#CBBE9F', ec=INK2, hatch='////', lw=0.4, label='reef'),
        Patch(fc=TIDE, alpha=0.6, lw=0, label='local spring range'),
        Line2D([0], [0], color=RED, lw=0.8, ls=(0, (2, 2)), label='Israeli spring range 0.40 m'),
        Patch(fc=INK, ec=INK, label='surfer, 1.8 m tall'),
    ]
    fig.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.04, -0.005), ncol=6, frameon=False, fontsize=7,
               handlelength=1.5, columnspacing=1.1, handletextpad=0.4)
    return fig


def main():
    paths = S.save(fig3(), 'fig3_wave_sketch')
    print('\n'.join(paths))


if __name__ == '__main__':
    main()
