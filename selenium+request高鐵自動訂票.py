import requests
from IPython.display import display
import prettytable as pt
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


# 設定目前時間
now_time = time.time()
struct_time = time.localtime(now_time) # 轉成時間元組
timeString = time.strftime("%Y-%m-%d %H:%M:%S", struct_time) # 轉成字串

now_time_hour = timeString.split()[1].split(":")[0]
today = timeString.split()[0].replace("-","/")

# post請求資料
data = {
        'SearchType': 'S', 
        'Lang': 'TW', 
        'StartStation': 'NanGang', 
        'EndStation': 'TaiNan', 
        'OutWardSearchDate': '2023/10/15', 
        'OutWardSearchTime': '8:00', 
        'ReturnSearchDate': '2023/10/15', 
        'ReturnSearchTime': '8:00', 
        'DiscountType': ''
}

# 站名轉換
station_dict = {
        "南港":"NanGang",
        "台北":"TaiPei",
        "板橋":"BanQiao",
        "桃園":"TaoYuan",
        "新竹":"HsinChu",
        "苗栗":"MiaoLi",
        "台中":"TaiChung",
        "彰化":"ChangHua",
        "雲林":"YunLin",
        "嘉義":"ChiaYi",
        "台南":"TaiNan",
        "左營":"ZuoYing",
}

# 建立爬蟲類別
class Taiwan_highway():

    def __init__(self, departure, destination, date=today):
        self.departure = departure
        self.destination = destination
        self.date = date
        self.url = 'https://www.thsrc.com.tw/TimeTable/Search'
        self.dict = station_dict 

    def get_timetable(self):
        
        data["StartStation"] = self.dict[self.departure]
        data["EndStation"] = self.dict[self.destination]
        data["OutWardSearchDate"] = self.date
        data["ReturnSearchDate"] = self.date

        respones = requests.post(self.url, data)
        if respones.status_code == 200:
            print("查詢成功")
        date_info = json.loads(respones.text)
        idx = 0
        tb = pt.PrettyTable(["序列","車次","出發時間","抵達時間","乘車時間","自由座車廂","優惠類型"], 
                            encoding="utf-8"
                            )

        
        data_index = {}
        for i in range(61):     
            departureTime = date_info["data"]["DepartureTable"]["TrainItem"][i]['DepartureTime']
            destinationTime = date_info["data"]["DepartureTable"]["TrainItem"][i]['DestinationTime']
            duration = date_info["data"]["DepartureTable"]["TrainItem"][i]['Duration']
            runDate = date_info["data"]["DepartureTable"]["TrainItem"][i]['RunDate']
            trainNumber = date_info["data"]["DepartureTable"]["TrainItem"][i]["TrainNumber"]
            no_reserved = date_info["data"]["DepartureTable"]["TrainItem"][i]["NonReservedCar"]
            
            if int(departureTime.split(':')[0]) > int(now_time_hour):
                data_index[idx] = [departureTime,destinationTime,duration,runDate,trainNumber]
                tb.add_row([idx, trainNumber, departureTime, destinationTime, duration, no_reserved, ""])
                idx += 1
            if idx == 10:
                break
        
        return tb.get_string(title=f"{self.departure}-{self.destination}  乘車日期:{self.date}")




# 查詢高鐵票
startstation = input("請輸入上車站:")
endstation = input("請輸入下車站:")

# 可以自行填入要的日期
titme_table = Taiwan_highway(startstation, endstation)

tb = titme_table.get_timetable()
print(tb)

# 訂票 取票人資訊 身分證字號 連絡電話 電子郵件
your_order = input("請輸入你要的班次(序列號):")
pessenger_id = input("請輸入你的身分證字號:")
phone_number = input("請輸入你的電話號碼:")
your_email = input("請輸入你的電子郵件:")



option = webdriver.FirefoxOptions()
# option.add_experimental_option("excludeSwiches", ["enable-automation"])
# option.add_experimental_option("useAutomationExtension", False)
option.add_argument("--disable-blink-features=AutomationControlled")
# option.add_argument('--headless')

# 創建瀏覽器物件
driver = webdriver.Firefox(options=option)
url2 = "https://irs.thsrc.com.tw/IMINT/?utm_source=thsrc&utm_medium=btnlink&utm_term=booking"
driver.get(url2)
driver.find_element(by="id", value="cookieAccpetBtn").click()
time.sleep(1)
select = Select(driver.find_element(by="name", value="selectStartStation"))
time.sleep(1)
select.select_by_value("1")
select2 = Select(driver.find_element(by="name", value="selectDestinationStation"))
time.sleep(1)
select2.select_by_value("12")
time.sleep(2)
select3 = Select(driver.find_element(by="name", value="toTimeTable"))
select3.select_by_value("1000P")
driver.implicitly_wait(10)
a = driver.find_element(By.XPATH, '//*[@id="BookingS1Form"]/div[3]/div[2]/div/div[1]/div[1]/input[2]')
js = 'arguments[0].removeAttribute("readonly");'
driver.execute_script(js, a)
driver.implicitly_wait(10)

a.clear()
a.send_keys("2023/10/03")
a.submit()
time.sleep(1)
valid = driver.find_element(By.ID, "securityCode")
valid_num = input("請輸入驗證碼:")
driver.implicitly_wait(10)
valid.send_keys(valid_num)
time.sleep(3)
driver.find_element(by="id", value="SubmitButton").click()