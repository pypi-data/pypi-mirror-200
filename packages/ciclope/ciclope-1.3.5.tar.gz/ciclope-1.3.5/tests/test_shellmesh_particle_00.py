import sys
# sys.path.append('/home/gianthk/PycharmProjects/recon_utils')
sys.path.append('/home/gianthk/PycharmProjects/CT2FE')

# import numpy as np

import meshio
from ciclope.utils.recon_utils import read_tiff_stack
from ciclope.core import tetraFE

input_file = '/home/gianthk/Data/BEATS/Franceschin/20217193_Traviglia/recons/581681_punta_HR_stitch2_merge_corr_phrt/masks/crystal/slice_00.tif'

data_3D = read_tiff_stack(input_file)
# vs = np.ones(3)*1e-3 # [mm]
print(data_3D.min())
print(data_3D.max())

# binarize
BW = data_3D > 100

filename_mesh_out = '/home/gianthk/Data/BEATS/Franceschin/20217193_Traviglia/recons/581681_punta_HR_stitch2_merge_corr_phrt/masks/crystal_mesh.vtk'
# mesh = tetraFE.shell_mesh(BW, vs)
# shell mesh using pymcubes (high resolution mesh; caps excluded)
vertices, triangles, shellmesh = tetraFE.shell_mesh(BW, method='pymcubes')

# write VTK mesh with meshio
meshio.write_points_cells(filename_mesh_out, vertices.tolist(), [("triangle", triangles.tolist())])
