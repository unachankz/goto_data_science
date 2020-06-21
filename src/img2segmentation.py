#imageをセグメンテーション化する。

from matplotlib.colors import LinearSegmentedColormap
from skimage.data import astronaut
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries, find_boundaries
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Apply MatplotLib or custom colormap to OpenCV image
# https://stackoverflow.com/questions/52498777/apply-matplotlib-or-custom-colormap-to-opencv-image
def apply_custom_colormap(image_gray, cmap=plt.get_cmap('seismic')):

    assert image_gray.dtype == np.uint8, 'must be np.uint8 image'
    if image_gray.ndim == 3: image_gray = image_gray.squeeze(-1)

    # Initialize the matplotlib color map
    sm = plt.cm.ScalarMappable(cmap=cmap)

    # Obtain linear color range
    color_range = sm.to_rgba(np.linspace(0, 1, 256))[:,0:3]    # color range RGBA => RGB
    color_range = (color_range*255.0).astype(np.uint8)         # [0,1] => [0,255]
    color_range = np.squeeze(np.dstack([color_range[:,2], color_range[:,1], color_range[:,0]]), 0)  # RGB => BGR

    # Apply colormap for each channel individually
    channels = [cv2.LUT(image_gray, color_range[:,i]) for i in range(3)]
    return np.dstack(channels)


# 画像を指定する。
for imfile in ['takahama.png']:
    img = img_as_float(imread(imfile)[::2, ::2, :3])
    segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=100) #300
    borders = find_boundaries(segments_fz)
    unique_colors = np.unique(segments_fz.ravel())

    # borderを描画する。
    # 描画したい場合にはコメントアウトする。
    segments_fz[borders] = -1 #len(unique_colors)
    colors = [np.zeros(3)]
    for color in unique_colors:
        colors.append(np.mean(img[segments_fz == color], axis=0))
    cm = LinearSegmentedColormap.from_list('pallete', colors, N=len(colors))


    # Apply MatplotLib or custom colormap to OpenCV image

    image_bgr = apply_custom_colormap(np.array(segments_fz,dtype=np.uint8), cmap=cm)
    #
    # cv2.imshow('image with colormap', image_bgr)
    # cv2.waitKey(0)
    cv2.imwrite(imfile+"_segmentation.png",image_bgr)
