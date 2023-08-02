from math import pi

import cv2
import numpy as np


def rotate_3d(
        image,
        theta=0,
        phi=0,
        gamma=0,
        dx=0,
        dy=0,
        dz=0,
        color=(0, 0, 0),
):
    image_height = image.shape[0]
    image_width = image.shape[1]

    # ピッチ、ヨー、ロールを算出
    pitch, yaw, roll = _get_rad(theta, phi, gamma)

    # 焦点距離算出
    d = np.sqrt(image_height**2 + image_width**2)
    focal = d / (2 * np.sin(roll) if np.sin(roll) != 0 else 1)
    dz_ = focal + dz

    # 射影変換用の行列を生成
    mat = _get_M(image, focal, pitch, yaw, roll, dx, dy, dz_)

    return cv2.warpPerspective(
        image.copy(),
        mat,
        (image_width, image_height),
        borderValue=color,
    )


def _get_rad(pitch, yaw, roll):
    return (_deg_to_rad(pitch), _deg_to_rad(yaw), _deg_to_rad(roll))


def _deg_to_rad(deg):
    return deg * pi / 180.0


def _get_M(image, focal, pitch, yaw, roll, dx, dy, dz):
    image_height = image.shape[0]
    image_width = image.shape[1]

    w = image_width
    h = image_height
    f = focal

    # 2次元射影変換行列 -> 3次元射影変換行列
    A1 = np.array([[1, 0, -w / 2], [0, 1, -h / 2], [0, 0, 1], [0, 0, 1]])

    # 回転行列生成
    RX = np.array([[1, 0, 0, 0], [0, np.cos(pitch), -np.sin(pitch), 0],
                   [0, np.sin(pitch), np.cos(pitch), 0], [0, 0, 0, 1]])
    RY = np.array([[np.cos(yaw), 0, -np.sin(yaw), 0], [0, 1, 0, 0],
                   [np.sin(yaw), 0, np.cos(yaw), 0], [0, 0, 0, 1]])
    RZ = np.array([[np.cos(roll), -np.sin(roll), 0, 0],
                   [np.sin(roll), np.cos(roll), 0, 0], [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    R = np.dot(np.dot(RX, RY), RZ)

    # 3次元射影変換行列 -> 2次元射影変換行列
    A2 = np.array([[f, 0, w / 2, 0], [0, f, h / 2, 0], [0, 0, 1, 0]])

    # 射影変換行列生成
    T = np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])
    return np.dot(A2, np.dot(T, np.dot(R, A1)))
