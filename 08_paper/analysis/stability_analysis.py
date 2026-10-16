#!/usr/bin/env python3
"""stability_analysis.py - material stability and wave loads (RESULTS.md part 7, insights c and e).

Run:    python3 08_paper/analysis/stability_analysis.py
Writes: results_stability_fk.csv (force / sliding-index ESTIMATE per tube, depth, H), results_fk_calibration.json,
        results_stability_tubes.csv (van Steeg criterion vs depth-limited waves), results_stability_rock.csv (Hudson),
        results_stability.json (all + metadata)

A. ESTIMATE of the Bar & Drimer (2023) sliding index (NOT the BELWF model, whose code is not released): linear (Airy)
   incident-wave pressure integrated over a rigid tube section on the bed (Froude-Krylov; no diffraction, no added mass,
   no nonlinearity), BD23 Eqs. 3-5: SI = Fy / (W' - Fz), SIc = Fy / (W' - Fz - Fc), Fc = L_contact (P_UW + P_DW)/2,
   W' = (rho_fill - rho_w) g A. Section = upper half of a superellipse |2x/B|^p + (z/D)^p = 1, p = 2.5 (ASSUMPTION; the
   Bezuijen & Vastenburg construction is not given as a formula in BD23). L_contact = B (ASSUMPTION). Evaluated over one
   period; the critical value is the maximum |SI|. Calibrated against BD23 read-offs: validation case (two tubes, 12 m wide,
   3.8 m high, h = 5 m, T = 7 s, H = 0.3-1.6 m; Fy, Fz, SI read from Figs. 5-6 via 08_paper/notes/bar_drimer_2023_coverage.md
   s6.4) and design case (single tube 11 x 2.2 m, h = 4 m, T = 9 s, H = 2.86 m; SI ~0.17, SIc ~0.31 from Fig. 11).
B. van Steeg et al. (2011) tube criterion chi Hs / (Delta sqrt(B D) (f cos a + sin a)) <= 0.65, chi = 1, f = 0.5
   (ASSUMPTION), compared with the depth-limited significant wave Hs = 0.55 h (ASSUMPTION gamma_s) at the tube base.
C. Hudson (1959) rock stability, K_D = 2.0 (breaking waves, 2 layers, trunk, SPM 1984 via Verhagen 2012 slide 6).
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

RHO_FILL_BD23 = 2082.0     # [BD23] p.6 wet saturated sand (low-confidence source in BD23)
F_FRICTION = 0.5           # ASSUMPTION tube-on-sand friction (Corvaro et al. 2022 use 0.48 bag-on-bag)
GAMMA_S = 0.55             # ASSUMPTION depth-limited significant wave / depth


def section(B, D, p=2.5, n=241):
    x = np.linspace(-B / 2, B / 2, n)
    f = D * np.clip(1 - np.abs(2 * x / B) ** p, 0, None) ** (1 / p)
    return x, f


def fk_forces(B, D, h, H, T, p=2.5, rho_fill=RHO_FILL_BD23, area=None, nph=96, Wsub=None):
    """Linear Froude-Krylov loads per metre on a bottom-mounted rigid section (bed at z = -h). Returns maxima over phase."""
    k = float(W.wavenumber(T, h))
    x, f = section(B, D, p)
    z = -h + f
    fp = np.gradient(f, x)
    A = float(np.trapezoid(f, x)) if area is None else area
    Wp = (rho_fill - W.RHO_W) * W.G * A if Wsub is None else Wsub
    amp = W.RHO_W * W.G * H / 2 / math.cosh(k * h)
    ph = np.linspace(0, 2 * math.pi, nph, endpoint=False)
    out = dict(Fy=[], Fz=[], Fc=[])
    for w in ph:
        pr = amp * np.cosh(k * (h + z)) * np.cos(k * x - w)
        Fy = float(np.trapezoid(pr * fp, x))           # + onshore
        Fz = float(-np.trapezoid(pr, x))               # + uplift (top surface only)
        pb = amp * np.cos(np.array([k * x[0] - w, k * x[-1] - w]))   # dynamic pressure on the bed at the contact ends
        Fc = B * float(pb.mean())                      # BD23 Eq. 4, + = uplift (ASSUMPTION L_contact = B)
        out['Fy'].append(Fy); out['Fz'].append(Fz); out['Fc'].append(Fc)
    Fy, Fz, Fc = (np.array(out[k_]) for k_ in ('Fy', 'Fz', 'Fc'))
    SI = Fy / (Wp - Fz)
    SIc = Fy / (Wp - Fz - Fc)
    i = int(np.argmax(np.abs(SI)))
    j = int(np.argmax(np.abs(SIc)))
    # 2026-10-16: uplift_fraction uses the top-surface pressure only (no dynamic pressure under the tube = sealed base,
    # upper bound). uplift_fraction_contact adds the BD23 contact term Fc (dynamic pressure reaches the base = lower bound).
    return dict(k=k, kh=k * h, area=A, Wsub_kN=Wp / 1e3, Fy_max_kN=float(np.abs(Fy).max()) / 1e3, Fz_uplift_max_kN=float(Fz.max()) / 1e3,
                Fz_down_max_kN=float(-Fz.min()) / 1e3, SI_max=float(abs(SI[i])), SI_phase_deg=math.degrees(ph[i]),
                SIc_max=float(abs(SIc[j])), uplift_fraction=float(Fz.max()) / Wp,
                uplift_fraction_contact=float((Fz + Fc).max()) / Wp, cycles_per_day=86400.0 / T)


def calibrate():
    """Compare the estimate with the BD23 read-offs; returns factors used to scale the estimate."""
    val = [(0.3, 7, 13, 0.016), (1.0, 28, 48, 0.066), (1.6, 44.5, 64, 0.106)]   # H, Fy, Fz, SI (by eye, +-10 %)
    W_sub_val = 467e3   # N/m: (Fg - Fb) DERIVED from the read-offs (450-485 kN) in bar_drimer_2023_coverage.md s6.4
    rows = []
    for H, Fy_b, Fz_b, SI_b in val:
        r = fk_forces(12.0, 3.8, 5.0, H, 7.0, Wsub=W_sub_val)
        rows.append(dict(case='BD23 validation', H=H, Fy_BELWF_kN=Fy_b, Fy_est_kN=r['Fy_max_kN'], Fz_BELWF_kN=Fz_b,
                         Fz_est_kN=r['Fz_uplift_max_kN'], SI_BELWF=SI_b, SI_est=r['SI_max'],
                         ratio_Fy=Fy_b / r['Fy_max_kN'], ratio_Fz=Fz_b / r['Fz_uplift_max_kN'], ratio_SI=SI_b / r['SI_max']))
    d = fk_forces(11.0, 2.2, 4.0, 2.86, 9.0)
    rows.append(dict(case='BD23 design (near breaking, H/h = 0.72)', H=2.86, SI_BELWF=0.17, SI_est=d['SI_max'], SIc_BELWF=0.31,
                     SIc_est=d['SIc_max'], ratio_SI=0.17 / d['SI_max'], ratio_SIc=0.31 / d['SIc_max'], Wsub_est_kN=d['Wsub_kN'],
                     uplift_fraction_est=d['uplift_fraction']))
    lin = float(np.mean([r['ratio_SI'] for r in rows[:3]]))
    nl = rows[3]['ratio_SI']
    return rows, dict(linear_range_SI_factor=lin, near_breaking_SI_factor=nl, near_breaking_SIc_factor=rows[3]['ratio_SIc'])


# Tubes and containers (B width, D height, m). Sources in 'src'.
TUBES = [
    dict(id='BD23 design tube', B=11.0, D=2.2, src='[BD23] p.10 (11 m wide, 2.2 m high)'),
    dict(id='Narrowneck container (small)', B=3.9, D=1.65, src='reefs.json material: 20 m long, 3-4.5 m diameter (Blacka 2013 A.2.5 p.97); B = 1.3 D_th, D = 0.55 D_th (ASSUMPTION typical filled-tube shape)'),
    dict(id='Narrowneck container (large)', B=5.85, D=2.5, src='as above, D_th = 4.5 m'),
    dict(id='Mount Maunganui container (small)', B=1.5, D=1.0, src='reefs.json material: filled 30 x 1.5 x 1.0 m (Blacka 2013 A.3.3 p.102)'),
    dict(id='Mount Maunganui container (large)', B=7.2, D=3.2, src='reefs.json material: filled 50 x 7.2 x 3.2 m (Blacka 2013 A.3.3 p.102)'),
    dict(id="Pratte's bag", B=2.1, D=1.2, src='reefs.json material: 3.0 x 2.1 x 1.2 m bags (Blacka 2013 A.11.2 p.115)'),
    dict(id='Boscombe T4 container', B=5.2, D=2.2, src='reefs.json material: ~4 m diameter, 65-70 m long, 746.7 m3 (Rendle 2016 Table 5.3 via reefs.json); B, D from D_th = 4 m (ASSUMPTION shape)'),
    dict(id='Israeli geotube (D_th 5 m)', B=6.5, D=2.75, src='State Comptroller 2024 PDF p.9 generic definition: tube up to 5 m diameter, 30 m long (via 08_paper/notes/israel_geotubes_netanya.md s4); Ashkelon sizes not stated; B, D ASSUMPTION shape'),
    dict(id='Israeli geotube (D_th 3 m)', B=3.9, D=1.65, src='ASSUMPTION smaller tube for comparison'),
]


def state_of(U, si, sic):
    """U = peak uplift / submerged weight (linear estimate). SI is singular as U -> 1, so U is reported first."""
    if U >= 1.0:
        return 'lift-off (U >= 1)'
    if U >= 0.8:
        return 'near lift-off (0.8 <= U < 1)'
    if max(si, sic) > F_FRICTION:
        return 'sliding (SI > 0.5)'
    return 'stable (SI <= 0.5, U < 0.8)'


def tube_runs(calib):
    rows = []
    for t in TUBES:
        for h in (2.0, 3.0, 4.0, 5.0, 6.0, 8.0):        # depth at the tube base (m)
            if h <= t['D'] + 0.3:
                continue
            for T in (6.0, 9.0, 12.0):
                Hlim = 0.78 * h
                for H in sorted(set([0.5, 1.0, 1.5, 2.0, 3.0, 4.0, round(Hlim, 2)])):
                    if H > Hlim + 1e-9:
                        continue
                    r = fk_forces(t['B'], t['D'], h, H, T)
                    nb = H / h >= 0.6
                    fac = calib['near_breaking_SI_factor'] if nb else calib['linear_range_SI_factor']
                    facc = calib['near_breaking_SIc_factor'] if nb else calib['linear_range_SI_factor']
                    rows.append(dict(tube=t['id'], B=t['B'], D=t['D'], h_base=h, d_over_crest=h - t['D'], T=T, H=H, H_over_h=H / h,
                                     at_break=bool(abs(H - Hlim) < 1e-6), **{k: v for k, v in r.items() if k not in ('k',)},
                                     SI_calibrated=r['SI_max'] * fac, SIc_calibrated=r['SIc_max'] * facc,
                                     calibration='near-breaking (H/h >= 0.6): BD23 design factor' if nb else 'linear range: BD23 validation factor',
                                     state=state_of(r['uplift_fraction'], r['SI_max'] * fac, r['SIc_max'] * facc),
                                     state_contact=state_of(r['uplift_fraction_contact'], r['SIc_max'] * facc, r['SIc_max'] * facc),
                                     SIc_calibrated_note='contact case: BD23 SIc only (SI without Fc is singular when the top-only uplift nears W)'))
    return rows


def vansteeg_rows():
    rows = []
    for t in TUBES:
        for rho in (RHO_FILL_BD23, 1900.0):
            hc = W.vansteeg_hs_crit(t['B'], t['D'], rho, f=F_FRICTION)
            rows.append(dict(tube=t['id'], B=t['B'], D=t['D'], rho_fill=rho, f=F_FRICTION, chi=1.0, Hs_crit=hc,
                             h_base_where_depth_limited_Hs_equals_crit=hc / GAMMA_S,
                             note='stable where the depth-limited Hs (0.55 h) or the local storm Hs is below Hs_crit; src: ' + t['src']))
    return rows


ROCKS = [
    dict(reef='cables-reef-wa', unit='body granite 1.5 t', M=1500.0, rho=2650.0, src='reefs.json material (Blacka 2013 A.1.3 p.93); rho ASSUMPTION 2650'),
    dict(reef='cables-reef-wa', unit='perimeter granite 3.0 t', M=3000.0, rho=2650.0, src='as above'),
    dict(reef='southern-ocean-surf-reef-albany', unit='armour D50 0.94 m', Dn=0.84 * 0.94, rho=2650.0, src='reefs.json material (design table); Dn50 = 0.84 D50 (ASSUMPTION sieve-to-nominal ratio); rho ASSUMPTION'),
    dict(reef='southern-ocean-surf-reef-albany', unit='core D50 0.49 m', Dn=0.84 * 0.49, rho=2650.0, src='as above'),
    dict(reef='southern-ocean-surf-reef-albany', unit='belly D50 0.16 m', Dn=0.84 * 0.16, rho=2650.0, src='as above'),
    dict(reef='borth-coastal-defence-reef', unit='Type 4 rock 6-10 t (8 t)', M=8000.0, rho=2650.0, src='reefs.json material (card R1)'),
    dict(reef='borth-coastal-defence-reef', unit='Type 1 rock 3-6 t (4.5 t)', M=4500.0, rho=2650.0, src='as above'),
]


def rock_rows(inp):
    rows = []
    for r in ROCKS:
        Dn = r.get('Dn') or (r['M'] / r['rho']) ** (1 / 3)
        M = r.get('M') or r['rho'] * Dn ** 3
        Delta = r['rho'] / W.RHO_W - 1
        met = inp[r['reef']]['lines']['crest_line']['metrics']
        for sl_name in ('mean_seaward_slope', 'max_seaward_slope'):
            tan = (met.get(sl_name) or {}).get('tan')
            if not tan:
                continue
            cot = 1 / tan
            Hst = Delta * Dn * (2.0 * cot) ** (1 / 3)
            rows.append(dict(reef=r['reef'], unit=r['unit'], M_kg=M, Dn50_m=Dn, Delta=Delta, slope=sl_name, cot_alpha=cot,
                             KD=2.0, H_stable_hudson=Hst, depth_where_breaking_H_equals_Hstable=Hst / 0.78,
                             extrapolated=bool(cot > 5.0), src=r['src']))
    return rows


def israel_depth_scan(calib):
    """Sliding-index ESTIMATE for an Israeli geotube vs base depth for storm waves (Hs 3.3 m T 10 s; Hs 5 m T 12 s),
    wave height at the tube = min(H shoaled, 0.78 h) for the maximum individual wave (H = 1.8 Hs ASSUMPTION Rayleigh H1/1000
    is not used; we use Hmax = min(1.8 Hs, 0.78 h))."""
    rows = []
    for t in TUBES[-2:]:
        for Hs, T in ((1.0, 7.0), (3.3, 10.0), (5.0, 12.0)):
            for h in np.arange(t['D'] + 0.5, 16.01, 0.5):
                Hmax = min(1.8 * Hs * float(W.shoaling_coefficient(T, h)), 0.78 * h)
                r = fk_forces(t['B'], t['D'], float(h), Hmax, T)
                nb = Hmax / h >= 0.6
                fac = calib['near_breaking_SI_factor'] if nb else calib['linear_range_SI_factor']
                rows.append(dict(tube=t['id'], Hs_storm=Hs, T=T, h_base=float(h), Hmax=Hmax, depth_limited=bool(Hmax >= 0.78 * h - 1e-6),
                                 SI_est=r['SI_max'], SI_calibrated=r['SI_max'] * fac, uplift_fraction=r['uplift_fraction'],
                                 state=state_of(r['uplift_fraction'], r['SI_max'] * fac, r['SIc_max'] * fac),
                                 uplift_fraction_contact=r['uplift_fraction_contact'],
                                 SIc_calibrated=r['SIc_max'] * (calib['near_breaking_SIc_factor'] if nb else calib['linear_range_SI_factor']),
                                 state_contact=state_of(r['uplift_fraction_contact'], r['SIc_max'] * (calib['near_breaking_SIc_factor'] if nb else calib['linear_range_SI_factor']), r['SIc_max'] * (calib['near_breaking_SIc_factor'] if nb else calib['linear_range_SI_factor'])),
                                 Fy_max_kN=r['Fy_max_kN'], Wsub_kN=r['Wsub_kN'], Hmax_rule='Hmax = min(1.8 Hs Ks, 0.78 h) (ASSUMPTION Rayleigh ~1000 waves)',
                                 Hs_crit_vansteeg=W.vansteeg_hs_crit(t['B'], t['D'], RHO_FILL_BD23, f=F_FRICTION),
                                 Hs_local=min(Hs * float(W.shoaling_coefficient(T, h)), GAMMA_S * h)))
    return rows


def main():
    inp = RI.load()
    cal_rows, calib = calibrate()
    fk = tube_runs(calib)
    vs = vansteeg_rows()
    rk = rock_rows(inp)
    isr = israel_depth_scan(calib)
    SA.write_csv(os.path.join(HERE, 'results_stability_fk.csv'), fk)
    SA.write_csv(os.path.join(HERE, 'results_stability_tubes.csv'), vs)
    SA.write_csv(os.path.join(HERE, 'results_stability_rock.csv'), rk)
    SA.write_csv(os.path.join(HERE, 'results_stability_israel_depth.csv'), isr)
    with open(os.path.join(HERE, 'results_fk_calibration.json'), 'w') as f:
        json.dump(dict(rows=cal_rows, factors=calib), f, indent=1)
    with open(os.path.join(HERE, 'results_stability.json'), 'w') as f:
        json.dump(dict(meta=dict(script='08_paper/analysis/stability_analysis.py', status='ESTIMATE (A, calibrated linear Froude-Krylov, not BELWF) / DERIVED (B, C); see RESULTS.md part 7',
                                 friction=F_FRICTION, gamma_s=GAMMA_S, rho_fill=RHO_FILL_BD23, tubes=TUBES, rocks=ROCKS),
                       calibration=dict(rows=cal_rows, factors=calib), fk=fk, vansteeg=vs, rock=rk, israel_depth=isr), f, indent=1, default=float)
    print(json.dumps(cal_rows, indent=0, default=float)[:2500])
    print(calib)


if __name__ == '__main__':
    main()
