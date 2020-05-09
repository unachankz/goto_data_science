# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import cv2

#濃淡を反転した画像を生成するために使用する。
def invert(pixel):
    return 1 - pixel

# グレースケールにしておく
img = cv2.imread('imgs/miiraku_junior_high.jpg',0)

print(img.shape)

cv2.imwrite("imgs/grayscale_miirak_junior_high.jpg",np.uint8(img))

#濃淡を反転した画像を生成する。
img_2 = np.array([invert(a) for a in img])

img_2_org = np.copy(img_2)

#濃淡を反転した画像を生成する。
cv2.imwrite("imgs/inverse_miirak_junior_high.jpg",np.uint8(img_2))

# 移動量
dx = -3
dy = -3

# 変換行列
#データ型が np.float32 のNumpyの配列に値を設定し， cv2.warpAffine() 関数に与える。
M = np.float32([[1,0,dx],[0,1,dy]])
rownum,colnum = img_2.shape[:2]
#http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
img_2 = cv2.warpAffine(img_2, M,(colnum,rownum)) # (列数, 行数)の順

#濃淡を反転した画像に対して移動した結果を画像出力する。
cv2.imwrite("imgs/inverse_miirak_junior_high_moved.jpg",np.uint8(img_2))

add = img + img_2
emboss = add - 128

# plt.figure(figsize=(16,9))
# plt.imshow(emboss)
# plt.show()


#ファイル出力
cv2.imwrite("imgs/emnos_miirak.jpg",emboss)



#分析結果
fig = plt.figure(figsize=(15,15))
gs_master = gridspec.GridSpec(nrows=3, ncols=3, height_ratios=[1, 1, 1])

sns.set_style('darkgrid')
gs_1 = gridspec.GridSpecFromSubplotSpec(nrows=2, ncols=1, subplot_spec=gs_master[0:2, 0])
ax2 = fig.add_subplot(gs_1[1,:])
ax2.set_title('input')
ax2.set_xlabel('x')
ax2.set_ylabel('pixel')
ax2.plot(img[450:500,450:500].ravel())

gs_2_and_3 = gridspec.GridSpecFromSubplotSpec(nrows=2, ncols=1, subplot_spec=gs_master[0:2, 1])
ax2 = fig.add_subplot(gs_2_and_3[0,:])

ax2.set_title('inverse')
ax2.set_xlabel('x')
ax2.set_ylabel('pixel')
ax2.plot(img_2_org[450:500,450:500].ravel())

ax2 = fig.add_subplot(gs_2_and_3[1,:])
ax2.set_title('inverse + horizontal transpose')
ax2.set_xlabel('x')
ax2.set_ylabel('pixel')
ax2.plot(img_2[450:500,450:500].ravel())


gs_4 = gridspec.GridSpecFromSubplotSpec(nrows=2, ncols=1, subplot_spec=gs_master[0:2, 2])
ax2 = fig.add_subplot(gs_4[1,:])
ax2.set_title('input')
ax2.set_xlabel('x')
ax2.set_ylabel('pixel')
ax2.plot(emboss[450:500,450:500].ravel())
plt.savefig("imgs/analyze.jpg")
