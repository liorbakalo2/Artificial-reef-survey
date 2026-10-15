"""Core analysis for extract_profiles.py: profile sampling and geometric metrics (see extract_profiles.py docstring)."""
import math

import numpy as np
from scipy import ndimage as ndi

STEP = 1.0            # m, profile sampling step (task: every 1-2 m)
THK_MIN = 0.10        # m, a reef cell belongs to the footprint if reef surface - natural seabed >= THK_MIN (ASSUMPTION, documented)
CREST_TOL = 0.10      # m, crest zone = contiguous points within CREST_TOL of the line's highest reef point (ASSUMPTION)
TIE_TOL = 0.02        # m, cells within TIE_TOL of the global maximum are 'equally shallowest'; the one nearest the footprint centroid is used
SLOPE_HALF = 1.0      # m, max slope = central difference over +-SLOPE_HALF (2 m baseline)
PAD_SEA = 150.0       # m, profile extends this far seaward of the most offshore reef toe (or to the end of the seabed domain)
LAND_LIMIT = -50.0    # m, profile starts at most this far landward of the model shoreline y = 0


def rnd(a, nd=3):
    a = np.asarray(a, float)
    return [None if not np.isfinite(v) else round(float(v), nd) for v in a]


def sample_reef(rx, ry, RZ, x, y):
    """Normalised bilinear sample of the reef surface (NaN-aware); NaN where fewer than half of the 4 neighbours exist."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    x, y = np.broadcast_arrays(x, y)
    fx = (x - rx[0]) / (rx[1] - rx[0])
    fy = (y - ry[0]) / (ry[1] - ry[0])
    fin = np.isfinite(RZ)
    num = ndi.map_coordinates(np.where(fin, RZ, 0.0), [fy.ravel(), fx.ravel()], order=1, mode='constant', cval=0.0)
    den = ndi.map_coordinates(fin.astype(float), [fy.ravel(), fx.ravel()], order=1, mode='constant', cval=0.0)
    with np.errstate(invalid='ignore', divide='ignore'):
        out = np.where(den >= 0.5, num / den, np.nan)
    return out.reshape(x.shape)


def footprint(rx, ry, RZ, seabed, mask=None):
    X, Y = np.meshgrid(rx, ry)
    SB = seabed(X, Y)
    TH = RZ - SB
    foot = np.isfinite(RZ) & (TH >= THK_MIN)
    if mask is not None:
        foot &= mask(X, Y)
    return X, Y, SB, TH, foot


def crest_and_centre(rx, ry, RZ, X, Y, foot):
    zmax = float(np.nanmax(np.where(foot, RZ, np.nan)))
    cand = foot & (RZ >= zmax - TIE_TOL)
    cx, cy = X[foot].mean(), Y[foot].mean()          # area centroid of the footprint
    d = np.hypot(X[cand] - X[cand].mean(), Y[cand] - Y[cand].mean())
    # tie-break: candidate cell nearest the centroid of the candidate set (the 'middle' of the shallowest plateau)
    k = int(np.argmin(d))
    xc, yc = float(X[cand][k]), float(Y[cand][k])
    cols = np.where(foot.any(axis=0))[0]
    x_lo, x_hi = float(rx[cols[0]]), float(rx[cols[-1]])
    rows = np.where(foot.any(axis=1))[0]
    y_lo, y_hi = float(ry[rows[0]]), float(ry[rows[-1]])
    dx = float(rx[1] - rx[0])
    return dict(zmax=zmax, x_crest=xc, y_crest=yc, x_centre=0.5 * (x_lo + x_hi), x_centroid=float(cx), y_centroid=float(cy),
                x_range=[x_lo, x_hi], y_range=[y_lo, y_hi], area_m2=float(foot.sum() * dx * (ry[1] - ry[0])), dx=dx)


def alongshore_length(rx, RZ, foot, level):
    """Alongshore extent (model x) of the part of the footprint whose surface is at or above `level` (m MSL):
    span = x_max - x_min of such cells; union = (number of x-columns containing such a cell) * dx."""
    sel = foot & (RZ >= level)
    if not sel.any():
        return dict(level_msl_m=round(float(level), 3), span_m=None, union_m=None, note='no reef cell at or above this level')
    cols = np.where(sel.any(axis=0))[0]
    dx = float(rx[1] - rx[0])
    return dict(level_msl_m=round(float(level), 3), span_m=round(float((cols[-1] - cols[0]) * dx + dx), 2), union_m=round(float(len(cols) * dx), 2),
                x_min_m=round(float(rx[cols[0]]), 2), x_max_m=round(float(rx[cols[-1]]), 2))


def msl_crossing(y, zs):
    """First downward crossing of z = 0 (MSL) moving offshore along the natural-seabed profile (linear interpolation)."""
    ok = np.isfinite(zs)
    for k in range(len(y) - 1):
        if ok[k] and ok[k + 1] and zs[k] > 0 >= zs[k + 1]:
            return float(y[k] + (0 - zs[k]) * (y[k + 1] - y[k]) / (zs[k + 1] - zs[k]))
    return None


def runs(inrun):
    out = []
    k = 0
    n = len(inrun)
    while k < n:
        if inrun[k]:
            j = k
            while j + 1 < n and inrun[j + 1]:
                j += 1
            out.append((k, j))
            k = j + 1
        else:
            k += 1
    return out


def slope_stats(y, z, k0, k1):
    """max slope (positive = deeper seaward, i.e. surface falls with increasing y) by central difference +-SLOPE_HALF between indices k0..k1"""
    h = int(round(SLOPE_HALF / (y[1] - y[0])))
    best, kb = None, None
    for k in range(max(k0, h), min(k1, len(y) - 1 - h) + 1):
        a, b = z[k - h], z[k + h]
        if np.isfinite(a) and np.isfinite(b):
            s = (a - b) / (y[k + h] - y[k - h])
            if best is None or s > best:
                best, kb = s, k
    return best, kb


def fmt_slope(s):
    if s is None or not np.isfinite(s) or s <= 0:
        return dict(tan=None, deg=None, one_in=None)
    return dict(tan=round(float(s), 4), deg=round(math.degrees(math.atan(s)), 2), one_in=round(1.0 / s, 2))


def line_metrics(y, zs, zr):
    th = zr - zs
    inrun = np.isfinite(zr) & (th >= THK_MIN)
    if not inrun.any():
        return dict(reef_on_line=False)
    segs = runs(inrun)
    kmax = int(np.nanargmax(np.where(inrun, zr, -np.inf)))
    seg = next(s for s in segs if s[0] <= kmax <= s[1])
    i0, i1 = seg
    # crest zone: contiguous around kmax within CREST_TOL of the max
    zmax = float(zr[kmax])
    c0 = kmax
    while c0 - 1 >= i0 and zr[c0 - 1] >= zmax - CREST_TOL:
        c0 -= 1
    c1 = kmax
    while c1 + 1 <= i1 and zr[c1 + 1] >= zmax - CREST_TOL:
        c1 += 1
    step = float(y[1] - y[0])
    ramp_len = float(y[i1] - y[c1])
    rise = float(zr[c1] - zr[i1])
    msl = msl_crossing(y, zs)
    smax, ksm = slope_stats(y, zr, c1, i1)
    # shoreward face
    sh_len = float(y[c0] - y[i0])
    sh_rise = float(zr[c0] - zr[i0])
    out = dict(
        reef_on_line=True,
        crest_z_msl_m=round(zmax, 3), crest_y_m=round(float(y[kmax]), 2), crest_depth_below_msl_m=round(-zmax, 3),
        crest_seabed_z_msl_m=round(float(zs[kmax]), 3), crest_height_above_seabed_m=round(float(zr[kmax] - zs[kmax]), 3),
        crest_zone_y_m=[round(float(y[c0]), 2), round(float(y[c1]), 2)], crest_zone_width_m=round(float(y[c1] - y[c0] + step), 2),
        seaward_toe_y_m=round(float(y[i1]), 2), seaward_toe_reef_z_msl_m=round(float(zr[i1]), 3), seaward_toe_seabed_z_msl_m=round(float(zs[i1]), 3),
        seaward_toe_thickness_m=round(float(zr[i1] - zs[i1]), 3),
        ramp_length_m=round(ramp_len, 2), ramp_rise_m=round(rise, 3),
        mean_seaward_slope=fmt_slope(rise / ramp_len) if ramp_len > 0 else fmt_slope(None),
        max_seaward_slope=fmt_slope(smax), max_seaward_slope_at_y_m=None if ksm is None else round(float(y[ksm]), 2),
        shoreward_toe_y_m=round(float(y[i0]), 2), shoreward_toe_reef_z_msl_m=round(float(zr[i0]), 3), shoreward_toe_seabed_z_msl_m=round(float(zs[i0]), 3),
        shoreward_ramp_length_m=round(sh_len, 2), shoreward_ramp_rise_m=round(sh_rise, 3),
        mean_shoreward_slope=fmt_slope(sh_rise / sh_len) if sh_len > 0 else fmt_slope(None),
        reef_cross_shore_extent_m=round(float(y[i1] - y[i0] + step), 2),
        max_thickness_on_line_m=round(float(np.nanmax(np.where(inrun, th, np.nan))), 3),
        y_msl_crossing_m=None if msl is None else round(msl, 2),
        segments=[dict(y_from_m=round(float(y[a]), 2), y_to_m=round(float(y[b]), 2), max_z_msl_m=round(float(np.nanmax(zr[a:b + 1])), 3)) for a, b in segs],
    )
    if msl is not None:
        out['crest_distance_from_msl_line_m'] = round(float(y[kmax]) - msl, 2)
        out['seaward_toe_distance_from_msl_line_m'] = round(float(y[i1]) - msl, 2)
        out['shoreward_toe_distance_from_msl_line_m'] = round(float(y[i0]) - msl, 2)
        if y[i1] > msl:
            out['seabed_mean_slope_msl_line_to_seaward_toe'] = fmt_slope((0.0 - float(zs[i1])) / (float(y[i1]) - msl))
        if y[i0] > msl:
            out['seabed_mean_slope_msl_line_to_shoreward_toe'] = fmt_slope((0.0 - float(zs[i0])) / (float(y[i0]) - msl))
    # natural seabed slope seaward of the reef (toe -> toe + 100 m)
    yt = float(y[i1])
    j = int(np.argmin(np.abs(y - (yt + 100.0))))
    if abs(y[j] - (yt + 100.0)) < 1e-6 and np.isfinite(zs[j]):
        out['seabed_mean_slope_seaward_of_toe_100m'] = fmt_slope((float(zs[i1]) - float(zs[j])) / 100.0)
    return out
