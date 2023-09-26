import urllib.request
from bs4 import BeautifulSoup
import os
import requests

#輸入搜尋目標
searching_target=input()

#目標網址
url='https://unsplash.com/s/photos/{}'.format(searching_target)

#取得網路回應資料
response=urllib.request.urlopen(url)

#解析網頁架構
html=BeautifulSoup(response,"html.parser")
result=html.find_all('div', class_= 'MorZF', limit=20) #找出圖片的下載連結 #limit=5限制找五個

#建立資料夾
dirname=searching_target
if not os.path.exists(dirname):
    os.mkdir(dirname)

fn=1

#依序讀出資料
for r in result:
    img=r.find('img')
    img_link=img['src']
    img_file=requests.get(img_link)  #下載

    # img_link.split('-')[1]
    # print(img_link)

    #指定下載資料夾
    with open(f'{dirname}/'+ str(fn)+ '.jpg', 'wb') as file: #寫入圖片的二進碼(wb)
        file.write(img_file.content)
    fn+=1