import urllib.request
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import prettytable
import sys,os
from IPython.display import display
from IPython.display import clear_output

'''
輸入商品關鍵字
並將結果用prettytable顯示出來
可以輸入頁碼瀏覽其他商品頁
'''

#給定關鍵字輸入
search =input('關鍵字:')

#將輸入字串轉成網頁需要的百分比編碼
encoded_url = urlencode({'search': search}, encoding='utf-8')
encoded_url = encoded_url.replace('search=', '')  

#預設搜尋頁為第1頁
page_search=1

while True:
    
    url='''https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page={}&sort=rnk/dc'''.format(encoded_url,page_search)

    respones=urllib.request.urlopen(url)  #取得網址資料
    html=json.load(respones)   #解析網站資料
    
    fram=prettytable.PrettyTable(['名稱','價格'],encoding='utf-8') #創建格式['列1','列2'] 輸入編碼
    fram.align['名稱']='l'   #列的對齊方式
    fram.align['價格']='c'
    
    
    for i in range(20):
        # print('商品名稱:',html['prods'][i]['name'])
        # print('商品價格:',html['prods'][i]['originPrice'])
            
        fram.add_row([html['prods'][i]['name'],html['prods'][i]['originPrice']])  #將資料填入表格中
        #注意資料列數要跟一開始創建的表格列數相同
    os.system(command='cls') 
    display(fram)
    # print('此商品頁共有:'+str(html['totalPage'])+'頁')
    page_search=int(input('前往頁碼:'))
    
    
    






