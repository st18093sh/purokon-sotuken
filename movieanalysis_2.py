import os

#py-featのモジュール設定（これのせいでGUIが動かない可能性あり）
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
def movie_analysis():
    #py-feat内の、結果を表示するモジュールの設定
    from feat.data import Fex
    fex = Fex()

    #分析するファイルのパス
    video_path = os.path.join("./moviedata/facemovie.mp4")

    #30フレーム（1秒ごと）に分析
    video_prediction = detector.detect_video(video_path, skip_frames = 30)
    #結果を数値で表示（コメントアウト）
    #video_prediction.head()
    #簡略化した顔と棒グラフを表示（コメントアウト）
    #video_prediction.plot_detections(faceboxes = False, add_titles = False)
