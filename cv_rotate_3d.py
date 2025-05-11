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
    transparent: bool = False,
):
    image_height, image_width = image.shape[:2]
    num_channels = image.shape[2] if len(image.shape) == 3 else 1

    is_bgr = num_channels == 3
    is_bgra = num_channels == 4

    if transparent:
        if is_bgr:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            color = color + (0,)
        elif not is_bgra:
            raise ValueError("透過を有効にするには、BGRまたはBGRA画像が必要です。")
    else:
        if is_bgra:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            color = color[:3]

    pitch, yaw, roll = _get_rad(theta, phi, gamma)
    d = np.sqrt(image_height**2 + image_width**2)
    focal = d / (2 * np.sin(roll) if np.sin(roll) != 0 else 1)
    dz_ = focal + dz

    # 射影変換行列を取得
    mat = _get_M(image, focal, pitch, yaw, roll, dx, dy, dz_)

    # 元画像の4隅の座標を取得
    h, w = image.shape[:2]
    corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32).reshape(
        -1, 1, 2
    )

    # 射影変換での変換後の座標を計算
    transformed_corners = cv2.perspectiveTransform(corners, mat)

    # 新しい画像サイズ（見切れない範囲）
    x_coords = transformed_corners[:, 0, 0]
    y_coords = transformed_corners[:, 0, 1]
    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)

    new_w = int(np.ceil(max_x - min_x))
    new_h = int(np.ceil(max_y - min_y))

    # オフセット行列（画像が切れないように中央に移動）
    offset_mat = np.array([[1, 0, -min_x], [0, 1, -min_y], [0, 0, 1]])

    final_mat = offset_mat @ mat

    # warpPerspective で画像変換（見切れ防止＆背景色反映）
    result = cv2.warpPerspective(
        image.copy(),
        final_mat,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=color,
    )

    # 透過不要ならBGRA → BGRへ変換
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
