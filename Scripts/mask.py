# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image

def main(image):
    # PILイメージをNumPy配列に変換
    image_array = np.array(image)

    # 白黒反転する
    img = cv2.bitwise_not(image_array)

    # グレースケールに変換する
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二値化する
    ret, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)

    # 輪郭抽出する
    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 面積が最大の輪郭を取得する
    contour = max(contours, key=lambda x: cv2.contourArea(x))

    # マスクを作成する
    mask = np.zeros_like(image_array)
    cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # マスク画像を保存する
    mask_image = Image.fromarray(mask)


    return mask_image

if __name__ == "__main__":
    image_path = "input27.png"
    init_image = Image.open(image_path).convert("RGB")
    mask_image = main(init_image)
    mask_image_path = image_path.replace(".png", "_mask.png")
    mask_image.save(mask_image_path)