from ciclope.utils.postprocess import paraview_plot

paraview_plot("/home/gianthk/PycharmProjects/CT2FE/test_data/tooth/results/Tooth_3_scaled_2.vtk", slicenormal="xyz", RepresentationType="3D Glyphs", Crinkle=False, ColorBy="E_Principal", Roll=90, ImageResolution=[1024, 1024])

# paraview_plot("/home/gianthk/PycharmProjects/CT2FE/test_data/tooth/results/Tooth_3_scaled_2.vtk", slicenormal="xyz", crinkle=True, colorby=['U', 'D3'], Roll=90, ImageResolution=[1024, 1024], TransparentBackground=True, colormap='Cool to Warm')