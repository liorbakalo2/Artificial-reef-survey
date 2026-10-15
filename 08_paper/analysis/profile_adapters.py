"""Per-reef adapters for extract_profiles.py.

Each adapter reads ONLY the published model data of one reef (07_scale/shapes/<slug>/3d/model.js, read only) and
returns a dict with
    seabed   : callable (x, y) -> natural-seabed elevation, m above MSL (NaN outside the model's seabed domain)
    rx, ry   : 1-D arrays, node coordinates of the reef-surface grid (m, model frame)
    RZ       : 2-D array [len(ry), len(rx)], reef-surface elevation, m above MSL (NaN where the model has no reef)
    meta     : dict with version, datum, frame, shoreline definition, source/method text, caveats
The reef-surface rules that are evaluated at run time inside the 3D viewers (Prattes, Bunbury, Mount Maunganui, Albany)
are re-implemented here, line by line, from the viewer code / build_3d.py (cited in meta['method']).
Frame of every model: x alongshore, y offshore (away from the model shoreline y = 0), z up, 0 = MSL.
"""
import base64
import json
import math
import os

import numpy as np
from scipy import ndimage as ndi

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SHAPES = os.path.join(REPO, '07_scale', 'shapes')


def load_model(slug):
    p = os.path.join(SHAPES, slug, '3d', 'model.js')
    t = open(p, encoding='utf-8').read()
    i = t.index('window.REEF_MODEL')
    j = t.index('=', i) + 1
    s = t[j:].strip()
    if s.endswith(';'):
        s = s[:-1]
    return json.loads(s), p


def b64_i16(s, ny, nx):
    a = np.frombuffer(base64.b64decode(s), dtype='<i2').reshape(ny, nx).astype(float)
    a[a == -32768] = np.nan
    return a / 100.0


def b64_u8(s, ny, nx):
    return np.frombuffer(base64.b64decode(s), dtype=np.uint8).reshape(ny, nx)


class GridFn:
    """Bilinear interpolation on a regular grid Z[j, i] (j along y, i along x); NaN outside the grid."""

    def __init__(self, x0, y0, dx, dy, Z):
        self.x0, self.y0, self.dx, self.dy = float(x0), float(y0), float(dx), float(dy)
        self.Z = np.asarray(Z, float)
        self.ny, self.nx = self.Z.shape

    def __call__(self, x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        fx = (x - self.x0) / self.dx
        fy = (y - self.y0) / self.dy
        out = ndi.map_coordinates(self.Z, [fy.ravel(), fx.ravel()], order=1, mode='nearest').reshape(x.shape)
        bad = (fx < -1e-9) | (fx > self.nx - 1 + 1e-9) | (fy < -1e-9) | (fy > self.ny - 1 + 1e-9)
        return np.where(bad, np.nan, out)

    @property
    def x_range(self):
        return (self.x0, self.x0 + (self.nx - 1) * self.dx)

    @property
    def y_range(self):
        return (self.y0, self.y0 + (self.ny - 1) * self.dy)


def rows_grid(sb):
    """model.js seabed {x0,y0,step|dx,z:[rows of y][cols of x]} -> GridFn"""
    dx = sb.get('step', sb.get('dx'))
    dy = sb.get('step', sb.get('dy', dx))
    return GridFn(sb['x0'], sb['y0'], dx, dy, np.array(sb['z'], float))


def flat_grid(sb, key='z_cm', dx_key='dx'):
    nx, ny = sb['nx'], sb['ny']
    Z = np.array(sb[key], float).reshape(ny, nx) / 100.0
    return GridFn(sb['x0'], sb['y0'], sb[dx_key], sb.get('dy', sb[dx_key]), Z)


def ax(x0, step, n):
    return x0 + step * np.arange(n)


# ---------------------------------------------------------------------------------------------------------- Borth
def borth(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    Zn = b64_u8(g['zone_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ, zone=Zn,
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL; MSL = +0.31 mODN (+-0.15, estimate); z_MSL = z_ODN - 0.31 (model.js datum.equation)',
            frame='x alongshore (+ toward SOUTH, bearing 179.57 deg T); y offshore (+ toward WEST, bearing 269.57 deg T); origin = foot of the perpendicular from the centroid of both mounds on the defence line',
            shoreline_def='y = 0 is the DEFENCE LINE (back of the shingle beach, z about +4.9 m MSL), NOT the MSL waterline. The MSL waterline is where the modelled natural seabed crosses z = 0 (computed per line, key y_msl_crossing_m).',
            reef_surface_def='model.js versions[lidar_2022].grid.h_cm_b64 (int16 cm, z_MSL, 1 m cells, rows = y, cols = x): 1 m LiDAR DSM (Welsh Government, flown 19 Mar 2022, lightly smoothed) inside the exposed-rock outline, plus the Royal Haskoning toe berm / blanket slopes (drawings 9V5090/1021-1023) down to the modelled seabed. Zones: 1 armour, 2 toe berm, 3 blanket/apron.',
            seabed_def='model.js seabed (5 m grid, z_MSL): thin-plate/RBF fit to the Royal Haskoning drawing nodes + Fig. 2 contours (build_3d.py seabed_grid).',
            source_files=['07_scale/shapes/borth-coastal-defence-reef/3d/model.js', '07_scale/shapes/borth-coastal-defence-reef/3d/build_3d.py (lines 62-130)', '07_scale/shapes/borth-coastal-defence-reef/3d/METHODS_3D.md'],
            caveats=['The 1 m LiDAR DSM sees block tops, about 0.1-0.3 m above the design surface (model.js versions[0].note).',
                     'The default 3D confidence is MEDIUM; bed under the reef is interpolated from design drawings, Fig. 2 contours and checked against Navionics (datum +-0.6 m).',
                     'The model has TWO structures: northern boot-shaped surf reef (crest +0.50 mODN) and southern oval shore-parallel breakwater (crest +1.50 mODN) which is NOT a surf reef. Reef metrics below are for the whole footprint incl. both unless a mask is given; the surf reef is the northern one (x < 0).'],
            region_masks={'surf_reef_north': 'x < 0 (model.js roles.north centroid x = -38.9)', 'breakwater_south': 'x > 0 (roles.south centroid x = 85.3)'},
        ))


# -------------------------------------------------------------------------------------------------------- Boscombe
def boscombe(m, mp):
    sb = m['seabed']
    Zsb = np.array(sb['z_cm'], float).reshape(sb['ny'], sb['nx']) / 100.0
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], Zsb)
    code = np.frombuffer(sb['code'].encode(), dtype=np.uint8).reshape(sb['ny'], sb['nx']) - 48
    rg = m['reef']['grid']
    nodata = rg['nodata']
    Z = np.array(rg['idealised_z_cm'], float).reshape(rg['ny'], rg['nx'])
    Z[Z == nodata] = np.nan
    Z /= 100.0
    surveyed = np.array(rg['surveyed_z_cm'], float).reshape(rg['ny'], rg['nx'])
    surveyed[surveyed == nodata] = np.nan
    surveyed /= 100.0
    return dict(
        seabed=seabed, rx=ax(rg['x0'], rg['dx'], rg['nx']), ry=ax(rg['y0'], rg['dy'], rg['ny']), RZ=Z,
        seabed_code=GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], code.astype(float)),
        evidence=dict(name='surveyed_surface_2011-04', RZ=surveyed, note='April 2011 DGPS surface (Rendle and Davidson 2012 Fig. 9, colour read) AFTER the container failure; evidence layer only, not the default'),
        meta=dict(
            version_id='idealised', version_name='AS-BUILT 2009 (intact): idealised loft of the verified outline, design crest +0.5 m ACD', version_date='2009 (Sept-Oct 2009 completion)',
            datum='z = metres above MSL; model assumes the survey zero is Admiralty Chart Datum (ACD) with MSL = ACD + 1.40 m (Ordnance Datum - 1.40 m at Bournemouth, NTSLF), so z_MSL = z_ACD - 1.40; the alternative reading (survey zero = ODN) shifts survey heights by +1.40 m',
            frame='x alongshore (true bearing 83.4 deg, toward the east; Boscombe Pier at negative x); y offshore (true bearing 173.4 deg); origin on the 2011-09-28 surf line nearest the reef centroid',
            shoreline_def='y = 0 is the surf line visible in the 2011-09-28 Esri image (tide state unknown); it lies about 8 m SEAWARD of the modelled MSL waterline (z = -0.2 m at the line) (model.js shoreline.note). The MSL crossing is computed per line (y_msl_crossing_m).',
            reef_surface_def='model.js reef.grid.idealised_z_cm (1 m cells, z_MSL): relief = clip(1 + phi/3.0, 0, crest - seabed), phi = signed distance from the verified outline (m, + inside), crest = design +0.5 m ACD = -0.9 m MSL (flat), outline on the 1 m relief contour (reef.idealised_rule). The viewer re-applies the same cap; with datumShift = 0 (default) the stored grid is what is drawn.',
            seabed_def='model.js seabed.z_cm (2 m grid, z_MSL): April 2011 DGPS plot colour read (Rendle and Davidson 2012 Fig. 9) in the survey area; thin-plate-spline infill under the reef; CCO beach profiles (2010-04-20) landward; EMODnet-slope extrapolation y > 380 m (seabed_source_code: 0 survey, 1 extrapolated, 2 interpolated under reef, 3 CCO beach, 4 CCO-survey blend, 5 EMODnet slope).',
            source_files=['07_scale/shapes/boscombe-surf-reef/3d/model.js', '07_scale/shapes/boscombe-surf-reef/3d/index.html (lines 195-262)', '07_scale/shapes/boscombe-surf-reef/3d/build_3d.py (lines 105-135, 405-410)'],
            caveats=['The default reef surface is an idealised flat-crest loft (crest level = design value +0.5 m ACD), not a survey: the real Oct 2009 profile tops were +0.05..+0.65 m ACD (model.js provenance).',
                     'Slope of the loft flanks (1:3) is an assumption (SLOPE_RUN_PER_RISE = 3.0, source S2); real flanks of the April 2011 DGPS surface have median gradient 0.172 (about 1:5.8) (stats.flank_gradient_median_survey).',
                     'Survey datum is assumed to be chart datum (ACD) - not stated in the source; a +1.4 m alternative exists.'],
        ))


# --------------------------------------------------------------------------------------------------------- Bunbury
def bunbury(m, mp):
    sb = m['seabed']
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], np.array(sb['z'], float))
    R = m['reef']
    cx, cy = R['centre_default']
    H = R['height_default_m']
    poly = np.array(R['toe_polygon_m'], float)
    # radial function of the traced polygon about its own centre (index.html RAD_R: ray/segment intersection)
    NR = 720
    rad = np.full(NR, np.nan)
    for mm in range(NR):
        th = 2 * math.pi * mm / NR
        dxr, dyr = math.cos(th), math.sin(th)
        best = np.inf
        for k in range(len(poly)):
            a, b = poly[k], poly[(k + 1) % len(poly)]
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = dxr * ey - dyr * ex
            if abs(den) < 1e-12:
                continue
            t = (a[0] * ey - a[1] * ex) / den
            u = (a[0] * dyr - a[1] * dxr) / den
            if t > 0 and 0 <= u <= 1 and t < best:
                best = t
        rad[mm] = best
    step = 0.25
    rx = np.arange(cx - 8, cx + 8 + 1e-9, step)
    ry = np.arange(cy - 8, cy + 8 + 1e-9, step)
    X, Y = np.meshgrid(rx, ry)
    dxx, dyy = X - cx, Y - cy
    r = np.hypot(dxx, dyy)
    th = np.mod(np.arctan2(dyy, dxx), 2 * math.pi)
    R_th = np.interp(th, np.append(2 * math.pi * np.arange(NR) / NR, 2 * math.pi), np.append(rad, rad[0]))
    s = r / R_th
    a0 = 6.0
    Rs = (a0 * a0 + H * H) / (2 * H)
    cap = np.sqrt(np.maximum(Rs * Rs - (a0 * s) ** 2, 0.0)) - (Rs - H)
    RZ = np.where(s <= 1.0, seabed(X, Y) + cap, np.nan)
    return dict(
        seabed=seabed, rx=rx, ry=ry, RZ=RZ,
        meta=dict(
            version_id='installed_Dec2019_spherical_cap', version_name='Installed bladder, December 2019 (torn before completion): symmetric spherical-cap stand-in, 12 m diameter, H = 2.0 m', version_date='2019-12-09..13',
            datum='z = metres above MSL; MSL = +0.1 m AHD (GHD 2021 Table 1, Port of Bunbury, rounded 0.1 m); z_MSL = z_AHD - 0.1',
            frame='x alongshore (true bearing 12.32 deg), y seaward from the fitted 0 m AHD contour of the 2009 lidar (bearing 282.32 deg), z up',
            shoreline_def='y = 0 is the fitted 0 m AHD contour of the 2009 lidar (about the MSL waterline, MSL = +0.1 m AHD; rms scatter 8.4 m) (model.js shoreline.definition).',
            reef_surface_def='z = lidar seabed(x, y) + capZ(s, H) with s = r / R_rim(theta) (rim from the traced 29-vertex polygon), capZ(t, H) = sqrt(Rs^2 - (6t)^2) - (Rs - H), Rs = (36 + H^2) / (2H) (index.html function capZ, buildReef with asymmetry 0). The viewer adds a +0.03 m rendering lift which is NOT included here. Default centre y = 37.5 m, H = 2.0 m (reef.height_default_m; text range 1.6-2.0 m).',
            seabed_def='model.js seabed (5 m grid resampled from the 10 m 2009 WA DoT airborne-lidar grid, z_MSL = AHD - 0.1; gap-filled cells flagged), vertical uncertainty +-0.5 m; default bed = lidar (state.bed = lidar).',
            source_files=['07_scale/shapes/bunbury-airwave/3d/model.js', '07_scale/shapes/bunbury-airwave/3d/index.html (lines 199-217, 382-425)'],
            caveats=['NOT a working reef: the bladder tore along a glued seam during installation (13 Dec 2019) and was removed; geometry is an idealised cap stand-in with height 1.6-2.0 m from pre-installation text, profile shape ASSUMED.',
                     'Offshore position 37.5 m from shoreline is the shape.json value; texts give 30-50 m (reef.offshore_presets).',
                     'Crest depth stated in text: about 1 m below surface at low tide (RWR, datum undefined) - compare with the modelled crest.'],
        ))


# ---------------------------------------------------------------------------------------------------------- Cables
def cables(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ,
        true_shoreline=dict(
            # DERIVED, see extract_profiles.py: fitted 0 m AHD line bearing 7.8 deg T, 254 m due east of the anchor (centroid of original plan, canonical x 3.738, y 271.446 => model x -3.738)
            anchor_model=(-3.738, 271.446), x_bearing=170.3, y_bearing=260.3, shore_bearing=7.8, dist_east_m=254.0),
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL, MSL taken = AHD (A12). Surveyed versions are in AHD directly. Design versions: reading A (default for design) z_MSL = z_RL - 0.716 (Fremantle LWD to AHD, DNM TR12 Table 3, +-0.04 m); reading B: z_MSL = z_RL.',
            frame='x alongshore (+ toward SOUTH, bearing 170.3 deg T; x_model = -x_canonical); y offshore (+ toward WEST, bearing 260.3 deg T). The frame is the design-drawing frame rotated 9.74 deg ccw from true north: it is NOT shore-normal (fitted shoreline bearing 7.8 deg T, i.e. the y axis is about 17.5 deg off the shore normal).',
            shoreline_def='y = 0 is the NOMINAL origin line of the design frame (centroid of the original footprint at y = 271 m, Pattiaratchi 1999 / Blacka 2013), not the surveyed shoreline. The surveyed 0 m AHD line (fitted line, bearing 7.8 deg T) lies 254 m due east of the anchor (centroid) (shore_and_datum.py); y_true_shoreline is DERIVED from that (see derived_true_shoreline). The seabed grid starts at y = 190 m, so the MSL crossing is not in the model.',
            reef_surface_def='model.js versions[survey_surface_1999_11].grid.h_cm_b64 (int16 cm, z_MSL=AHD, 0.5 m cells, x already flipped to the model frame): rock thickness = DoT WA singlebeam soundings of 22 Nov 1999 (840 soundings, AHD) minus the measured 30 Mar 1998 pre-construction bed, linearly interpolated between sounding lines inside the original-plan footprint + 6 m, Gaussian-smoothed 1 m; footprint = the georeferenced Lyons (1992) original-plan outline (4,049 m2).',
            seabed_def='model.js seabed (5 m grid, y 190-420 m, x -150..150 m): DoT WA singlebeam of 30 Mar 1998 (pre-construction) inside the survey, Perth_5m composite elsewhere; AHD = MSL.',
            source_files=['07_scale/shapes/cables-reef-wa/3d/model.js', '07_scale/shapes/cables-reef-wa/3d/build_3d.py (lines 30-62, 120-140)', '07_scale/shapes/cables-reef-wa/3d/index.html (lines 148-175)', '07_scale/shapes/cables-reef-wa/HANDOFF.md', '07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md section 3.6'],
            caveats=['Default surface is a MEASURED single-beam survey (+-0.3 m, interpolated between ~5 m sounding lines, smoothed 1 m) of the month before completion (Nov 1999): crest top -1.55 m AHD, highest sounding -1.40 m. Feb 2002 survey: -1.71 / -1.67 m.',
                     'Footprint is the original design outline; the drawn south-arm extension is NOT confirmed (23 soundings).',
                     'Footprint edge cells keep a non-zero rock thickness (survey interpolation within the outline), so the surface does not taper to zero at the toe.',
                     'Design crest RL -1.0 = -1.72 m AHD (reading A) or -1.00 m (B); the surveyed surface is 0.13-0.22 m higher than reading A (physical/survey, not datum).'],
        ))


# ----------------------------------------------------------------------------------------------------- Mount Maunganui
def mount_maunganui(m, mp):
    MSL = m['datum']['msl_above_cd_m']
    SB = m['seabed']
    R = m['reef']
    GR = R['grid']
    ZC = R['zc_cd']
    YC = SB['y_ref']
    KY = np.array([k[0] for k in SB['knots_cd']], float)
    KZ = np.array([k[1] for k in SB['knots_cd']], float)

    def pnav(y):
        y = np.asarray(y, float)
        out = np.interp(y, KY, KZ)
        out = np.where(y >= KY[-1], KZ[-1] + (y - KY[-1]) * (KZ[-1] - KZ[-2]) / (KY[-1] - KY[-2]), out)
        out = np.where(y < 0, MSL - y / SB['beach_run_per_rise'], out)
        return out

    ZREF = float(pnav(YC))
    bed = SB['bed_default_cd']       # -3.6 m CD (ASSUMPTION, Lior decision D1)

    def bedCD(y):
        w = np.clip((np.asarray(y, float) - SB['w_y0']) / (YC - SB['w_y0']), 0, 1)
        return pnav(y) + (bed - ZREF) * w

    def seabed(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        ext = SB['extent']
        z = bedCD(y) - MSL
        bad = (y < ext['y'][0]) | (y > ext['y'][1]) | (x < ext['x'][0]) | (x > ext['x'][1])
        return np.where(bad, np.nan, z)
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    nx, ny = GR['nx'], GR['ny']
    inner = np.array(R['inner_per_mille'], float).reshape(ny, nx)
    flank = np.array(ver['flank'], float).reshape(ny, nx)
    crest = R['crest_cd']['default']
    run = ver.get('run_default', 1.0)
    rxs = ax(GR['x0'], GR['dx'], nx)
    rys = ax(GR['y0'], GR['dx'], ny)
    S = np.repeat(bedCD(rys)[:, None], nx, axis=1)
    Z = S.copy()
    msk = inner >= 0
    Z[msk] = ZC + inner[msk] / 1000.0 * (crest - ZC)
    mf = (~msk) & (flank >= 0)
    if ver['rule'] == 'skirt':
        Z[mf] = np.maximum(S[mf], ZC - flank[mf] / 100.0 / run)
    else:
        Z[mf] = np.maximum(S[mf], S[mf] + (ZC - S[mf]) * flank[mf] / 1000.0)
    Hh = np.maximum(0, Z - S)
    RZ = np.where(Hh > 0.005, Z - MSL, np.nan)
    ev = m['survey2013']
    g2 = ev['grid']
    ZZ = np.array(ev['z_msl_cm'], float).reshape(g2['ny'], g2['nx'])
    ZZ[ZZ == ev['nodata']] = np.nan
    ZZ /= 100.0
    return dict(
        seabed=seabed, rx=rxs, ry=rys, RZ=RZ,
        evidence=dict(name='multibeam_2013-07-18_DEM_from_BoPRC_Fig5', rx=ax(g2['x0'], g2['dx'], g2['nx']), ry=ax(g2['y0'], g2['dy'] if 'dy' in g2 else g2['dx'], g2['ny']), RZ=ZZ,
                      note='18 Jul 2013 multibeam DEM decoded from the hue of BoPRC Fig. 5 (colour-read, see model.js survey2013.note); evidence layer, 5 years after completion, not the default'),
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above present MSL; MSL = Chart Datum + 1.13 m (LINZ Tauranga 2026-27 standard port levels); z_MSL = z_CD - 1.13; MVD-53 = CD + 0.9622 m (NIWA 2006)',
            frame='x alongshore (true bearing 316.15 deg, toward NW / Mauao side); y offshore (true bearing 46.15 deg, shore-normal, toward NE); origin = point on the wet/dry-sand shoreline (Esri 2011-01-15) nearest the survey-outline centroid',
            shoreline_def='y = 0 is the wet/dry-sand boundary of the Esri 2011-01-15 image; the seabed rule starts at y = 0 with z = MSL (first knot (0, 1.13 m CD)), so y = 0 is also the MSL line of the modelled profile by construction. Landward (y < 0) a schematic 1:15 beach (not sourced).',
            reef_surface_def='Re-implementation of index.html computeField(): inside the -2.0 m CD polygons of the 18 Jul 2013 multibeam survey z_CD = ZC + r/1000 (crest - ZC) with ZC = -2.0 m CD, crest = -0.9 m CD (reef.crest_cd.default), r from reef.inner_per_mille (2013 DEM median rise table scaled to 1.10 m); outside: skirt z_CD = max(S, ZC - dout/run), run 1.0 (H:V = 1:1, ASSUMPTION), dout = distance from the -2.0 m contour (versions[].flank, cm); z_MSL = z_CD - 1.13. Grid 0.5 m. Reef cells = height above local bed > 0.005 m.',
            seabed_def='Alongshore-UNIFORM cross-shore profile (no x dependence): S(y) = Pnav(y) + (bed - Pnav(y_ref)) * clamp((y - 111.2)/(y_ref - 111.2), 0, 1) in m CD, Pnav = Navionics SonarChart 2026 contour crossings (knots_cd), bed at the reef = -3.6 m CD = -4.73 m MSL (ASSUMPTION, Lior decision D1 2026-10-07; chart datum assumed, RMS 0.30 m against the 2013 multibeam).',
            source_files=['07_scale/shapes/mount-maunganui-reef/3d/model.js', '07_scale/shapes/mount-maunganui-reef/3d/index.html (lines 193-245, 366-400)'],
            caveats=['As-built seabed under the reef is an ASSUMPTION (-3.6 m CD; stated volume 2,800 m3 gives -3.51 m); the later seabed (Navionics 2026) is -2.76 m CD, which would give a reef 0.84 m lower in height. Reef HEIGHT and slopes therefore depend on this assumption; the crest level (-0.9 m CD = -2.03 m MSL, BoPRC p6/p21) is sourced.',
                     'Flank (skirt) 1:1 below the -2.0 m CD contour is an ASSUMPTION; inside the contour the rise follows the 2013 DEM median rise table.',
                     'Seabed is alongshore uniform; no x dependence.'],
        ))


# ------------------------------------------------------------------------------------------------------- Narrowneck
def narrowneck(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ,
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL; z_MSL = z_AHD - 0.12 (MSQ 2026 Gold Coast Seaway planes: AHD = LAT + 0.76, MSL = LAT + 0.88, uncertainty +-0.25 m); alternative from the papers: AHD = LAT + 1.00 shifts geometry by +0.24 m',
            frame='x alongshore (+ toward NORTH, bearing 356.21 deg T); y offshore (+ toward EAST, bearing 86.21 deg T); origin = waterline of the 2020-08-08 Esri image nearest the reef centroid',
            shoreline_def='y = 0 is the waterline of the Esri World Imagery of 8 Aug 2020 (tide stage unknown); the seabed profile there is 0.0 m AHD = -0.12 m MSL (validation.stats.bed_profile_AHD), so the MSL crossing is within a few metres of y = 0.',
            reef_surface_def='model.js versions[photo_2020-08-08].grid.h_cm_b64 (int16 cm, z_MSL, 1 m cells): plan = 7 traced container-field polygons of the 8 Aug 2020 aerial; surface = design crest surface of renewal Option 2 (crest loops -2.5 m AHD, falling linearly with distance rank to the -6 m AHD envelope), lowered to the measured shallowest crest -2.2/-1.8 m AHD (build_3d.py surface()).',
            seabed_def='model.js seabed (5 m grid, z_MSL): 2017 multibeam (19 Jul 2017) + Navionics labels; offshore profile AHD: 0 at y 0, -1.8 at y 100, -2.1 at y 190, -5.1 at y 265, -6.76 at y 340 (validation.stats.bed_profile_AHD).',
            source_files=['07_scale/shapes/narrowneck-gold-coast/3d/model.js', '07_scale/shapes/narrowneck-gold-coast/3d/build_3d.py (lines 90-115)', '07_scale/shapes/narrowneck-gold-coast/3d/index.html (lines 154-165)'],
            caveats=['Plan is a photo trace of the VISIBLE container field (a lower bound of the footprint; deeper toe not visible); the top surface is a design-rule surface, not a survey; confidence MEDIUM.',
                     'The reef has two arms (north and south) plus channel containers; the cross-shore centreline x_c is the mid-point of the whole footprint (between the arms), so the centreline profile may cross little or no reef; use the crest line profile for the arm.',
                     'History (1999-2000 build, 2004 weir and flared wings, 2017-18 renewal) is not modelled; this is the state after the June 2018 renewal.'],
        ))


# ----------------------------------------------------------------------------------------------------------- Palm Beach
def palm_beach(m, mp):
    sb = m['seabed']
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dx'], np.array(sb['z_cm'], float).reshape(sb['ny'], sb['nx']) / 100.0)
    g = m['reef']['grid']
    Z = np.array(g['z_cm'], float).reshape(g['ny'], g['nx'])
    Z[Z == g['nodata']] = np.nan
    Z /= 100.0
    return dict(
        seabed=seabed, rx=ax(g['x0'], g['dx'], g['nx']), ry=ax(g['y0'], g['dx'], g['ny']), RZ=Z,
        meta=dict(
            version_id='as_built_2019', version_name='As built (rock placed May-Sept 2019, certified Sept 2019); contours from Bluecoast/Nearmap aerial of the completed reef', version_date='2019-09 (aerial undated, Sept 2019 - Sept 2020)',
            datum='z = metres above MSL; MSL = LAT + 0.88 m (MSQ 2026 Gold Coast Seaway); seabed Navionics depths taken as depth below LAT (assumption A5): z_MSL = -d - 0.88',
            frame='x alongshore (toward 334.3 deg T, NNW); y offshore (toward 64.3 deg T, ENE); origin on the waterline of Esri World Imagery 2025-12-01',
            shoreline_def='y = 0 is the waterline fitted to Esri World Imagery 2025-12-01 and taken as z = 0 (MSL) (assumption A7, tide stage of the image unknown). Landward (y < 0) a visual beach face rises at 1:15 (not surveyed).',
            reef_surface_def='model.js reef.grid.z_cm (1 m cells, z_MSL): linear (Delaunay) interpolation between survey contour lines read off the aerial, each at z = -1.5 - 0.5 k m (k = lines crossed outward from the 59 x 6 m crest outline at -1.5 m MSL), toe outline at the next 0.5 m level by fractional position; edge ramped (2.5 m) onto the seabed (reef.side_slope_rule).',
            seabed_def='model.js seabed.z_cm (4 m grid, z_MSL): thin-plate spline through Garmin Navionics SonarChart iso-depth lines (1 m interval, outside a 25 m buffer round the reef) plus toe elevations read from the aerial contours (hybrid); under the reef and seaward of the 10 m line interpolated / extrapolated; chart datum assumed LAT (rms residual 0.08 m).',
            source_files=['07_scale/shapes/palm-beach-gold-coast/3d/model.js', '07_scale/shapes/palm-beach-gold-coast/3d/index.html (lines 160-190)'],
            caveats=['Crest at -1.5 m MSL is from the contour reading of an undated aerial (chart/lidar datum of the contour lines assumed); height above the seabed is sensitive to the Navionics datum assumption (volume 12,000-34,000 m3 for a +-1 m seabed offset).',
                     'Seabed under the reef is interpolated (reef height 3.9 m at the crest from an interpolated bed of -5.4 m MSL, hybrid; Navionics-only bed -5.0 m).'],
        ))


# ------------------------------------------------------------------------------------------------------------- Prattes
def prattes(m, mp):
    S = m['seabed']
    yp = np.array(S['profile_y_m'], float)
    zp = np.array(S['profile_z_m'], float)    # default bed = NOAA DEM mean profile (state.bed = 'dem')

    def seabed(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        z = np.interp(y, yp, zp)
        return np.where((y < yp[0]) | (y > yp[-1]), np.nan, z)
    R = m['reef']
    import shapely
    from shapely.geometry import Polygon
    poly = Polygon(R['toe_polygon_xy_m'])
    st = next(s for s in R['states'] if s['id'] == R['default_state'])
    slope_run = R['slope_run_default']
    min_h = R['min_height_m']
    cell = 0.25
    b = poly.bounds
    xs = np.arange(b[0] - 1 + cell / 2, b[2] + 1, cell)
    ys = np.arange(b[1] - 1 + cell / 2, b[3] + 1, cell)
    X, Y = np.meshgrid(xs, ys)
    inside = shapely.contains_xy(poly, X, Y)
    d = np.zeros_like(X)
    pts = shapely.points(X[inside], Y[inside])
    d[inside] = shapely.distance(pts, poly.exterior)
    zb = seabed(X, Y)
    if st['mode'] == 'level':
        Htop = np.maximum(st['z_msl'] - zb, min_h)
    else:
        t = max(st['z_ref_msl'] - float(seabed(0.0, st['y_ref_m'])), min_h)
        Htop = np.full_like(zb, t)
    H = np.where(inside, np.minimum(Htop, d / slope_run), 0.0)
    RZ = np.where(inside & (H > 0), zb + H, np.nan)
    return dict(
        seabed=seabed, rx=xs, ry=ys, RZ=RZ,
        meta=dict(
            version_id='state_' + st['id'], version_name=st['label'], version_date='Phase I, 22 Sept 2000 (as installed)',
            datum='z = metres above MSL (NOAA 9410840 Santa Monica, epoch 1983-2001); MSL - MLLW = 0.849 m; z_MSL = z_NAVD88 - 0.792 (DEM); LAT = -1.469 m MSL; MLLW = -0.849 m MSL',
            frame='x alongshore (toward 155 deg T, SSE); y offshore (toward 245 deg T, WSW); origin on the MSL waterline (alongshore-uniform profile)',
            shoreline_def='y = 0 is the MSL waterline: the z = 0 contour of the NOAA DEM mean cross-shore profile (model.js seabed.shoreline_y_m = 0, definition: "MSL waterline (z = 0 contour of the seabed profile)").',
            reef_surface_def='Re-implementation of build_3d.py reef_height_field(): h(x,y) = max(0, min(h_top, d_in/slope_run)), d_in = distance inside the toe outline (76-vertex Skelly Engineering design layout of 110 bags, no as-built plan exists), slope_run = 1.0 (ASSUMPTION A5), h_top = constant thickness z_ref - z_seabed(y_ref) = %.3f m (state B: outermost point approx. 6 ft = 1.829 m below MLLW = -2.678 m MSL at the apex, Borrero and Nelsen 2003 p.2; assumption A4: top follows the seabed at constant thickness), >= one 1.2 m bag course; z = z_seabed(y) + h; 0.25 m grid.' % (float(t) if st['mode'] != 'level' else float('nan')),
            seabed_def='model.js seabed.profile_z_m (5 m spacing, NOAA NGDC 2010 Santa Monica 1/3 arc-second NAVD88 DEM, mean of 31 alongshore stations +-150 m, z_MSL = z_NAVD88 - 0.792); alongshore-UNIFORM (no x dependence). Position of the reef on the profile is nominal (100 yd = 91.44 m from the waterline; +-25 m uncertainty, reef_offset_range_m).',
            source_files=['07_scale/shapes/prattes-reef-el-segundo/3d/model.js', '07_scale/shapes/prattes-reef-el-segundo/3d/build_3d.py (lines 48-72, 205-216)'],
            caveats=['Plan is the DESIGN layout (no as-built plan); crest level is a single sourced number (-6 ft MLLW at the apex); the top is assumed parallel to the seabed (state B), so the highest point is at the shoreward tips (-1.78 m MSL) and the V is shallower shoreward.',
                     'State A (top of bag -6 ft MSL = -1.829 m, level crest, Skelly drawing) is the alternative; both are the same number with two datum labels.',
                     'Reef is a V of geotextile sand bags ~1.2-1.35 m high (3.0 x 2.13 x 1.2 m bags); hence slopes are bag-stack flanks (1:1 assumed), not designed wave-transformation ramps.',
                     'Confidence in the 3D model is LOW (model.js confidence_3d).'],
        ))


# ---------------------------------------------------------------------------------------------------------- Albany
def albany(m, mp):
    sb = rows_grid(m['seabed'])
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    H = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])         # height above the seabed (m), NaN outside the footprint
    rx = ax(g['x0'], g['step'], g['nx'])
    ry = ax(g['y0'], g['step'], g['ny'])
    X, Y = np.meshgrid(rx, ry)
    RZ = np.where(np.isfinite(H), sb(X, Y) + H, np.nan)
    return dict(
        seabed=sb, rx=rx, ry=ry, RZ=RZ,
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above AHD, taken as MSL (assumption A2); LAT = -0.74 m AHD (derived: LAT + mean of 2024 predicted extremes), MHHW = +0.34, MLLW = -0.26 (City of Albany crest statement)',
            frame='x alongshore (+ toward NNE, bearing 30.26 deg T); y offshore (+ toward ESE, bearing 120.26 deg T); origin = foot of the perpendicular from the traced reef centroid onto the beach-face line (edge of bright dry sand, Esri 2026-01-20)',
            shoreline_def='y = 0 is the beach-face line (edge of bright dry sand) of the Esri 2026-01-20 image, NOT the MSL line; the modelled seabed crosses z = 0 (AHD) at y about 7 m offshore of it ... (seabed.profile: z = +1.0 at y -30, -0.5 at y 7); the MSL crossing is computed per line (y_msl_crossing_m).',
            reef_surface_def='model.js versions[design_bluecoast].grid.h_cm_b64 = reef HEIGHT above the seabed (int16 cm, 1 m cells); z = seabed(x, y) + h with the bilinear 5 m seabed (index.html buildReef: z = seaAt(x,y) + h). Height rule (build_3d.py reef_grid): crest ridge 9 m inside the steep shoreward edge, -1.0 m AHD at the offshore (east) end and -2.0 m AHD along the rest (City design table), flanks fall to the seabed with shape exponent N = 2.734, volume fitted to the stated 34,000 m3.',
            seabed_def='model.js seabed (5 m grid, z AHD=MSL): read from the RHDHV 2015 design contour profile (alongshore-uniform-ish); LOW confidence per METHODS (2017 bathymetry referred to in the design volume).',
            source_files=['07_scale/shapes/southern-ocean-surf-reef-albany/3d/model.js', '07_scale/shapes/southern-ocean-surf-reef-albany/3d/build_3d.py (lines 100-130)', '07_scale/shapes/southern-ocean-surf-reef-albany/3d/index.html (lines 123-170)'],
            caveats=['3D confidence is LOW: the plan outline is high-confidence and the crest levels are City DESIGN values, but the seabed under the reef (hence heights and flank slopes) is read from 2015 design contours; the reef shape between toe and ridge is a fitted rule (exponent N) not a survey.',
                     'Default version is the Bluecoast design outline (13,104 m2); the visible-reef version (Esri 2026-01-20) has 10,919 m2.',
                     'Slopes of the flanks follow from the fitted exponent and the volume fit to 34,000 m3 (design) and are therefore model results, not measurements.'],
        ))


ADAPTERS = {
    'borth-coastal-defence-reef': borth,
    'boscombe-surf-reef': boscombe,
    'bunbury-airwave': bunbury,
    'cables-reef-wa': cables,
    'mount-maunganui-reef': mount_maunganui,
    'narrowneck-gold-coast': narrowneck,
    'palm-beach-gold-coast': palm_beach,
    'prattes-reef-el-segundo': prattes,
    'southern-ocean-surf-reef-albany': albany,
}
