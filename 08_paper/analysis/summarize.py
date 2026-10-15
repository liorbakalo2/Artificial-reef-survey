#!/usr/bin/env python3
"""summarize.py - one row per reef combining parts 1-7 (writes results_reef_summary.csv). Run after the other scripts."""
import csv
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOME_SCORE = {'works': 3, 'works rarely': 2, 'mixed/disputed': 2, 'does not work': 1, 'unknown': None}


def main():
    meta = json.load(open(os.path.join(HERE, 'results_surf.json')))['meta']['site_inputs']
    tw = pd.read_csv(os.path.join(HERE, 'results_tide_window.csv'))
    tw = tw[tw.apply(lambda r: r['T'] == meta[r.slug]['T'], axis=1)]
    size = pd.read_csv(os.path.join(HERE, 'results_size.csv')).set_index('slug')
    peel = pd.read_csv(os.path.join(HERE, 'results_peel.csv'))
    shore = pd.read_csv(os.path.join(HERE, 'results_shoreline.csv')).set_index('slug')
    tr = pd.read_csv(os.path.join(HERE, 'results_transmission.csv'))
    prof = {s: json.load(open(os.path.join(HERE, '..', 'data', 'profiles', s + '.json'))) for s in meta}
    rows = []
    for s, site in meta.items():
        m = prof[s]['lines']['crest_line']['metrics']
        t = tw[(tw.slug == s) & tw.H0.isin([0.5, 1.0, 1.5, 2.0])]
        sf = t.groupby('line')['frac_time_surfable'].mean()
        sfi = t.groupby('line')['frac_time_surfable_israeli_tide'].mean()
        default_lines = [l for l in sf.index if not l.startswith('layer')]
        p = peel[(peel.slug == s) & (peel['T'] == site['T']) & (peel.H0 == site['H']) & ~peel.phi0_src.str.startswith('ALT')]
        k = tr[(tr.slug == s) & (tr['T'] == site['T']) & (tr.H0 == site['H'])].set_index('tide')['Kt']
        sz = size.loc[s]
        rows.append(dict(
            slug=s, outcome=sz['outcome'], outcome_score=OUTCOME_SCORE.get(sz['outcome']),
            crest_depth_msl_m=round(-m['crest_z_msl_m'], 2), relief_m=m.get('crest_height_above_seabed_m'),
            depth_gap_crest_to_toe_bed_m=m.get('crest_to_toe_seabed_drop_m'), ramp_length_m=m.get('ramp_length_m'),
            mean_seaward_slope_1_in=(m.get('mean_seaward_slope') or {}).get('one_in'), max_seaward_slope_1_in=(m.get('max_seaward_slope') or {}).get('one_in'),
            vortex_Y_of_mean_face=0.065 * ((m.get('mean_seaward_slope') or {}).get('one_in') or np.nan) + 0.821,
            H_site=site['H'], T_site=site['T'], spring_range_m=float(t['spring_range'].iloc[0]) if len(t) else None,
            H0_to_break_on_crest_at_msl=sz['H0_needed_to_break_on_crest_msl'], H0_max_before_breaking_seaward_msl=sz['H0_max_before_breaking_seaward_of_reef_msl'],
            surfable_frac_crest_line=sf.get('crest_line'), surfable_frac_best_line=float(sf[default_lines].max()) if default_lines else None,
            surfable_frac_israeli_tide_best_line=float(sfi[default_lines].max()) if default_lines else None,
            peel_alpha_unrefracted_deg=float(p['alpha_no_refraction_deg'].mean()) if len(p) else None,
            peel_alpha_snell_deg=float(p['alpha_break_deg'].mean()) if len(p) else None,
            hutt_rating_range=('%d-%d' % (p['hutt_rating_no_refraction'].min(), p['hutt_rating'].max())) if len(p) else None,
            volume_model_m3=sz['volume_model_m3'], volume_stated_m3=sz['volume_stated_m3'], alongshore_span_m=sz['alongshore_span_m'],
            area_within_1m_of_crest_m2=sz['area_within_1m_of_crest_m2'], crossshore_over_L=sz['crossshore_over_L'],
            Kt_site_low=k.get('low'), Kt_site_mid=k.get('mid'), Kt_site_high=k.get('high'),
            B_over_S=shore.loc[s, 'B_over_S'], salient_pred_m=shore.loc[s, 'salient_Yoff_pred_m'],
            Sa_over_SZW_siteH=shore.loc[s, 'Sa_over_SZW_siteH'], H0_at_ranasinghe_peak=shore.loc[s].get('H0_at_Sa_over_SZW_2')))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, 'results_reef_summary.csv'), index=False, float_format='%.3f')
    ok = df.dropna(subset=['outcome_score'])
    from scipy.stats import spearmanr
    corr = {}
    for c in ['surfable_frac_best_line', 'surfable_frac_crest_line', 'volume_model_m3', 'alongshore_span_m', 'area_within_1m_of_crest_m2',
              'crest_depth_msl_m', 'mean_seaward_slope_1_in', 'ramp_length_m', 'crossshore_over_L']:
        x = ok[[c, 'outcome_score']].dropna()
        if len(x) >= 5:
            r, pval = spearmanr(x[c], x['outcome_score'])
            corr[c] = dict(n=len(x), spearman_rho=round(float(r), 3), p=round(float(pval), 3))
    with open(os.path.join(HERE, 'results_outcome_correlations.json'), 'w') as f:
        json.dump(dict(note='Spearman rank correlation with outcome score (works 3, works rarely / mixed 2, does not work 1; unknown excluded). n is tiny: descriptive only.', corr=corr), f, indent=1)
    print(df[['slug', 'outcome', 'surfable_frac_crest_line', 'surfable_frac_best_line', 'surfable_frac_israeli_tide_best_line', 'hutt_rating_range', 'volume_model_m3']].round(2).to_string(index=False))
    print(json.dumps(corr))


if __name__ == '__main__':
    main()
