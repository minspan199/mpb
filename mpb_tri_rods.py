# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
from bands_plotting_utils import plot_data as pltd
from bands_plotting_utils import plot_te as plte
from bands_plotting_utils import plot_tm as pltm

num_bands = 8
resolution = 32
geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
                              basis1=mp.Vector3(math.sqrt(3)/2, 0.5),
                              basis2=mp.Vector3(math.sqrt(3)/2, -0.5))
geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]
# =============================================================================
# k_points = [
#     mp.Vector3(),               # Gamma
#     mp.Vector3(y=0.5),          # M
#     mp.Vector3(-1./3, 1./3),    # K
#     mp.Vector3(),               # Gamma
# ]
# =============================================================================

k_points = [
    mp.Vector3(-1./3, 1./3),    # K
    mp.Vector3(),               # Gamma
    mp.Vector3(y=0.5),          # M
    mp.Vector3(-1./3, 1./3)    # K
]

k_points = mp.interpolate(50, k_points)

ms = mpb.ModeSolver(
    geometry=geometry,
    geometry_lattice=geometry_lattice,
    k_points=k_points,
    resolution=resolution,
    num_bands=num_bands
)
ms.run_tm(mpb.output_at_kpoint(mp.Vector3(-1./3, 1./3), mpb.fix_efield_phase,
          mpb.output_efield_z))
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list


md = mpb.MPBData(rectify=True, periods=3, resolution=32)
eps = ms.get_epsilon()
converted_eps = md.convert(eps)

plt.imshow(converted_eps.T, interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

pltd(tm_freqs, te_freqs, tm_gaps, te_gaps)

plte(te_freqs, te_gaps)

pltm(tm_freqs, tm_gaps)