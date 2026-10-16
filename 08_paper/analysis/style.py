"""style.py - shared figure style of the surf-reef review paper (08_paper/figures).

Import in every figure script:   from style import SLUGS, NAMES, COLORS, MARKERS, setup, save, cm
One colour (+ one marker) per reef, the same in ALL figures. Colour-blind check (dataviz validate_palette.js, light mode):
lightness band PASS, chroma floor PASS, normal-vision separation PASS, CVD separation WARN (worst adjacent pair
Bunbury/Mexico, dE 6.2 protan = floor band), so identity is ALSO carried by a unique marker shape and by direct labels.
Palette = Okabe-Ito / Tol hues, in the dataset order of 08_paper/data/reefs.json.
"""
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FIG_DIR = os.path.join(REPO, '08_paper', 'figures')
DATA_DIR = os.path.join(REPO, '08_paper', 'data')
SHAPES = os.path.join(REPO, '07_scale', 'shapes')

# dataset order (reefs.json)
SLUGS = ['narrowneck-gold-coast', 'cables-reef-wa', 'prattes-reef-el-segundo', 'mount-maunganui-reef', 'opunake-reef',
         'boscombe-surf-reef', 'kovalam-reef-india', 'borth-coastal-defence-reef', 'palm-beach-gold-coast',
         'southern-ocean-surf-reef-albany', 'burkitts-reef-bargara', 'bunbury-airwave', 'mexico-reef-2026-unnamed']

NAMES = {  # short labels used in all figures
    'narrowneck-gold-coast': 'Narrowneck', 'cables-reef-wa': 'Cables', 'prattes-reef-el-segundo': "Pratte's",
    'mount-maunganui-reef': 'Mt Maunganui', 'opunake-reef': 'Opunake', 'boscombe-surf-reef': 'Boscombe',
    'kovalam-reef-india': 'Kovalam', 'borth-coastal-defence-reef': 'Borth', 'palm-beach-gold-coast': 'Palm Beach',
    'southern-ocean-surf-reef-albany': 'Albany', 'burkitts-reef-bargara': 'Burkitts', 'bunbury-airwave': 'Bunbury Airwave',
    'mexico-reef-2026-unnamed': 'Xala (Mexico)'}

PLACE = {  # place + country code, second label line
    'narrowneck-gold-coast': 'Gold Coast, AU', 'cables-reef-wa': 'Perth, AU', 'prattes-reef-el-segundo': 'California, US',
    'mount-maunganui-reef': 'Bay of Plenty, NZ', 'opunake-reef': 'Taranaki, NZ', 'boscombe-surf-reef': 'Dorset, UK',
    'kovalam-reef-india': 'Kerala, IN', 'borth-coastal-defence-reef': 'Ceredigion, UK', 'palm-beach-gold-coast': 'Gold Coast, AU',
    'southern-ocean-surf-reef-albany': 'Albany, AU', 'burkitts-reef-bargara': 'Bargara, AU', 'bunbury-airwave': 'Bunbury, AU',
    'mexico-reef-2026-unnamed': 'Jalisco, MX'}

COLORS = {
    'narrowneck-gold-coast': '#0072B2', 'cables-reef-wa': '#E69F00', 'prattes-reef-el-segundo': '#CC79A7',
    'mount-maunganui-reef': '#009E73', 'opunake-reef': '#882255', 'boscombe-surf-reef': '#D55E00',
    'kovalam-reef-india': '#8E6BBE', 'borth-coastal-defence-reef': '#56B4E9', 'palm-beach-gold-coast': '#5E4FA2',
    'southern-ocean-surf-reef-albany': '#117733', 'burkitts-reef-bargara': '#AA4499', 'bunbury-airwave': '#1F9E89',
    'mexico-reef-2026-unnamed': '#EE6677'}

MARKERS = {
    'narrowneck-gold-coast': 'o', 'cables-reef-wa': 's', 'prattes-reef-el-segundo': '^', 'mount-maunganui-reef': 'D',
    'opunake-reef': 'v', 'boscombe-surf-reef': 'P', 'kovalam-reef-india': '<', 'borth-coastal-defence-reef': 'X',
    'palm-beach-gold-coast': '>', 'southern-ocean-surf-reef-albany': 'h', 'burkitts-reef-bargara': '*',
    'bunbury-airwave': 'p', 'mexico-reef-2026-unnamed': 'd'}

# neutral inks / grounds (shared)
INK = '#222222'
INK2 = '#555555'
GRID = '#D9D9D9'
UNKNOWN = '#9A9A9A'
SEA = '#EAF3FA'      # sea ground (plan)
SAND = '#F1E7D0'     # beach / seabed fill
SEABED = '#8A6D3B'   # seabed line
TIDE = '#9CC7E8'     # tide band

CM = 1 / 2.54
FULL_W = 17.0 * CM   # inches, full A4 text width
COL_W = 8.3 * CM     # inches, one column


def cm(x):
    return x / 2.54


def setup():
    """matplotlib rcParams: sans-serif, >= 7 pt at print size, vector fonts embedded (Type 42)."""
    from matplotlib import font_manager
    fam = 'DejaVu Sans'
    for f in ('Liberation Sans', 'Arial', 'Helvetica'):
        try:
            font_manager.findfont(f, fallback_to_default=False)
            fam = f
            break
        except Exception:
            pass
    plt.rcParams.update({
        'font.family': fam, 'font.size': 7.5, 'axes.labelsize': 7.5, 'axes.titlesize': 8, 'xtick.labelsize': 7,
        'ytick.labelsize': 7, 'legend.fontsize': 7, 'axes.linewidth': 0.6, 'xtick.major.width': 0.6,
        'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'lines.linewidth': 1.0,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': INK2, 'axes.labelcolor': INK,
        'xtick.color': INK, 'ytick.color': INK, 'text.color': INK, 'figure.facecolor': 'white',
        'axes.facecolor': 'white', 'savefig.facecolor': 'white', 'pdf.fonttype': 42, 'ps.fonttype': 42,
        'svg.fonttype': 'none', 'mathtext.default': 'regular'})
    return fam


def save(fig, name, dpi=300):
    """Write <name>.png (300 dpi) and <name>.pdf (vector) into 08_paper/figures/."""
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, name + '.png'), dpi=dpi)
    fig.savefig(os.path.join(FIG_DIR, name + '.pdf'))
    plt.close(fig)
    return [os.path.join(FIG_DIR, name + e) for e in ('.png', '.pdf')]
