#!/usr/bin/env python3
"""post_break.py - how far shoreward of the break point a reef keeps the wave breaking (Section 4.3).

Run:    python3 08_paper/analysis/post_break.py
Reads:  reef_inputs.py (profiles from 08_paper/data/profiles/<slug>.json, tidal planes), results_reef_summary.csv (rep_line,
        outcome)
Writes: results_post_break.csv

Method (DERIVED, 1-D, idealised). On each reef's representative line (rep_line of results_reef_summary.csv, i.e. the crest
line or the surf cut) and at low / mid (MSL) / high water, a wave of breaking height Hb = 1.0, 1.5, 2.0 m is taken to break at
the first point from offshore where the depth h <= Hb / 0.78 (McCowan index, as in surf_analysis.py). Shoreward of that
point two measures of the "sustained-breaking length" are computed:
  L_simple : distance to the first point where h > Hb / 0.4, i.e. where the water is deep enough that a wave of the
             breaking height is below the stable height ratio H/h = 0.4 (Dally, Dean & Dalrymple 1985) and stops breaking
             (Hb held constant: an upper bound, since a breaking wave loses height).
  L_dally  : the Dally et al. (1985) energy-flux decay model in shallow-water linear theory, d(H^2 h^0.5)/dx =
             -(K/h) (H^2 h^0.5 - (G h)^2 h^0.5), K = 0.15, G = 0.4, integrated shoreward on the 1 m grid from Hb; breaking
             stops where H <= G h. Green's law shoaling is implied where h changes.
If breaking never stops before the shoreline (h <= 0.05 m) the length is to the shoreline and the flag 'to_shore' is set
(the reef wave joins the beach surf zone). Break points seaward of the reef or on no reef are flagged. Limits: normal
incidence, no refraction or 2-D spreading (a V or narrow arm loses depth sideways too), no set-up, no friction, the
model profile (survey or idealised, see profiles/SUMMARY.md).
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reef_inputs as RI  # noqa: E402
from surf_analysis import prof_arrays  # noqa: E402

H_SET = [1.0, 1.5, 2.0]
GAMMA_B, GAMMA_S, K = 0.78, 0.4, 0.15
H_SHORE = 0.05


def dally_length(y, h, i0, Hb):
    """Distance from index i0 (break) shoreward until H <= GAMMA_S*h (Dally et al. 1985 decay); None if it reaches shore."""
    G = Hb ** 2 * np.sqrt(h[i0])
    for i in range(i0 + 1, len(y)):
        dx = y[i - 1] - y[i]
        hm = 0.5 * (h[i - 1] + h[i])
        if h[i] <= H_SHORE or hm <= H_SHORE:
            return None, i
        Gs = (GAMMA_S * hm) ** 2 * np.sqrt(hm)
        G = G - K / hm * (G - Gs) * dx
        H = np.sqrt(max(G, 0.0) / np.sqrt(h[i]))
        if H <= GAMMA_S * h[i]:
            return y[i0] - y[i], i
    return None, len(y) - 1


def run():
    inp = RI.load()
    summ = {r['slug']: r for r in csv.DictReader(open(os.path.join(HERE, 'results_reef_summary.csv')))}
    rows = []
    for slug, d in inp.items():
        line = summ.get(slug, {}).get('rep_line') or 'crest_line'
        if line not in d['lines']:
            line = 'crest_line'
        y, zb, zr, zs = prof_arrays(d['lines'][line])
        reef = np.isfinite(zr) & (zr > zb + 0.10)
        y_reef_shore = float(y[reef].min()) if reef.any() else float('nan')
        for tide, eta in d['tide_levels'].items():
            if eta is None:
                continue
            h = eta - zs
            for Hb in H_SET:
                r = dict(slug=slug, outcome=summ.get(slug, {}).get('outcome'), line=line, tide=tide, eta_msl_m=round(eta, 3),
                         Hb_m=Hb, h_crest_m=round(float(np.nanmin(h[reef])) if reef.any() else float('nan'), 3))
                hit = np.where(h <= Hb / GAMMA_B)[0]
                if len(hit) == 0:
                    r.update(status='no_break_on_profile')
                    rows.append(r)
                    continue
                i0 = int(hit[0])
                r.update(y_break_m=round(float(y[i0]), 1), h_break_m=round(float(h[i0]), 3),
                         break_on_reef=bool(reef[i0]), status='breaks_on_reef' if reef[i0] else 'breaks_seaward_of_reef',
                         reef_shoreward_of_break_m=round(float(y[i0] - y_reef_shore), 1) if reef.any() else '')
                deep = np.where((h > Hb / GAMMA_S) & (np.arange(len(y)) > i0))[0]
                shore = np.where((h <= H_SHORE) & (np.arange(len(y)) > i0))[0]
                if len(deep) and (not len(shore) or deep[0] < shore[0]):
                    r.update(L_simple_m=round(float(y[i0] - y[deep[0]]), 1), simple_to_shore=False,
                             h_max_after_break_m=round(float(h[i0:deep[0] + 30].max()), 2))
                else:
                    j = shore[0] if len(shore) else len(y) - 1
                    r.update(L_simple_m=round(float(y[i0] - y[j]), 1), simple_to_shore=True,
                             h_max_after_break_m=round(float(h[i0:j + 1].max()), 2))
                L, j = dally_length(y, h, i0, Hb)
                if L is None:
                    r.update(L_dally_m=round(float(y[i0] - y[j]), 1), dally_to_shore=True)
                else:
                    r.update(L_dally_m=round(float(L), 1), dally_to_shore=False)
                rows.append(r)
    return rows


def main():
    rows = run()
    keys = ['slug', 'outcome', 'line', 'tide', 'eta_msl_m', 'Hb_m', 'h_crest_m', 'status', 'y_break_m', 'h_break_m',
            'break_on_reef', 'reef_shoreward_of_break_m', 'L_simple_m', 'simple_to_shore', 'h_max_after_break_m',
            'L_dally_m', 'dally_to_shore']
    with open(os.path.join(HERE, 'results_post_break.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in keys})
    for r in rows:
        if r['tide'] == 'mid' or r['tide'] == 'low':
            print(r['slug'][:14], r['tide'], r['Hb_m'], r['status'], r.get('h_crest_m'), r.get('reef_shoreward_of_break_m'),
                  r.get('L_simple_m'), r.get('simple_to_shore'), r.get('L_dally_m'), r.get('dally_to_shore'))


if __name__ == '__main__':
    main()
