# cv_rotate_3d
OpenCVでX軸、Y軸、Z軸の回転を行うサンプルです。<br>
![image](https://github.com/Kazuhito00/cv_rotate_3d/assets/37477845/f1a36082-5762-47c1-84d7-db28be57648e)

# Requirement
* OpenCV 3.4.2 or later
 
# Usage
サンプルの実行方法は以下です。
```bash
python sample.py
```
```python
image = rotate_3d(
    image,
    theta=30,          # x軸を中心に回転(度)
    phi=30,            # y軸を中心に回転(度)
    gamma=30,          # z軸を中心に回転(度)
    dx=0,              # x軸方向に平行移動(ピクセル)
    dy=0,              # y軸方向に平行移動(ピクセル)
    dz=0,              # z軸方向に平行移動(ピクセル)
    color=(0, 255, 0), # 回転時に発生する余白の色
)
```

# Note
サンプルの画像は[ぱくたそ](https://www.pakutaso.com/)様の「[モチベーションが死んでる女子校生](https://www.pakutaso.com/20230655173post-47613.html)」を使用しています。

# Author
高橋かずひと
 
# License 
cv_rotate_3d is under [Apache 2.0 license](LICENSE).

