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
