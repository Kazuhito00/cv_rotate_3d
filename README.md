# cv_rotate_3d
OpenCVでX軸、Y軸、Z軸の回転を行うサンプルです。<br>
![image](https://github.com/Kazuhito00/cv_rotate_3d/assets/37477845/b969c395-87d9-4b1a-b1fb-31038104b54c)

# Requirement
* OpenCV 3.4.2 or later
 
# Usage
サンプルの実行方法は以下です。
```bash
python sample.py
```
```python
import cv2
from cv_rotate_3d import rotate_3d

image = cv2.imread('sample.jpg')

image = rotate_3d(
    image,
    theta=30,
    phi=30,
    gamma=30,
    dx=0,
    dy=0,
    dz=0,
    color=(0, 255, 0),
)

cv2.imshow('cv rotate 3d sample', image)
key = cv2.waitKey(-1)
```

# Note
サンプルの画像は[ぱくたそ](https://www.pakutaso.com/)様の「[モチベーションが死んでる女子校生](https://www.pakutaso.com/20230655173post-47613.html)」を使用しています。

# Author
高橋かずひと
 
# License 
cv_rotate_3d is under [Apache 2.0 license](LICENSE).

