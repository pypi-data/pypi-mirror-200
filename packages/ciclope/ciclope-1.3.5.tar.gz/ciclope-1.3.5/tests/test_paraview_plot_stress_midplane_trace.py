# trace generated using paraview version 5.9.0-RC1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
b_matrix_tetraFE_Nlgeom16vtk = LegacyVTKReader(registrationName='B_matrix_tetraFE_Nlgeom.16.vtk', FileNames=['/home/gianthk/PycharmProjects/CT2FE/test_data/steel_foam/B_matrix_tetraFE_Nlgeom.16.vtk'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
b_matrix_tetraFE_Nlgeom16vtkDisplay = Show(b_matrix_tetraFE_Nlgeom16vtk, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
b_matrix_tetraFE_Nlgeom16vtkDisplay.Representation = 'Surface'
b_matrix_tetraFE_Nlgeom16vtkDisplay.ColorArrayName = [None, '']
b_matrix_tetraFE_Nlgeom16vtkDisplay.SelectTCoordArray = 'None'
b_matrix_tetraFE_Nlgeom16vtkDisplay.SelectNormalArray = 'None'
b_matrix_tetraFE_Nlgeom16vtkDisplay.SelectTangentArray = 'None'
b_matrix_tetraFE_Nlgeom16vtkDisplay.OSPRayScaleArray = 'ERROR'
b_matrix_tetraFE_Nlgeom16vtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
b_matrix_tetraFE_Nlgeom16vtkDisplay.SelectOrientationVectors = 'ERROR'
b_matrix_tetraFE_Nlgeom16vtkDisplay.ScaleFactor = 0.41558346679667013
b_matrix_tetraFE_Nlgeom16vtkDisplay.SelectScaleArray = 'ERROR'
b_matrix_tetraFE_Nlgeom16vtkDisplay.GlyphType = 'Arrow'
b_matrix_tetraFE_Nlgeom16vtkDisplay.GlyphTableIndexArray = 'ERROR'
b_matrix_tetraFE_Nlgeom16vtkDisplay.GaussianRadius = 0.020779173339833507
b_matrix_tetraFE_Nlgeom16vtkDisplay.SetScaleArray = ['POINTS', 'ERROR']
b_matrix_tetraFE_Nlgeom16vtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
b_matrix_tetraFE_Nlgeom16vtkDisplay.OpacityArray = ['POINTS', 'ERROR']
b_matrix_tetraFE_Nlgeom16vtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'
b_matrix_tetraFE_Nlgeom16vtkDisplay.DataAxesGrid = 'GridAxesRepresentation'
b_matrix_tetraFE_Nlgeom16vtkDisplay.PolarAxes = 'PolarAxesRepresentation'
b_matrix_tetraFE_Nlgeom16vtkDisplay.ScalarOpacityUnitDistance = 0.13139722740050921
b_matrix_tetraFE_Nlgeom16vtkDisplay.OpacityArrayName = ['POINTS', 'ERROR']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
b_matrix_tetraFE_Nlgeom16vtkDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
b_matrix_tetraFE_Nlgeom16vtkDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(registrationName='WarpByVector1', Input=b_matrix_tetraFE_Nlgeom16vtk)
warpByVector1.Vectors = ['POINTS', 'S_Principal']

# Properties modified on warpByVector1
warpByVector1.Vectors = ['POINTS', 'U']

# show data in view
warpByVector1Display = Show(warpByVector1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
warpByVector1Display.Representation = 'Surface'
warpByVector1Display.ColorArrayName = [None, '']
warpByVector1Display.SelectTCoordArray = 'None'
warpByVector1Display.SelectNormalArray = 'None'
warpByVector1Display.SelectTangentArray = 'None'
warpByVector1Display.OSPRayScaleArray = 'ERROR'
warpByVector1Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByVector1Display.SelectOrientationVectors = 'ERROR'
warpByVector1Display.ScaleFactor = 0.4268416158854962
warpByVector1Display.SelectScaleArray = 'ERROR'
warpByVector1Display.GlyphType = 'Arrow'
warpByVector1Display.GlyphTableIndexArray = 'ERROR'
warpByVector1Display.GaussianRadius = 0.02134208079427481
warpByVector1Display.SetScaleArray = ['POINTS', 'ERROR']
warpByVector1Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByVector1Display.OpacityArray = ['POINTS', 'ERROR']
warpByVector1Display.OpacityTransferFunction = 'PiecewiseFunction'
warpByVector1Display.DataAxesGrid = 'GridAxesRepresentation'
warpByVector1Display.PolarAxes = 'PolarAxesRepresentation'
warpByVector1Display.ScalarOpacityUnitDistance = 0.13323858984902565
warpByVector1Display.OpacityArrayName = ['POINTS', 'ERROR']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
warpByVector1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
warpByVector1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(b_matrix_tetraFE_Nlgeom16vtk, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=warpByVector1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [2.061317566782236, 1.9398072597105056, 1.62587882054504]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [2.061317566782236, 1.9398072597105056, 1.62587882054504]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = [None, '']
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'ERROR'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'ERROR'
slice1Display.ScaleFactor = 0.3722270727157593
slice1Display.SelectScaleArray = 'ERROR'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'ERROR'
slice1Display.GaussianRadius = 0.018611353635787965
slice1Display.SetScaleArray = ['POINTS', 'ERROR']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'ERROR']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(warpByVector1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

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

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# reset view to fit data
renderView1.ResetCamera()

# get color legend/bar for s_MisesLUT in view renderView1
s_MisesLUTColorBar = GetScalarBar(s_MisesLUT, renderView1)

# change scalar bar placement
s_MisesLUTColorBar.WindowLocation = 'AnyLocation'
s_MisesLUTColorBar.Position = [0.7813884785819792, 0.32912988650693564]
s_MisesLUTColorBar.ScalarBarLength = 0.3300000000000003

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1354, 793)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [11.564813561444938, 1.9243587255477905, 1.645284004509449]
renderView1.CameraFocalPoint = [2.0613176822662354, 1.9243587255477905, 1.645284004509449]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 2.4596857285847724

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).