
import re
import requests
import base64
from fontTools.ttLib import TTFont, BytesIO

def get_list(url):
    url = 'https://bj.58.com/dashanzi/chuzu/pn'+page+'/'
    resp = requests.get(url)
    if resp:
        base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}', resp.text)
        try:
            bin_data = base64.b64decode(base64_str[0])
        except:
            print("未拿到数据，可能服务器端由于高频访问需要人工验证")
            return
        #fonts = TTFont(io.BytesIO(bin_data))#复制过来的原代码
        fonts = TTFont(BytesIO(bin_data))#修订后代码
        bestcmap = fonts.getBestCmap()
        newmap = {}
        for key in bestcmap.keys():
            #print(key)
            #print(re.findall(r'(\d+)',bestcmap[key]))
            value = int(re.findall(r'(\d+)',bestcmap[key])[0])-1
            key = hex(key)
            newmap[key] = value

        #print('==========', newmap)
        resp_ = resp.text
        for key,value in newmap.items():
            key_ = key.replace('0x', '&#x') + ';'
            if key_ in resp_:
                resp_ = resp_.replace(key_, str(value))
    
    #对整理好的html代码进行筛选
    #print(len(resp_))
    pat = '<div class="img_list">.*? lazy_src="(.*?)".*?<div class="des">.*?<h2>.*?<a .*?>(.*?)</a>.*?<p class="room strongbox">(.*?) .*?<div class="money">.*?<b class="strongbox">(.*?)</b>'
    dlist = re.findall(pat,resp_,re.S) #re.S修正查找，使得'.'涵盖了所有字符包括换行、空格等
    #print('print directly--',dlist)
    for v in dlist:	
	
        print('标题：%s，图片：%s,户型：%s，价格：%s'%(re.sub(r'\s+','',v[1]),v[0],v[2],v[3]))
        #print(v)

if __name__ == '__main__':
	while True:
		page = input("请输入租房信息页码(或输入q退出)：")
		if page == "q":
			break
		
		get_list(page)
		