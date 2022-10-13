import cv2
import os
import numpy as np

#分析した表情と手本の比較（違う点を赤枠で強調表示）
def movie_comparison():
    #img1を改善点があるタイミングの表情の画像
    #img2を手本の画像とする予定
    img_1 = cv2.imread('img1.png')
    img_2 = cv2.imread('img2.png')

    #サイズ設定
    height = img_2.shape[0]
    width = img_2.shape[1]
    img_1 = cv2.resize(img_1 , (int(width), int(height)))

    #色設定（モノクロ）
    img_1_gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    img_2_gray = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

    #違う点のみを抜き出した画像を生成
    img_diff = cv2.absdiff(img_1_gray, img_2_gray)
    #しきい値を設定
    ret2,img_th = cv2.threshold(img_diff,20,255,cv2.THRESH_BINARY)
    #画像全体の輪郭を判別している模様（消すと動かなくなるので残してある）
    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #縦横20ピクセルの赤枠を、ズレのある点に表示
    for i,cnt in enumerate(contours):
        x, y, width, height = cv2.boundingRect(cnt)
        if width > 20 or height > 20:
            cv2.rectangle(img_1, (x, y), (x+width, y+height), (0, 0, 255), 1)

    #赤枠を表示した画像を保存
    cv2.imwrite("diff_image.jpg", img_1)
