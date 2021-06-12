# 爬取指定城市天气信息
# 和风天气网址：https://console.heweather.com/  账号：122794105@qq.com 密码：python123
import requests
import re,time

#获取城市列表信息
url = 'https://cdn.heweather.com/china-city-list.txt'
res = requests.get(url)
data = res.content.decode('utf-8')

#使用换行符拆分每条城市信息
dlist = re.split("[\n\r]+",data)

#去除多用头信息数据
for i in range(5):
    dlist.remove(dlist[0])
print(len(dlist))

#遍历所有城市信息
for i in range(10):
    #print(dlist[i])
    item = re.split("[\s\|]+",dlist[i])
    url = 'https://free-api.heweather.com/s6/weather?location=%s&key=a46fd5c4f1b54fda9ee71ba6711f09cd'%(item[1])
    res = requests.get(url)
    time.sleep(2)

    #使用json格式获取数据
    datalist = res.json()
    #获取第一条城市信息
    data = datalist['HeWeather6'][0]

    #输出城市信息
    print('城市：',data['basic']['location'])
    print('日期：',data['daily_forecast'][0]['date'])
    print('温度：',data['daily_forecast'][0]['tmp_min'],' ~ ',data['daily_forecast'][0]['tmp_max'])
    print('天气：',data['daily_forecast'][0]['cond_txt_d'],' ~ ',data['daily_forecast'][0]['cond_txt_n'])
    print(data['daily_forecast'][0]['wind_dir'],data['daily_forecast'][0]['wind_sc'],"级")
    print("-"*60)