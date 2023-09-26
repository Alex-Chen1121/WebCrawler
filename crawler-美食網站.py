import urllib.request
from bs4 import BeautifulSoup


url='https://tabelog.com/tw/tokyo/rstLst/?SrtT=rt'
html=urllib.request.urlopen(url)
response=BeautifulSoup(html)  #解析網站 讓得到的資訊跟開發者模式看到的一樣
print(response)

#find 找到第一個符合條件的 find_all 找所有符合條件的
print(response.find_all('li',class_='list-rst'))

for r in response.find_all('li',class_='list-rst'):  #因為class在py中已有用途 因此多加一個底線
    ja=r.find('small',class_='list-rst__name-ja')
    en=r.find('a',class_='list-rst__name-main js-detail-anchor')
    #萃取內容(.text) 網頁上直接看到的內容    #萃取特別特徵([特徵]) 例如:href之類的
    print('日本店名:',ja.text)
    print('英文店名:',en.text)
    print('該店網址:',en['href'])

    with open('1121.txt','a',encoding='utf-8') as file:  #直接新增檔案 只有資料夾才要另外建
        file.write('日本店名:'+ja.text+'\n')
