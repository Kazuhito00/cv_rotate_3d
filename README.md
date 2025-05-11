# cv_rotate_3d
OpenCVでX軸、Y軸、Z軸の回転を行うサンプルです。<br>
<img src="https://github.com/user-attachments/assets/535de9ba-c717-44d6-ac08-2c71a9a76754" loading="lazy" width="50%">

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
    color=(0, 255, 0), # 回転時に発生する余白の色
    transparent=False, # 背景を透過するか否か
)
```

# Note
サンプルの画像は[ぱくたそ](https://www.pakutaso.com/)様の「[モチベーションが死んでる女子校生](https://www.pakutaso.com/20230655173post-47613.html)」を使用しています。

# Author
高橋かずひと
 
# License 
cv_rotate_3d is under [Apache 2.0 license](LICENSE).

