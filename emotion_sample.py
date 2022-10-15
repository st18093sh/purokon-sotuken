import glob
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

#---------------------複数データを読み込み--------------------------
datseta = []
melspects = []
for file_name in glob.glob('dir/*.wav'):
    y, sr = librosa.load('onsei.wav')
    dataset.append(y)
    #y : 音声データ　振幅幅が連続したnumpy.array
    # sr = サンプリングレート値

#--------------------メルスペクトログラムの計算---------------------
#音声波形を複数のsin波に分解し、周波数と振幅と時間の情報を持たせ、
#　高音低温の粗さを考慮したデータ　
    melspec = librosa.feature.melspectgram(y,sr)
    melspec = librosa.amplitude_to_db(melspec).flatten()
    melspecs.append(melspec.astype(np.float16))

#--------------------各データの振幅の平均値-----------------------
mean = np.sqrt(np.mean(dataset**2,axis=1))

#--------------------各データのゼロクロス数----------------------
zc = np.sum(librosa.zero_crossings(dataset),axis=1)

#-------------------機械学習データにする。------------------------
train_feature = pd.DataFrame()
train_feature['mean'] = mean
train_feature['zc'] = zc
train_feature['melspects'] = melspects
train_labels = #正常・異常などを表すラベル

#機械学習 : 教師あり
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(train_feature, train_labels)

#予測
pred = model.predict(test_feature)
