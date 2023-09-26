# 爬取ig關鍵字圖片
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time,os,wget

PATH = "C:/Users/hibyby/Desktop/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.instagram.com/")
#獲取欄位的資訊
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)
login = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')

username.clear() #怕輸入欄有預設文字
password.clear()
username.send_keys('你的帳號') #自動輸入帳密 建議改用輸入認證的方式
password.send_keys('你的密碼')
login.click() #執行滑鼠點擊
#找到搜尋欄位
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
)
keyword = "#dog"
search.send_keys(keyword) #觀察網頁搜尋需要連續按兩次enter才會搜尋
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "FFVAD")) #找尋照片的共同標籤
)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #使用for迴圈自動執行
    time.sleep(5)

imgs = driver.find_elements_by_class_name("FFVAD")

path = os.path.join(keyword) #儲存檔案設定方式
os.mkdir(path) #創建資料夾

count = 0
for img in imgs:
    save_as = os.path.join(path, keyword + str(count) + '.jpg')
    # print(img.get_attribute("src"))
    wget.download(img.get_attribute("src"), save_as) #使用wget來儲存 (前面放下載路徑, 後面放儲存路徑)
    count += 1