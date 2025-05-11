from math import pi
import cv2
import numpy as np


def rotate_3d(
    image,
    theta=0,  # ピッチ角（X軸回転）
    phi=0,  # ヨー角（Y軸回転）
    gamma=0,  # ロール角（Z軸回転）
    dx=0,  # X方向の平行移動
    dy=0,  # Y方向の平行移動
    dz=0,  # Z方向の平行移動
    color=(0, 0, 0),  # 背景色（transparent=False時に有効）
    transparent: bool = False,  # 背景を透明にするかどうか
):
    image_height, image_width = image.shape[:2]
    num_channels = image.shape[2] if len(image.shape) == 3 else 1

    # チャンネル数を確認（3=BGR, 4=BGRA）
    is_bgr = num_channels == 3
    is_bgra = num_channels == 4

    # 透過処理の有無に応じてチャンネル変換
    if transparent:
        if is_bgr:
            # BGR → BGRA に変換し、背景色のアルファ値を0に
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            color = color + (0,)
        elif not is_bgra:
            raise ValueError("透過を有効にするには、BGRまたはBGRA画像が必要です。")
    else:
        if is_bgra:
            # BGRA → BGR に変換し、アルファ値を無視
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            color = color[:3]

    # 回転角度（度）をラジアンに変換
    pitch, yaw, roll = _get_rad(theta, phi, gamma)

    # 画像の対角長を基に焦点距離を推定
    d = np.sqrt(image_height**2 + image_width**2)
    focal = d / (2 * np.sin(roll) if np.sin(roll) != 0 else 1)
    dz_ = focal + dz  # Z方向のオフセットを加味

    # 射影変換行列を生成
    mat = _get_M(image, focal, pitch, yaw, roll, dx, dy, dz_)

    # warpPerspectiveで変換を実行（背景色または透過色を適用）
    result = cv2.warpPerspective(
        image.copy(),
        mat,
        (image_width, image_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=color,
    )

    # 透過を使わない場合はBGRに戻す
    if not transparent and result.shape[2] == 4:
        result = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR)

    return result


def _get_rad(pitch, yaw, roll):
    """角度をラジアンに変換"""
    return (_deg_to_rad(pitch), _deg_to_rad(yaw), _deg_to_rad(roll))


def _deg_to_rad(deg):
    """度をラジアンに変換"""
    return deg * pi / 180.0


def _get_M(image, focal, pitch, yaw, roll, dx, dy, dz):
    """3次元射影変換行列を生成"""
    h, w = image.shape[:2]
    f = focal

    # 原点を画像中心に移動
    A1 = np.array([[1, 0, -w / 2], [0, 1, -h / 2], [0, 0, 1], [0, 0, 1]])

    # 回転行列（X軸・Y軸・Z軸）
    RX = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch), 0],
            [0, np.sin(pitch), np.cos(pitch), 0],
            [0, 0, 0, 1],
        ]
    )

    RY = np.array(
        [
            [np.cos(yaw), 0, -np.sin(yaw), 0],
            [0, 1, 0, 0],
            [np.sin(yaw), 0, np.cos(yaw), 0],
            [0, 0, 0, 1],
        ]
    )

    RZ = np.array(
        [
            [np.cos(roll), -np.sin(roll), 0, 0],
            [np.sin(roll), np.cos(roll), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # 回転行列合成
    R = RZ @ RY @ RX

    # 投影行列（3D → 2D）
    A2 = np.array([[f, 0, w / 2, 0], [0, f, h / 2, 0], [0, 0, 1, 0]])

    # 平行移動行列
    T = np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

    # 射影変換行列を返す
    return A2 @ T @ R @ A1
