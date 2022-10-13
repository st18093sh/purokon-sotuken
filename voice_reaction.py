import time
import requests
import json
import glob
url = 'https://api.webempath.net/v2/analyzeWav'

#ここはご自分のKeyを入力ください
apikey = 'I9D0hwNxDJpBbDRv2fDtouE3bWpzAuCihpJVzc7bSic'
payload = {'apikey': apikey}

sum=0
count=0

for wav in glob.glob(r'C:\Users\dishi\pro_con\voice02\voice*.wav'):
  #wav = 'voice020.wav' # 「明るく」
  data = open(wav, 'rb')
  file = {'wav': data}
  print(wav)

  res = requests.post(url, params=payload, files=file)
  print(res.json())
  a1 = json.loads(res.text)
  if a1['error'] == 1014:
    print('wavファイルの録音秒数が5秒以上です')
  a2 = a1['energy']
  sum += a2
  count += 1
  time.sleep(1)
  
  

kekka=sum/count
if kekka>30:
  print("すばらしい")
else:
  print("もう少し元気に")

'''
wav = 'new_sayonara_02.wav' # 「涙をこらえて」
data = open(wav, 'rb')
file = {'wav': data}

res = requests.post(url, params=payload, files=file)
print(res.json())
a1 = json.loads(res.text)
a2 = a1['joy']
if a2>30:
  print("すばらしい")
else:
  print("もう少し楽しそうに")
print({a2})
'''