import os
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


class Vieshow():

    def __init__(self) -> None:
        # 目標網址:威秀影城網頁
        self.url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx?p=1" 
        respones = requests.get(self.url) 
        self.date = datetime.date.today() 
        self.html = BeautifulSoup(respones.text, "html.parser")
         

    def get_movie_info(self):

        movie_info = self.html.find_all("section", class_="infoArea")
        movie_name, english_name, release_date = [], [], []

        for info in movie_info:
            movie_name.append(info.find('h2').text)
            english_name.append(info.find('h3').text)
            release_date.append(info.find('time').text)
        
        info_dict = {}    
        info_dict["movie_name"] = movie_name
        info_dict["english_name"] = english_name
        info_dict["release_date"] = release_date
        
        return info_dict

    
    def get_movie_poster(self):    
        # 下載電影海報圖片
        movie_img = self.html.find("ul", class_="movieList")
        img_list = movie_img.find_all("img")

        dirname = "recent_movie"+str(self.date)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        for img in img_list:
            name = img["alt"]
            img_url = "https://www.vscinemas.com.tw/vsweb"+img["src"].split(".")[2]+".jpg"
            image = requests.get(img_url)

            with open(dirname+"/"+name+".jpg","wb") as file:
                file.write(image.content)
        print("下載完成")

    
    def get_movie_about(self, movie_name, date="default"):
        # 下載電影簡介
        details = self.html.find_all("section", class_="infoArea")
        for detail in details:
            if detail.find("h2").find("a").text == movie_name:
                url = "https://www.vscinemas.com.tw/vsweb/film/"+detail.find("h2").find("a")["href"]
                respones = requests.get(url)
                html = BeautifulSoup(respones.text, "html.parser")
                about = html.find("div", class_="bbsArticle").find("p").text
        
        return about

# url = "https://www.vscinemas.com.tw/vsweb/film/detail.aspx?id=6835"
# respones = requests.get(url)
# html = BeautifulSoup(respones.text, "html.parser")
# about = html.find("article", class_="hidden")
# print(about)


if __name__ == "__main__":
    
    vieshow_crawler = Vieshow()
    data = pd.DataFrame(vieshow_crawler.get_movie_info())
    movie_about = vieshow_crawler.get_movie_about("周處除三害")
    print(movie_about)