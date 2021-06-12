from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import time

#初始化一个浏览器（如：谷歌，使用Chrome需安装chromedriver）
driver = webdriver.Chrome()
#driver = webdriver.PhantomJS() #无界面浏览器
try:
    #请求网页
    driver.get("http://image.baidu.com/")
    #查找id值为kw的节点对象（搜索输入框）
    input = driver.find_element_by_id("kw")
    #模拟键盘输入字串内容
    input.send_keys("街拍")
    #模拟键盘点击回车键
    input.send_keys(Keys.ENTER)
    #显式等待,最长10秒
    wait = WebDriverWait(driver,10)
    #等待条件：10秒内必须有个id属性值为imgContainer的节点加载出来，否则抛异常。
    wait.until(EC.presence_of_element_located((By.ID,'imgContainer')))
    # 输出响应信息
    #print(driver.current_url) #请求url地址
    #print(driver.get_cookies())
    #print(driver.page_source) #获取网页内容
    #
    #将页面滚动条拖到底部
    
    js="var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(4)
    
    driver.execute_script(js)
    time.sleep(4)

    driver.execute_script(js)
    time.sleep(4)
    
    driver.execute_script(js)
    time.sleep(4)

    #print(driver.page_source)

except Exception as err:
    print(err)
finally:
    #关闭浏览器
    #driver.close()
    pass