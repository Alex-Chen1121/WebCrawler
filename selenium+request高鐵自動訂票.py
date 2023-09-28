import requests
from IPython.display import display
import prettytable as pt
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


# 查詢高鐵票

# start_station = input("請輸入上車站:")
# end_station = input("請輸入下車站:")
# date = input("請輸入乘車日期:")
# time = input("請輸入乘車時間")

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


# def return_time(time):
#     if int(time.split(":")[1]) <30:
#         return str(int(time.split(":")[0])-1)+":30"
#     else:
#         return time.split(":")[0]+":00"
 
url = 'https://www.thsrc.com.tw/TimeTable/Search'

# data = {
#         "SearchType": "S",
#         "Lang": "TW",
#         "StartStation": station_dict[start_station],
#         "EndStation": station_dict[end_station],
#         "OutWardSearchDate": date,
#         "OutWardSearchTime": time,
#         "ReturnSearchDate": date,
#         "ReturnSearchTime": time,
#         "DiscountType":"" 
# }
data = {
        "SearchType": "S",
        "Lang": "TW",
        "StartStation": "NanGang",
        "EndStation": "TaiNan",
        "OutWardSearchDate": "2023/09/29",
        "OutWardSearchTime": "8:00",
        "ReturnSearchDate": "2023/09/29",
        "ReturnSearchTime": "8:00",
        "DiscountType":"" 
}
timee = "8:00"
headers = {":authority":"www.thsrc.com.tw",
           ":method":"POST",
           ":path":"/TimeTable/Search",
           ":scheme":"https",
           "Accept":"*/*",
           "Accept-Encoding":"gzip, deflate, br",
           "Accept-Language":"en-US,en;q=0.9",
           "Content-Length":"190",
           "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
           "Cookie":"_gcl_au=1.1.692045517.1695777542; _td_cid=1741007328.1695777542; _fbp=fb.2.1695777542642.547995837; _gid=GA1.3.119633726.1695777543; _gat_UA-9967381-26=1; AcceptThsrcCookiePolicyTime=Wed%20Sep%2027%202023%2009:19:04%20GMT+0800%20(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93); _ga_1FDVRGS3MR=GS1.1.1695777542.1.1.1695777558.44.0.0; _ga_6M07CCJT7N=GS1.1.1695777542.1.1.1695777559.43.0.0; _ga=GA1.3.178527844.1695777542",
           "Origin":"https://www.thsrc.com.tw",
           "Referer":"https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c",
           "Sec-Ch-Ua":'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
           "Sec-Ch-Ua-Mobile":"?0",
           "Sec-Ch-Ua-Platform":"Windows",
           "Sec-Fetch-Dest":"empty",
           "Sec-Fetch-Mode":"cors",
          " Sec-Fetch-Site":"same-origin",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
           "X-Requested-With":"XMLHttpRequest"
           }

respones = requests.post(url, data)
print(respones.status_code)
data = json.loads(respones.text)

idx = 0
tb = pt.PrettyTable(["序列","車次","出發時間","抵達時間","乘車時間","自由座車廂","優惠類型"], encoding="utf-8")

endStationName = data["data"]["DepartureTable"]["Title"]["EndStationName"]
startStationName = data["data"]["DepartureTable"]["Title"]["StartStationName"]
titleSplit2 = data["data"]["DepartureTable"]["Title"]["TitleSplit2"]

data_index = {}
for i in range(61):     
        departureTime = data["data"]["DepartureTable"]["TrainItem"][i]['DepartureTime']
        destinationTime = data["data"]["DepartureTable"]["TrainItem"][i]['DestinationTime']
        duration = data["data"]["DepartureTable"]["TrainItem"][i]['Duration']
        runDate = data["data"]["DepartureTable"]["TrainItem"][i]['RunDate']
        trainNumber = data["data"]["DepartureTable"]["TrainItem"][i]["TrainNumber"]
        no_reserved = data["data"]["DepartureTable"]["TrainItem"][i]["NonReservedCar"]  
        
        # print(int(departureTime.split(':')[0]))
        if int(departureTime.split(':')[0]) > int(timee.split(":")[0]):
                data_index[idx] = [departureTime,destinationTime,duration,runDate,trainNumber]
                tb.add_row([idx, trainNumber, departureTime, destinationTime, duration, no_reserved, ""])
                idx += 1
        if idx == 10:
            break
print(tb.get_string(title=f"{startStationName}-{endStationName}  乘車日期:{titleSplit2}"))    

your_order = input("請輸入你要的班次(序列號):")
pessenger_id = input("請輸入你的身分證字號:")
phone_number = input("請輸入你的電話號碼:")
your_email = input("請輸入你的電子郵件:")

# 訂票 取票人資訊 身分證字號 連絡電話 電子郵件

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