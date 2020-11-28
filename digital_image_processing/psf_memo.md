# point spred function
手軽にpoint spred functionの実験ができないかを調査した。

## sample codeのダウンロード
1. サンプルコードをダウンロードする
```
git clone https://github.com/michal2229/dft-wiener-deconvolution-with-psf
```

2. サンプルコードを実行する。
```
cd dft-wiener-deconvolution-with-psf
python deconv_cv.py --angle 0 --circle  --d 22  lena.png
```

3. bug fix
実行すると、cv2.CV_AAが無いとエラーが発生する。
```
Traceback (most recent call last):
  File "deconv_cv.py", line 169, in <module>
    update(None)
  File "deconv_cv.py", line 121, in update
    psf = defocus_kernel(d)
  File "deconv_cv.py", line 63, in defocus_kernel
    cv2.circle(kern, (sz, sz), d, 255, -1, cv2.CV_AA, shift=1)
AttributeError: module 'cv2.cv2' has no attribute 'CV_AA'
```
- 修正前
```
def defocus_kernel(d, sz=65):
    kern = np.zeros((sz, sz), np.uint8)
    cv2.circle(kern, (sz, sz), d, 255, -1, cv2.CV_AA, shift=1) ## ここでエラーが発生
    kern = np.float32(kern) / 255.0
```
- 修正後
`cv.CV_AA`を`cv.LINE_AA`に変えることで実行できる。

```
def defocus_kernel(d, sz=65):
    kern = np.zeros((sz, sz), np.uint8)
    cv2.circle(kern, (sz, sz), d, 255, -1, cv2.LINE_AA, shift=1) ##ここを修正する。
    kern = np.float32(kern) / 255.0
    return kern
```

＃ImageJ Fiji
ImageJ Fijiを用いることでconvolution / deconvolutionの実験を行うことができた。

## ImageJ Fiji software Downloads
1. 私はmac版をdownloadした。
   [ImageJ](https://imagej.net/Downloads)

2. アプリケーション配下にソフトウェアをコピーする。
3. Diffraction PSF 3Dのクラスをダウンロードする。
[Diffraction_PSF_3D.class](http://www.optinav.info/download/Diffraction_PSF_3D.class)

4. Fijiのアプリケーションを右クリックして、「パッケージの内容」を表示を開く。
5. pluginsの配下にDiffraction_PSF_3D.classをコピーする。




# Image deblurring

下記のパッケージでもpoint spred functionの実験は可能
https://pylops.readthedocs.io/en/latest/tutorials/deblurring.html#sphx-glr-tutorials-deblurring-py
```
git clone https://github.com/equinor/pylops
pip install pylops

```

# 参考
・[Wiener-Filter](https://github.com/tranleanh/Wiener-Filter-image-restoration)

・[Out-of-focus Deblur Filter](https://docs.opencv.org/master/de/d3c/tutorial_out_of_focus_deblur_filter.html)
