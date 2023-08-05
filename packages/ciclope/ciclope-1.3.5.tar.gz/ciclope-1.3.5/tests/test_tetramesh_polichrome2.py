import sys
# sys.path.append('/home/gianthk/PycharmProjects/recon_utils')
sys.path.append('/home/gianthk/PycharmProjects/CT2FE')

import numpy as np

from scipy import ndimage
from skimage.filters import threshold_multiotsu
from skimage import morphology, transform

import skimage.io as skio

# from recon_utils import plot_midplanes, bbox
from ciclope.utils.recon_utils import plot_midplanes, bbox
from ciclope.utils.preprocess import fill_voids, embed, add_cap
from ciclope.core import tetraFE

input_file = './test_data/tooth/Tooth_3_scaled_2.tif' # scale factor: 0.4

data_3D = skio.imread(input_file, plugin="tifffile")
vs = np.ones(3)*16.5e-3/0.2 # [mm]

# prepare transformation matrix
# affine = []
# tform = transform.AffineTransform(matrix=np.array([[affine[0], affine[1], affine[2]],
#                                                    [affine[3], affine[4], affine[5]],
#                                                    [0, 0, 1]]))
#
# tform_inverse = tform.inverse
# data_3D = transform.warp(data_3D, tform_inverse)

# binarize
Ts = threshold_multiotsu(data_3D)
BW_tooth = ndimage.binary_fill_holes(ndimage.binary_opening(data_3D >= Ts[0], morphology.ball(3)))
BW_dentin = ndimage.binary_fill_holes(ndimage.binary_opening((data_3D <= Ts[1]) & (data_3D >= Ts[0]), morphology.ball(3)))
BW_enamel = data_3D > Ts[1]

# Create color image with different materials
data_for_meshing = fill_voids(BW_dentin*1 + BW_enamel*2, 1, False)

data_for_meshing_embedded, BW_embedding_bottom = embed(data_for_meshing, 140, "-z", embed_val=3, pad=2, makecopy=True)
data_for_meshing_embedded, BW_embedding_top = embed(data_for_meshing_embedded, 40, "+z", embed_val=3, pad=2)

# add steel caps
data_for_meshing_embedded = add_cap(data_for_meshing_embedded, cap_thickness=10, cap_val=4)

filename_mesh_out = 'test_data/tooth/results/Tooth_3_scaled_2_tetramesh.vtk'

mesh = tetraFE.cgal_mesh(data_for_meshing_embedded, vs, 'tetra', 1.2 * min(vs), 3.6 * min(vs))

# print(mesh)
# print(mesh.cells)

# mesh.write(filename_mesh_out)

# create ABAQUS input
input_template = "input_templates/tmp_example03_comp_static_tooth.inp"
filename_out = 'test_data/tooth/results/Tooth_3_scaled_2.inp'

tetraFE.mesh2tetrafe(mesh, input_template, filename_out, keywords=['NSET', 'ELSET'])