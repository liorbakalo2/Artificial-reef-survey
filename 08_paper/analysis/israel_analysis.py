#!/usr/bin/env python3
"""israel_analysis.py - Israel / Haifa implications (RESULTS.md part 8, insight h).

Run:    python3 08_paper/analysis/israel_analysis.py   (after surf_analysis.py and coastal_analysis.py)
Writes: results_israel_design_sweep.csv (synthetic Haifa reef: crest depth x ramp slope x H x T x tide),
        results_israel_design_summary.csv, results_israel_lst.csv, results_israel_sandtrap.csv, results_israel.json

1. Synthetic Haifa profile (ASSUMPTION: no Haifa bathymetry in the repo): natural bed 1:50 from the MSL line (Haifa Bay
   closure depth ~5 m, Zviely et al. 2009) to 8 m depth; reef crest 10 m wide at depth d_c (m below MSL), crest 200 m
   offshore, seaward ramp of slope s down to the bed, landward slope 1:3. Breaking, Iribarren, vortex ratio, surfable flag
   as in surf_analysis.py (gamma 0.78), Israeli tide +-0.2 m spring / +-0.075 m neap (Rosen 2001) vs a Gold Coast tide
   (Narrowneck planes) for comparison.
2. CERC longshore transport order of magnitude (SPM 1984 / CEM; K = 0.39) for breaking heights 0.5-3 m and angles 5-15 deg,
   compared with the published net 60,000-72,000 m3/yr at the south Carmel coast (Zviely et al. 2007).
3. Sand trap: Black & Andrews (2001) salient (upper bound) and an observation-scaled salient (factor 0-0.5 on the
   amplitude from part 6) for reef lengths 60-150 m at 150-300 m offshore; volume V = 0.5 Y_off D_tot h_active c,
   h_active = closure depth 5 m + berm 1 m (ASSUMPTION), c = 0.3-0.6 (ASSUMPTION plan-to-volume shape factor).
4. Burial: seasonal bed change 1 m (Lior; 0.5-1.5 m) vs reef relief and crest depth; settlement observed at geotextile reefs.
"""
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wavelib as W  # noqa: E402
import reef_inputs as RI  # noqa: E402
import surf_analysis as SA  # noqa: E402

BED_SLOPE = 1 / 50.0
Y_CREST = 200.0
CREST_W = 10.0


def haifa_profile(d_c, s_ramp, bed_slope=BED_SLOPE):
    y = np.arange(-20.0, 501.0, 1.0)
    zb = np.minimum(-bed_slope * y, 0.0 + 0 * y)
    zb = np.where(y < 0, -bed_slope * y * 0 + (-y) * 0.05, zb)   # beach face above MSL landward of y = 0
    zb = np.maximum(zb, -8.0)
    zc = -d_c
    z_ramp = zc - s_ramp * (y - (Y_CREST + CREST_W / 2))
    z_back = zc - (1 / 3.0) * ((Y_CREST - CREST_W / 2) - y)
    zr = np.where(np.abs(y - Y_CREST) <= CREST_W / 2, zc, np.where(y > Y_CREST, z_ramp, z_back))
    zr = np.where(zr > zb + 0.1, zr, np.nan)
    o = np.argsort(-y)
    y, zb, zr = y[o], zb[o], zr[o]
    zs = np.where(np.isfinite(zr), np.maximum(zr, zb), zb)
    ok = np.isfinite(zr)
    toe_i = int(np.argmax(np.where(ok, y, -1e9)))
    back_i = int(np.argmin(np.where(ok, y, 1e9)))
    met = dict(reef_on_line=True, crest_z_msl_m=zc, crest_zone_y_m=[Y_CREST - CREST_W / 2, Y_CREST + CREST_W / 2],
               seaward_toe_y_m=float(y[toe_i]), seaward_toe_reef_z_msl_m=float(zr[toe_i]), seaward_toe_seabed_z_msl_m=float(zb[toe_i]),
               shoreward_toe_y_m=float(y[back_i]), outer_toe_y=float(y[toe_i]), outer_toe_reef_z=float(zr[toe_i]), outer_toe_bed_z=float(zb[toe_i]))
    return y, zb, zr, zs, met


def design_sweep():
    rows, summ = [], []
    lev_i = np.round(np.arange(-0.2, 0.2001, 0.02), 3)
    ser_i = SA.tide_series(0.2, 0.075)[1]
    gc = RI.load()['narrowneck-gold-coast']['tide']
    ser_gc = SA.tide_series(gc['A_spring'], gc['A_neap'], gc.get('z0', 0.0))[1]
    lev_gc = np.round(np.arange(-0.95, 0.951, 0.02), 3)
    for d_c in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
        for s in (1 / 8, 1 / 12, 1 / 16, 1 / 20, 1 / 30):
            y, zb, zr, zs, met = haifa_profile(d_c, s)
            vol_cs = float(np.nansum(np.where(np.isfinite(zr), zr - zb, 0.0)))   # m3 per m of reef length
            for T in (6.0, 7.0, 8.0):
                for H0 in (0.5, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0):
                    res = [SA.analyse_case(y, zb, zr, zs, met, H0, T, float(e)) for e in lev_i]
                    mid = res[len(res) // 2]
                    surf = np.array([SA.is_surfable(r) for r in res])
                    res_gc = [SA.analyse_case(y, zb, zr, zs, met, H0, T, float(e)) for e in lev_gc]
                    surf_gc = np.array([SA.is_surfable(r) for r in res_gc])
                    rows.append(dict(d_c=d_c, ramp_slope=s, ramp_one_in=round(1 / s), T=T, H0=H0, category_msl=mid['category'],
                                     H_break=mid.get('H_break'), d_break=mid.get('d_break'), xi_b=mid.get('xi_b'), vortex_Y=mid.get('vortex_Y'),
                                     breaker=mid.get('breaker'), skill_msl=mid.get('skill'),
                                     frac_surfable_israeli_tide=SA.window_fraction(lev_i, surf, ser_i),
                                     frac_surfable_goldcoast_tide=SA.window_fraction(lev_gc, surf_gc, ser_gc),
                                     reef_cross_section_m2=vol_cs, ramp_length_m=(met['seaward_toe_y_m'] - (Y_CREST + CREST_W / 2))))
            sub = [r for r in rows if r['d_c'] == d_c and r['ramp_slope'] == s and 0.6 <= r['H0'] <= 1.5]
            summ.append(dict(d_c=d_c, ramp_one_in=round(1 / s), n_cases=len(sub),
                             mean_frac_surfable_israeli=float(np.mean([r['frac_surfable_israeli_tide'] for r in sub])),
                             mean_frac_surfable_goldcoast_tide=float(np.mean([r['frac_surfable_goldcoast_tide'] for r in sub])),
                             share_intermediate_msl=float(np.mean([str(r['skill_msl']).startswith('intermediate') for r in sub])),
                             share_advanced_or_expert_msl=float(np.mean([str(r['skill_msl']).startswith(('advanced', 'expert')) for r in sub])),
                             share_too_hollow_msl=float(np.mean([str(r['skill_msl']).startswith('too hollow') for r in sub])),
                             reef_cross_section_m2=sub[0]['reef_cross_section_m2'], ramp_length_m=sub[0]['ramp_length_m'],
                             volume_per_100m_m3=100 * sub[0]['reef_cross_section_m2']))
    return rows, summ


def lst_rows():
    rows = []
    for Hb in (0.5, 1.0, 1.5, 2.0, 3.0):
        for th in (5.0, 10.0, 15.0):
            q = W.cerc_q(Hb, th)
            rows.append(dict(Hb=Hb, theta_b_deg=th, Q_m3_s=q, Q_m3_day=q * 86400,
                             days_to_move_published_net_annual=RI.ISRAEL['lst_m3yr'][0] / (q * 86400)))
    return rows


def sandtrap_rows():
    rows = []
    for B in (60.0, 100.0, 150.0):
        for S in (150.0, 200.0, 300.0):
            ba = W.black_andrews(B, S)
            for scale, lab in ((1.0, 'Black & Andrews (upper bound)'), (0.5, 'observation-scaled x0.5'), (0.25, 'observation-scaled x0.25')):
                yoff = ba['Y_off_m'] * scale
                dtot = yoff / 0.125
                for c in (0.3, 0.6):
                    V = 0.5 * yoff * dtot * (RI.ISRAEL['closure_depth_m'] + 1.0) * c
                    rows.append(dict(B=B, S=S, B_over_S=B / S, basis=lab, Y_off=yoff, D_tot=dtot, shape_c=c, V_m3=V,
                                     years_at_10pct_of_LST=V / (0.1 * RI.ISRAEL['lst_m3yr'][0]),
                                     years_at_30pct_of_LST=V / (0.3 * RI.ISRAEL['lst_m3yr'][0])))
    return rows


def burial_rows(summ):
    rows = []
    for d_c in (0.8, 1.0, 1.2, 1.5):
        for h_toe in (4.0, 5.0, 6.0):
            relief = h_toe - d_c
            for dz in (0.5, 1.0, 1.5):
                rows.append(dict(d_c=d_c, h_toe=h_toe, relief_m=relief, bed_change_m=dz,
                                 relief_after_bed_rise=relief - dz, relief_loss_pct=100 * dz / relief,
                                 gap_toe_minus_crest_after=relief - dz,
                                 crest_depth_after_settlement=d_c + dz,
                                 Hb_needed_after_settlement=0.78 * (d_c + dz), Hb_needed_before=0.78 * d_c))
    return rows


SETTLEMENT_OBS = [
    dict(reef='narrowneck-gold-coast', obs='settlement 1-2 m locally (weir containers up to 2 m)', src='reefs.json durability (Blacka 2013 A.2.5 p.97-98)'),
    dict(reef='prattes-reef-el-segundo', obs='crest dropped 1.5 m in the year after Phase II; bags sank and were buried', src='reefs.json durability (Blacka 2013 A.11 p.116-119)'),
    dict(reef='mount-maunganui-reef', obs='apex bags deflated to -2.0 to -2.4 m CD by 2013; offshore end ~1 m lower after a container slumped', src='reefs.json durability (M&B p.3; Blacka p.72; BoPRC 2013)'),
    dict(reef='boscombe-surf-reef', obs='crest dip ~2 m after the 2011 container failure', src='reefs.json durability (METHODS_3D s1, Rendle & Davidson 2012)'),
    dict(reef='cables-reef-wa', obs='top -1.55 -> -1.71 m AHD 1999-2002, within survey error (rock)', src='reefs.json durability (Blacka 2013 A.1.3)'),
]


def main():
    rows, summ = design_sweep()
    SA.write_csv(os.path.join(HERE, 'results_israel_design_sweep.csv'), rows)
    SA.write_csv(os.path.join(HERE, 'results_israel_design_summary.csv'), summ)
    lst = lst_rows()
    SA.write_csv(os.path.join(HERE, 'results_israel_lst.csv'), lst)
    st = sandtrap_rows()
    SA.write_csv(os.path.join(HERE, 'results_israel_sandtrap.csv'), st)
    bu = burial_rows(summ)
    SA.write_csv(os.path.join(HERE, 'results_israel_burial.csv'), bu)
    with open(os.path.join(HERE, 'results_israel.json'), 'w') as f:
        json.dump(dict(meta=dict(script='08_paper/analysis/israel_analysis.py', status='DERIVED / ASSUMPTION-based design screening; see RESULTS.md part 8',
                                 israel_inputs=RI.ISRAEL, bed_slope=BED_SLOPE, crest_offshore_m=Y_CREST, crest_width_m=CREST_W),
                       design_summary=summ, lst=lst, sandtrap=st, burial=bu, settlement_observed=SETTLEMENT_OBS), f, indent=1, default=float)
    best = sorted(summ, key=lambda r: -r['mean_frac_surfable_israeli'])[:8]
    for r in best:
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == '__main__':
    main()
