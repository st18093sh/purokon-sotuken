import cv2
import os
import pandas
import numpy as np
import PySimpleGUI as sg
from statistics import mean
from threading import Thread

#保存する動画の形式
def videosave_setup(self):
    cam = cv2.VideoCapture(0)
    #保存する動画の形式
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (1280, 720)
    #保存するフォルダとファイル名
    writer = cv2.VideoWriter('facemovie.mp4', fmt, fps, size)

#録画開始
def videosave_start(self, cam, fmt, fps, size):
    _, frame = cam.read()
    frame = cv2.resize(frame, size)
    writer.write(frame)

#録画停止（カメラとファイル書き込みの設定を解除）
def videosave_stop(self):
    writer.release()
    cam.release()

#動画の表情分析のモジュールインストール
def analysis_setup(self):
    from feat import Detector
    detector = Detector(
        face_model     = "retinaface",
        landmark_model = "mobilefacenet",
        au_model       = "svm",
        emotion_model  = "resmasknet",
        facepose_model = "img2pose",
    )
    detector

#動画の感情分析をする関数
def video_analysis(self):
    #py-feat内の、結果を表示するモジュールの設定
    from feat.data import Fex
    fex = Fex()
    #分析するファイルのパス
    video_path = os.path.join("./moviedata/facemovie.mp4")
    #30フレーム（1秒ごと）に分析
    video_prediction = detector.detect_video(video_path, skip_frames = 30)
    #テキストファイルに結果を書き込み
    f = open('result.txt', 'w')
    f.writelines(video_prediction.head())
    f.close()
    #テキストファイルから感情毎に数値を読み込み
    f = open ('result.txt', 'r')
    result = f.readlines()
    anger     = [line for line in result if 'anger' in line]
    disgust   = [line for line in result if 'disgust' in line]
    fear      = [line for line in result if 'fear' in line]
    happiness = [line for line in result if 'happiness' in line]
    sadness   = [line for line in result if 'sadness' in line]
    suprise   = [line for line in result if 'surprise' in line]
    neutral   = [line for line in result if 'neutral' in line]
    f.close()
    #int型に変換
    anger_i    = [int(a) for a in anger]
    disgust_i  = [int(a) for a in anger]
    fear_i     = [int(a) for a in anger]
    happines_i = [int(a) for a in anger]
    sadness_i  = [int(a) for a in anger]
    surprise_i = [int(a) for a in anger]
    neutral_i  = [int(a) for a in anger]
    #平均値算出
    angave = statistics.mean(anger_i)
    disave = statistics.mean(disgust_i)
    feaave = statistics.mean(fear_i)
    hapave = statistics.mean(happiness_i)
    sadave = statistics.mean(sadness_i)
    surave = statistics.mean(surprise_i)
    neuave = statistics.mean(neutral_i)
    #相手がどう感じていたかを表示
    if hapave >= angave:
        if hapave >= disave:
            if hapave >= feaave:
                if hapave >= sadave:
                    if hapave >= surave:
                        if hapave >= neuave:
                            print('相手は、あなたが楽しそうだと感じていました。\n')
    elif angave >= disave:
        if angave >= feaave:
            if angave >= sadave:
                if angave >= surave:
                    if angave >= neuave:
                        print('相手は、あなたが怒っているように感じていました。')
    elif disave >= feaave:
        if disave >= sadave:
            if disave >= surave:
                if disave >= neuave:
                    print('相手は、あなたが嫌そうだと感じていました。')
    elif feaave >= sadave:
        if feaave >= surave:
            if feaave >= neuave:
                print('相手は、あなたが感情豊かだと感じていました。')
    elif sadave >= surave:
        if sadave >= neuave:
            print('相手は、あなたが悲しそうだと感じていました。')
    elif surave >= neuave:
        print('相手は、あなたが感情豊かだと感じていました。')
    elif neutral >= surave:
        print('相手は、あなたが無表情だと感じていました。')
    #自分の画像を保存
    cv2.imwrite('./imagedata/img1.png', video_prediction.plot_detections)
    #自分の画像と手本を表示
    img_0 = cv2.imread('img1.png')
    cv2.imshow('あなたの画像です。', img_0)
    #結果を数値で表示（コメントアウト）
    #video_prediction.head()
    #簡略化した顔と棒グラフを表示（コメントアウト）
    #video_prediction.plot_detections(faceboxes = False, add_titles = False)

#分析した表情と手本の比較（違う点を赤枠で強調表示）
def video_comparison(self):
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

layout = [[sg.Text('「録画開始」ボタンを押すと録画が開始します。')],
          [sg.Text('「録画停止」ボタンを押すと録画が停止します。')],
          [sg.Text('「分析開始」ボタンを押すと分析が始まります。結果が出るまでお待ちください。')],
          [sg.Text('「終了」ボタンでウィンドウが閉じます。')],
          [sg.Button('録画開始', size=(10, 1)), sg.Button('録画停止', size=(10, 1)),
           sg.Button('分析開始', size=(10, 1)), sg.Button('終了', size=(10, 1))],
          [sg.Output(size=(100, 30))]]

window = sg.Window('TSUWA', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break

    elif event == '録画開始':
        print('録画開始')
        self.thread = threading.Thread(target = self.videosave_setup())
        self.thread.start()
        self.thread = threading.Thread(target = self.videosave_start())
        self.thread.start()

    elif event == '録画停止':
        print('録画停止')
        self.thread = threading.Thread(target = self.videosave_stop())
        self.thread.start()

    elif event == '分析開始':
        print('分析開始...しばらくお待ちください...')
        self.thread = threading.Thread(target = self.video_analysis())
        self.thread.start()
        self.thread = threading.Thread(target = self.video_comparison())
        self.thread.start()

window.close()
