import ciclope.core.voxelFE
from ciclope.utils.recon_utils import read_tiff_stack
from ciclope.utils.preprocess import remove_unconnected
import ciclope
import numpy as np
import unittest

# read test dataset
pippo = read_tiff_stack("/home/gianthk/Data/LHDL/3155_D_4_bc/trab/slice_00.tif")
# segment
pippo_BW = pippo > 100
# ------------------------------------------------------------------------------
# test remove_unconnected method
pippo_BW_remove = remove_unconnected(pippo_BW)
assert (np.sum(pippo_BW) - np.sum(pippo_BW_remove)) == 4

# ------------------------------------------------------------------------------
# test tetraFE.shell_mesh (pymcubes method)
vert, tri, mesh = ciclope.tetraFE.shell_mesh(pippo_BW_remove, method='pymcubes', voxelsize=[0.12,0.12,0.12])
# check if 3D shell mesh fields (vertices, triangles) were produced
assert vert.shape[1] == 3
assert tri.shape[1] == 3

# test tetraFE.shell_mesh (pygalmesh method)
vert, tri, mesh = ciclope.tetraFE.shell_mesh(pippo_BW_remove, method='pygalmesh', voxelsize=[0.12,0.12,0.12])
# check if 3D shell mesh fields (vertices, triangles) were produced
# assert mesh.points.shape == (12, 3)
assert (len(mesh.points) != 0) == True
assert mesh.cells[0][0] == 'triangle'
# assert mesh.cells[0][1].shape == (36,3)
assert (len(mesh.cells[0][1]) != 0) == True

# test tetraFE.cgal_mesh (pygalmesh method)
mesh = ciclope.tetraFE.cgal_mesh(pippo_BW_remove, [0.12,0.12,0.12], meshtype='tetra', max_facet_distance=0.0, max_cell_circumradius=0.0)
# check that points and cells fields are not empty
assert (len(mesh.points) != 0) == True
assert mesh.cells[0][0] == 'tetra'
assert (len(mesh.cells[0][1]) != 0) == True

# test mesh2tetrafe
# write input file from already loaded mesh
ciclope.tetraFE.mesh2tetrafe(mesh, 'input_test.inp', 'foo.inp')
# read and check input CALCULIX file: check existence of essential fields
with open("foo.inp", 'r') as f:
    lines = f.readlines()
    node = False
    element = False
    elset = False
    elset_z1 = False
    nset_z0 = False
    step = False
    bc = False

    for line in lines:
        if line.find('*NODE') != -1:
            node = True
        if line.find('*ELEMENT, TYPE=C3D4') != -1:
            element = True
        if line.find('*ELSET, ELSET=SETALL') != -1:
            elset = True
        if line.find('*ELSET, ELSET=ELEMS_Z1') != -1:
            elset_z1 = True
        if line.find('*NSET, NSET=NODES_Z0') != -1:
            nset_z0 = True
        if line.find('*STEP') != -1:
            step = True
        if line.find('NODES_T, 3, 3, -0.002') != -1:
            bc = True

assert node == True
assert element == True
assert elset == True
assert elset_z1 == True
assert nset_z0 == True
assert step == True
assert bc == True

# ------------------------------------------------------------------------------
# test voxelFE.vol2ugrid meshing method
pippo_mesh = ciclope.core.voxelFE.vol2ugrid(pippo, [0.12,0.12,0.12], GVmin=100)
assert pippo_mesh.cells[0].type == "hexahedron"
assert pippo_mesh.cells[0].data.shape == (209,8)
assert pippo_mesh.points.shape == (1331,3)
assert pippo_mesh.point_sets['NODES_X0Y0Z0'] == [18,19]
assert (pippo_mesh.points[100] == np.array([0.12, 1.08, 0])).all() == True

# ------------------------------------------------------------------------------
# run mesh2voxelFE
ciclope.voxelFE.mesh2voxelfe(pippo_mesh, 'input_test.inp', 'foo.inp')
# read and check input CALCULIX file: check existence of essential fields
with open("foo.inp", 'r') as f:
    lines = f.readlines()
    node = False
    element = False
    elset_z1 = False
    nset_z0 = False
    step = False
    bc = False

    for line in lines:
        if line.find('*NODE') != -1:
            node = True
        if line.find('*ELEMENT, TYPE=C3D8, ELSET=SET255') != -1:
            element = True
        if line.find('*ELSET, ELSET=CELLS_Z1') != -1:
            elset_z1 = True
        if line.find('*NSET, NSET=NODES_Z0') != -1:
            nset_z0 = True
        if line.find('*STEP') != -1:
            step = True
        if line.find('NODES_T, 3, 3, -0.002') != -1:
            bc = True

assert node == True
assert element == True
assert elset == True
assert elset_z1 == True
assert nset_z0 == True
assert step == True
assert bc == True

# read and check input CALCULIX file: read two specific file lines
with open("foo.inp", 'r') as f:
    line_numbers = [99, 860]
    lines = []
    for i, line in enumerate(f):
        if i in line_numbers:
            lines.append(line.strip())

# assert one node and one node_set line
assert list(map(float, lines[0].split(","))) == [359.0, 0.84, 1.2, 0.24]
assert list(map(int, lines[1].strip(',').split(','))) == [37, 64, 92, 126]

# ------------------------------------------------------------------------------
