"""Objective dark-patch outline of the built reef on the Esri 2026-01-20 z18 tile.
Method: green channel -> 7x7 minimum filter (suppresses glints/foam) -> gaussian sigma 3 -> threshold T
(midway between reef interior ~12-20 and ambient deep water ~40-55) -> largest connected component inside the ROI
-> fill holes -> contour -> Douglas-Peucker 3 px. Prints polygon (px). Usage: python -I trace_mask.py T"""
import sys, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, minimum_filter, label, binary_fill_holes, binary_opening, binary_closing
from skimage import measure  # may be missing
