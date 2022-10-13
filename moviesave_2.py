import cv2
import numpy as np

#動画を保存する関数
def movie_save():
    cam = cv2.VideoCapture(0)

    #保存する動画の形式
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (1280, 720)

    #保存するフォルダとファイル名
    writer = cv2.VideoWriter('./moviedata/facemovie.mp4', fmt, fps, size)

    #Trueの間、録画し続ける（今は無限ループする）
    #録画停止ボタンを押したときに停止するよう、書き直す必要あり
    while True:
        _, frame = cam.read()
        frame = cv2.resize(frame, size)
        writer.write(frame)

    #カメラとファイル書き込みの設定を解除
    writer.release()
    cam.release()
