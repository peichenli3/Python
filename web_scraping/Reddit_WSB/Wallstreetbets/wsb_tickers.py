from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
# 启动爬虫浏览器
driver=webdriver.Chrome(executable_path='C:/Users/90596/Downloads/chromedriver_win32/chromedriver.exe')
# 目标网址
play_url = 'https://dayminer.herokuapp.com/'
# 封装请求头信息
headers_ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}
# 请求目标网址
driver.get(play_url)

time.sleep(5) # 这个是留给浏览器加载的时间，如果网速慢的话可以把数字增大一些

# 获取目标网址HTML源代码
html = driver.page_source
soup1 = BeautifulSoup(html,'lxml')

# 从HTML源代码中搜索选择你需要的文本信息
res_dynamic_symbol = soup1.select("div.grid-item.symbol-col")
res_dynamic_score = soup1.select("div.grid-item.count-col")

# 把symbol 和score放入list中
symbol = []
score = []
for mono_symbol in res_dynamic_symbol:
    symbol.append(mono_symbol.get_text())
for mono_score in res_dynamic_score:
    score.append(mono_score.get_text())

# 写入文件
df1 = pd.DataFrame(list(zip(symbol, score)))
df1.to_csv("wsb.csv",header=False,index=False)

