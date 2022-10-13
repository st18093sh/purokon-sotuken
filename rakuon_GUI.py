import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as flog
from tkinter import ttk
from tkinter import messagebox
import sys,os.path
import subprocess
import wave
from pydub import AudioSegment
import librosa
import soundfile as sf
import struct
from scipy import fromstring, int16
import numpy as np
import math



class Application(tk.Frame):
    def __init__(self, master=None,file_name='out.wav'):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        master.title(u"TSUWA")
        master.geometry("600x500")
        self.cmd = ""
        self.file_na = file_name
        self.p = None
        self.rec_flag = False
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # ウィンドウの x ボタンが押された時に呼ばれるメソッドを設定
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)
    def create_widgets(self):
        #録音開始ボタン
        self.Button1 = tk.Button(text=u'録音開始ボタン',width=20,command=self.button_clickrec)
        self.Button1.grid(row=0,column=0,pady=20)
        #録音停止ボタン
        self.Button2 = tk.Button(text=u'録音停止ボタン',width=20,command=self.button_clickstop)
        self.Button2.grid(row=0,column=1,pady=5)
        #再生ボタン
        self.Button3 = tk.Button(text=u'再生ボタン',width=20,command=self.button_clickplay)
        self.Button3.grid(row=1,column=0,pady=5)
        #再生ボタン
        self.Button4 = tk.Button(text=u'終了',width=20,command=self.button_delete)
        self.Button4.grid(row=1,column=1,pady=5)
        #感情解析
        self.Button5 = tk.Button(text='感情分析',width=20,command=self.button_bunseki)
        self.Button5.grid(row=1,column=2,pady=5)
        #スクロールテキスト
        self.Scrolltext1 = st.ScrolledText()
        self.Scrolltext1.grid(row=2,columnspan=5,padx=20,pady=20)
        label = tk.Label(text='ログ')
        label.place(x=50,y=100)
        
        
    #録音開始
    def button_clickrec(self):
        if self.rec_flag == False:
            self.cmd = "sox -t waveaudio -d "+ self.file_na
            self.p = subprocess.Popen(self.cmd.split())
            self.Scrolltext1.insert('end',u'録音を開始しました\n')
            self.rec_flag = True
            
    def button_bunseki(self):
        import time
        import requests
        import json
        import glob
        url = 'https://api.webempath.net/v2/analyzeWav'

        #ここはご自分のKeyを入力ください
        apikey = 'I9D0hwNxDJpBbDRv2fDtouE3bWpzAuCihpJVzc7bSic'
        payload = {'apikey': apikey}

        ene_sum=0
        joy_sum=0
        count=0

        for wav in glob.glob(r'C:\Users\dishi\pro_con\voice02\voice*.wav'):
            data = open(wav, 'rb')
            file = {'wav': data}
            print(wav)

            res = requests.post(url, params=payload, files=file)
            kekka = json.loads(res.text)
            if kekka['error'] == 1001:
                self.Scrolltext1.insert('API keyが空です')
            elif kekka['error'] == 1002:
                self.Scrolltext1.insert('wavファイル送信されていません')
            elif kekka['error'] == 1003:
                self.Scrolltext1.insert('contet-typeがmulripart/form-dataで始まりません')
            elif kekka['error'] == 1011:
                self.Scrolltext1.insert('wavファイルがPCM_FLOAT,PCM_SIGNED,PCM_UNSIGNEDのいずれにも該当しません')
            elif kekka['error'] == 1012:
                self.Scrolltext1.insert('wavファイルのサンプリング周波数が11025Hz以外です')
            elif kekka['error'] == 1013:
                self.Scrolltext1.insert('wavファイルがモノラルではありません')
            elif kekka['error'] == 1014:
                self.Scrolltext1.insert('wavファイルの録音秒数が5秒以上です')
            elif kekka['error'] == 1015:
                self.Scrolltext1.insert('wavファイルのサイズが1.9MB以上です')
            elif kekka['error'] == 1016:
                self.Scrolltext1.insert('wavファイルが妥当な音声として読み取れません')
            elif kekka['error'] == 1017:
                self.Scrolltext1.insert('不正なAPIバージョンが指定されました')
            elif kekka['error'] == 2001:
                self.Scrolltext1.insert('送信されたAPI keyはAPIコール回数上限を超過しました')
            elif kekka['error'] == 2002:
                self.Scrolltext1.insert('アカウントまたはその状態が不正です')
            elif kekka['error'] == 2003:
                self.Scrolltext1.insert('送信されたAPI key利用可能な状態ではありません')
            elif kekka['error'] == 1017:
                self.Scrolltext1.insert('送信されたAPI keyは利用できないか、存在しません')
            elif kekka['error'] == 1017:
                self.Scrolltext1.insert('不正なAPIバージョンが指定されました')
            elif kekka['error'] == 3001:
                self.Scrolltext1.insert('許可されていない国からのアクセスである')
            elif kekka['error'] == 9999:
                self.Scrolltext1.insert('内部エラー')
                
            ene = kekka['energy']
            joy = kekka['joy']
            joy_sum += joy
            ene_sum += ene
            count += 1
            time.sleep(1)
        
        ene_kekka=ene_sum/count
        joy_kekka=joy_sum/count
        if ene_kekka>30 and joy_kekka>30:
            self.Scrolltext1.insert('end',u'すばらしい\n')
        elif ene_kekka<30 and joy_kekka>30:
            self.Scrolltext1.insert('end',u'楽しいそうですが、元気があまりありません\n')
        elif ene_kekka>30 and joy_kekka<30:
            self.Scrolltext1.insert('end',u'元気ですが、楽しそうではありません\n')
        elif ene_kekka<30 and joy_kekka<30:
            self.Scrolltext1.insert('end',u'元気も楽しそうでもありません\n')
            
    #録音停止
    def button_clickstop(self):
        if self.rec_flag == True:
            self.p.terminate()
            self.Scrolltext1.insert('end',u'録音を終了しました\n')
            try:
                self.p.wait(timeout=1)
                self.rec_flag = False
            except subprocess.TimeoutExpired:
                self.p.kill()
                self.rec_flag = False
        y, sr = librosa.core.load('out001.wav', sr=11025, mono=True) # 22050Hz、モノラルで読み込み
        sf.write("new_out001.wav", y, sr, subtype="PCM_16") #1
        sound = AudioSegment.from_wav("new_out001.wav")
        sound = sound.set_channels(1)
        sound.export("new_out001.wav", format="wav")
        self.Scrolltext1.insert('end',u'wavファイルの変換完了')
        # wavファイルをどの間隔で区切りたいか？（単位[sec]）
        time = 5
        # 分割したいwavファイルの格納先
        audio_change_wav = 'new_out001.wav'
        # wav分割ファイルの格納先
        wav_cut_dir = 'C:/Users/dishi/pro_con/voice02/voice'

        # wav読み込み
        wr = wave.open(audio_change_wav, "r")
    
        # wav情報を取得
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)
        t = int(time)
        frames = int(ch * fr * t)
        # 小数点切り上げ（1分に満たない最後のシーンを出力するため）
        num_cut = int(math.ceil(integer / t))
        data = wr.readframes(wr.getnframes())
        wr.close()
    
        X = np.frombuffer(data, dtype=int16)
    
        for i in range(num_cut):
            outf = wav_cut_dir + str(i) + '.wav'
            start_cut = int(i * frames)
            end_cut = int(i * frames + frames)
            print(start_cut)
            print(end_cut)
            Y = X[start_cut:end_cut]
            outd = struct.pack("h" * len(Y), *Y)
    
            # 書き出し
            ww = wave.open(outf, "w")
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()
        self.Scrolltext1.insert('end',u'音声ファイルの分割ができました\n')
        
    #再生
    def button_clickplay(self):
        if self.rec_flag == False:
            self.cmd = self.file_na + '\n'
            self.p = subprocess.call(self.cmd,shell=True)
            self.Scrolltext1.insert('end',u'再生を実行中。ファイル名：' + self.cmd)

    #録音中に終了したときの処理
    def on_closing(self):
        self.button_clickstop()
        sys.exit()
    
    def button_delete(self):
        # 終了確認のメッセージ表示
        ret = messagebox.askyesno(
            title = "終了確認",
            message = "プログラムを終了しますか？")

        if ret == True:
            # 「はい」がクリックされたとき
            self.master.destroy()

        
    def delete_window(self):
        # 終了確認のメッセージ表示
        ret = messagebox.askyesno(
            title = "終了確認",
            message = "プログラムを終了しますか？")

        if ret == True:
            # 「はい」がクリックされたとき
            self.master.destroy()

#本体
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root,file_name='out001.wav')
    root.configure(bg="gray")
    root.state("zoomed")
    app.mainloop()