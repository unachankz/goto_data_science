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
    cv2.circle(kern, (sz, sz), d, 255, -1, cv2.CV_AA, shift=1)
    kern = np.float32(kern) / 255.0
```
- 修正後
- 
