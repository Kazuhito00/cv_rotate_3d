import cv2
from cv_rotate_3d import rotate_3d

image = cv2.imread("sample.jpg")

temp_image = rotate_3d(
    image,
    theta=30,
    phi=30,
    gamma=30,
    color=(0, 255, 0),
)

cv2.imshow("cv rotate 3d sample", temp_image)
key = cv2.waitKey(-1)

temp_image = rotate_3d(
    image,
    theta=30,
    phi=30,
    gamma=30,
    transparent=True,
)

cv2.imshow("cv rotate 3d sample(transparent)", temp_image)
key = cv2.waitKey(-1)
