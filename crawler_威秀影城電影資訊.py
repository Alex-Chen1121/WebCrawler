import os
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
# GUI介面
import ttkbootstrap as ttk
# 圖像處理
from PIL import ImageTk, Image

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

        for img in tqdm(img_list):
            name = img["alt"]
            img_url = "https://www.vscinemas.com.tw/vsweb"+img["src"].split(".")[2]+".jpg"
            image = requests.get(img_url)

            with open(dirname+"/"+name+".jpg","wb") as file:
                file.write(image.content)
        print("下載完成")

    
    def get_movie_about(self, movie_name):
        # 下載電影簡介
        details = self.html.find_all("section", class_="infoArea")
        for detail in details:
            if detail.find("h2").find("a").text == movie_name:
                url = "https://www.vscinemas.com.tw/vsweb/film/"+detail.find("h2").find("a")["href"]
                respones = requests.get(url)
                html = BeautifulSoup(respones.text, "html.parser")
                about = html.find("div", class_="bbsArticle").find("p").text
        
        return about
    
    def main():
        vieshow_crawler = Vieshow()
        data = pd.DataFrame(vieshow_crawler.get_movie_info())
        movie_about = vieshow_crawler.get_movie_about("奪魂鋸X")
        vieshow_crawler.get_movie_poster()


# url = "https://www.vscinemas.com.tw/vsweb/film/detail.aspx?id=6835"
# respones = requests.get(url)
# html = BeautifulSoup(respones.text, "html.parser")
# about = html.find("article", class_="hidden")
# print(about)

def show():
    key = search_va.get()
    info = Vieshow()
    ttf = info.get_movie_about(key)
    tree_view.insert(parent="", index=1, values=ttf)

def release():
    xx = Vieshow()
    yy = xx.get_movie_info()
    for i in range(len(yy["movie_name"])):
        tree_view.insert(parent="", index=i+1, 
            values=(i+1,yy["movie_name"][i],yy["english_name"][i],yy["release_date"][i]))



if __name__ == "__main__":
    
    # 設置窗口
    root = ttk.Window(title="電影查詢",size = (1000,700))
    # 居中窗口
    root.place_window_center()
    root.resizable(False, False)
    img = Image.open("vieshow.png")
    photo = ImageTk.PhotoImage(img)
    ttk.Label(root, image=photo).pack()

    input_frame = ttk.Frame()
    input_frame.pack(pady=20)
    search_va = ttk.StringVar()
    ttk.Button(input_frame, text="查詢近期上映電影", command=release).pack(pady=20)
    ttk.Label(input_frame, text="查詢電影詳細資訊", font=80).pack(side=ttk.LEFT,padx=5)
    ttk.Entry(input_frame, textvariable=search_va).pack(side=ttk.LEFT,padx=5)
    ttk.Button(input_frame, text="查詢", command=release).pack(side=ttk.LEFT)

    # 創建資料展示
    columns = ("index", "poster", "release_date", "about")
    columns_value = ("序號", "電影名稱", "英文名稱", "上映日期")

    # 創建表格
    tree_view = ttk.Treeview(root, show="headings", columns=columns)

    # 添加字段名
    tree_view.column("index", width=10, anchor="center")
    tree_view.column("poster", width=200, anchor="w")
    tree_view.column("release_date", width=200, anchor="w")
    tree_view.column("about", width=20, anchor="center")

    # 設置在頁面上顯示的內容
    tree_view.heading("index", text="序號")
    tree_view.heading("poster", text="電影名稱")
    tree_view.heading("release_date", text="英文名稱")
    tree_view.heading("about", text="上映日期")

    # 佈局到頁面上
    tree_view.pack(fill=ttk.BOTH, expand=True)
    root.mainloop()