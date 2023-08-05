import numpy as np
import skimage.io as skio
from recon_utils import plot_midplanes
from old.pybonemorph import embed
import matplotlib.pyplot as plt

input_file = '/home/gianthk/Data/sarig/Tooth_TAU_3_scaled.tif'
data_3D = skio.imread(input_file, plugin="tifffile")

tooth = np.zeros(data_3D.shape, dtype='uint8')
tooth[data_3D>80] = 10

embedded, embedding_mask = embed(tooth, 150, "ay", 20)

plot_midplanes(embedded)
plt.show()