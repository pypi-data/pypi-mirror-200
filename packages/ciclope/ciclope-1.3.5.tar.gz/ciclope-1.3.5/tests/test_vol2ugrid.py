import sys
sys.path.append('/home/gianthk/PycharmProjects/recon_utils')
sys.path.append('/home/gianthk/PycharmProjects/CT2FE')

import ciclope.core.voxelFE
from ciclope.utils.recon_utils import read_tiff_stack
from ciclope.utils.preprocess import remove_unconnected
import ciclope
import numpy as np

vs = 0.0606

# input_file = '/home/gianthk/Data/2019.001.coop_TUberlin_simulierte_Mensch.iorig/trabecular_samples/trabecular_sample_mini3/2000L_crop_imgaussfilt_60micron_uint8_0000.tif'
input_file = '/home/gianthk/Data/LHDL/3155_D_4_bc/cropped2/slice_000.tif'
data_3D = read_tiff_stack(input_file)

# data_3D = data_3D[25:28, 25:28, 25:28]
# data_3D = data_3D[20:40, 20:40, 20:40]

# apply threshold
# BW = data_3D > 140
BW = data_3D > 63

# detect isolated cluster
BW = remove_unconnected(BW)

# # mask the voxel data
# data_3D[BW==0] = 0
#
# tmpfile = '/home/gianthk/PycharmProjects/CT2FE/input_templates/tmp_example01_comp_static_bone_matprop.inp'
# matprop = {
#             "file": ["/home/gianthk/PycharmProjects/CT2FE/material_properties/bone.inp"],
#             "range": [[1, 250]]
#            }

# mesh, refnodes = ciclope.core.voxelFE.vol2ugrid(data_3D, vs, refnodes=True, verbose=True)
mesh = ciclope.core.voxelFE.vol2ugrid(BW, vs, verbose=True)
mesh.write('foo.vtk')
# src.ciclope.voxelFE.mesh2voxelfe(mesh, tmpfile, "pippo.inp", matprop, keywords=['NSET', 'ELSET', 'PROPERTY'], verbose=True)

# ciclope.voxelFE.vol2voxelfe(data_3D, tmpfile, 'pippo_vol2voxelFE.inp', matprop, ['NSET', 'ELSET', 'PROPERTY'], 0.0606, verbose=True)

#
# import ccx2paraview
# ccx2paraview.Converter('pippo.frd', ['vtk']).run()