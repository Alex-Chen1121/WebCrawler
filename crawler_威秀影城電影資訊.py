import requests
import os
from bs4 import BeautifulSoup

# 目標網址:威秀影城網頁
url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx?p=1"
respones = requests.get(url)
html = BeautifulSoup(respones.text, "html.parser")

# response.json()
# response.text

# 創建存放資料夾
dirname = "recent_movie"
if not os.path.exists(dirname):
    os.mkdir(dirname)

# 分析網站資料
movie_info = html.find_all("section", class_="infoArea")
for info in movie_info:
    movie_name = info.find('h2').text
    english_name = info.find('h3').text
    release_date = info.find('time').text
    detail = f"電影名稱:{movie_name}\n英文名稱:{english_name}\n上映日期:{release_date}\n"+"----"*10+"\n"
    with open("recent_movie/movie_list.txt","a") as file:
        file.write(detail)

# 下載電影海報圖片
movie_img = html.find("ul", class_="movieList")
img_list = movie_img.find_all("img")

for img in img_list:
    name = img["alt"]
    img_url = "https://www.vscinemas.com.tw/vsweb"+img["src"].split(".")[2]+".jpg"
    image = requests.get(img_url)

    with open("recent_movie/"+name+".jpg","wb") as file:
        file.write(image.content)

print("下載完成")