import sys
sys.path.append('./../../')

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scipy import ndimage, misc
from skimage.filters import threshold_otsu, gaussian
from skimage import measure, morphology
from skimage.morphology import skeletonize, skeletonize_3d,  medial_axis
from skimage.util import invert
from skimage import data


from ciclope.utils.recon_utils import read_tiff_stack, plot_midplanes, plot_projections
from ciclope.utils.preprocess import remove_unconnected
import ciclope

import sknw

input_file = '/home/gianthk/PycharmProjects/CT2FE/test_data/LHDL/3155_D_4_bc/cropped/3155_D_4_bc_0000.tif'

data_3D = read_tiff_stack(input_file)
vs = np.ones(3)*19.5e-3 # [mm]

data_3D = gaussian(data_3D, sigma=1, preserve_range=True)

BW = data_3D > 63 # 52?? from comparison with histology

BW = remove_unconnected(BW)

# SKELETON
inverseBW = invert(BW)

ske = skeletonize_3d(BW).astype(np.uint8)

graph = sknw.build_sknw(ske)

graph.edges(176)