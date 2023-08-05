#!/usr/bin/pvpython
from paraview.simple import *
import time

# read vtk file
# data = LegacyVTKReader(FileNames="/home/gianthk/PycharmProjects/CT2FE/test_data/steel_foam/B_matrix_tetraFE_Nlgeom.10.vtk")
data = LegacyVTKReader(FileNames="/home/gianthk/PycharmProjects/CT2FE/test_data/tooth/results/Tooth_3_scaled_2.vtk")
# Show(data)

slice = Slice(registrationName='Slice1', Input=data)

slice.SliceType = 'Plane'
slice.HyperTreeGridSlicer = 'Plane'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

#draw the object
# show data in view
slice1Display = Show(slice, renderView1, 'GeometryRepresentation')

# get the object bounds
bounds = data.GetDataInformation().GetBounds()
center = [(bounds[1]-bounds[0])/2, (bounds[3]-bounds[2])/2, (bounds[5]-bounds[4])/2]

slice.SliceOffsetValues = [0.0]

# slice.SliceType.Origin = [2., 2., 1.4]
slice.SliceType.Origin = center

# slice.SliceType.Normal = [0.0, 0.0, 1.0]
slice.SliceType.Normal = [1.0, 0.0, 0.0]

# crinckle the slice
slice.Crinkleslice = 1

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [10000, center[1], center[2]]
renderView1.CameraFocalPoint = center

# change representation type
# slice1Display.SetRepresentationType('Surface')
slice1Display.SetRepresentationType('SurfaceWithEdges')

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'S_Mises', 'S_Mises'))

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'S_Mises'
s_MisesLUT = GetColorTransferFunction('S_Mises')

# get opacity transfer function/opacity map for 'S_Mises'
s_MisesPWF = GetOpacityTransferFunction('S_Mises')

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
s_MisesLUT.ApplyPreset('Viridis (matplotlib)', True)

# get color legend/bar for s_MisesLUT in view renderView1
s_MisesLUTColorBar = GetScalarBar(s_MisesLUT, renderView1)

# change scalar bar placement
# s_MisesLUTColorBar.Orientation = 'Horizontal'
s_MisesLUTColorBar.Orientation = 'Vertical'
s_MisesLUTColorBar.WindowLocation = 'UpperRightCorner'# 'AnyLocation', 'LowerRightCorner', 'LowerLeftCorner', 'LowerCenter', 'UpperLeftCorner', 'UpperRightCorner', 'UpperCenter'
s_MisesLUTColorBar.TitleColor = [0,0,0]      # switch to black
s_MisesLUTColorBar.LabelColor = [0,0,0]      # switch to black
s_MisesLUTColorBar.TitleFontSize = 10
s_MisesLUTColorBar.LabelFontSize = 10
s_MisesLUTColorBar.ScalarBarThickness = 8

# Data Axis visibility
slice1Display.DataAxesGrid.GridAxesVisibility = 1

# Data Axis Font
slice1Display.DataAxesGrid.XTitleFontSize = 40
slice1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0] # switch to black
slice1Display.DataAxesGrid.XLabelFontSize = 40
slice1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
slice1Display.DataAxesGrid.YTitleFontSize = 40
slice1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0] # switch to black
slice1Display.DataAxesGrid.YLabelFontSize = 40
slice1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
slice1Display.DataAxesGrid.ZTitleFontSize = 40
slice1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0] # switch to black
slice1Display.DataAxesGrid.ZLabelFontSize = 40
slice1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

slice1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0] # grid color to black

# update the view to ensure updated data information
renderView1.Update()

# dp = GetDisplayProperties()
#
# #set point color
# dp.AmbientColor = [1, 0, 0] #red
#
# #set surface color
# dp.DiffuseColor = [0, 1, 0] #blue
#
# #set point size
# dp.PointSize = 2

# #set representation
# dp.Representation = "Surface"

camera = GetActiveCamera()
# camera.Elevation(45)
camera.Roll(-90)
Render()

#save screenshot
# SaveScreenshot("pippo.png", ImageResolution=[1000,1000], TransparentBackground=1)
SaveScreenshot("pippo.png", ImageResolution=[1280,960])