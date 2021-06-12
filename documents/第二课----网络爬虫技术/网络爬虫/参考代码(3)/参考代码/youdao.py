#有道翻译使用requests
import requests
import time,random,hashlib

#生成data中salt和sign两个数据
def salt_sign(keyword):
    #m = hashlib.md5()
    now_time = int(time.time()*1000)
    salt = now_time+random.randint(1,10)
    sign = "fanyideskweb" + keyword + str(salt) + "p09@Bn{h02_BIEe]$P^nG"
    #m.update(bytes(sign,encoding='utf-8'))
    #sign = m.hexdigest()
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    return (salt,sign,now_time)
        

def translate(keyword):
    #取出salt,sign和当前时间
    salt,sign,now_time = salt_sign(keyword)
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    #data提交制定
    data = {
        'action':'FY_BY_REALTIME',
        'client':'fanyideskweb',
        'doctype':'json',
        'from':'AUTO',
        'i':keyword,
        'keyfrom':'fanyi.web',
        'salt':salt,
        'sign':sign,
        'smartresult':'dict',
        'to':'AUTO',
        'typoResult':'false',
        'version':'2.1',
	}
    #header信息制定
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        #'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        #'Content-Length':'218',#len(data),
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'Cookie':'OUTFOX_SEARCH_USER_ID=-436151303@10.169.0.83; JSESSIONID=aaajO50X4odGG5auUeLpw; OUTFOX_SEARCH_USER_ID_NCOO=806738224.8182715; fanyi-ad-id=44881; fanyi-ad-closed=1; Hm_lvt_4e5bdf78b2b9fcb88736fc67709f2806=1528556613,1528556720,1528557273; Hm_lpvt_4e5bdf78b2b9fcb88736fc67709f2806=1528557273; Hm_lvt_cc903faaed69cca18f7cf0997b2e62c9=1528556613,1528556720,1528557273; Hm_lpvt_cc903faaed69cca18f7cf0997b2e62c9=1528557273; ___rl__test__cookies'+str(now_time),
        'X-Requested-With':'XMLHttpRequest',
    }

    #将提交信息封装
    res = requests.post(url,data=data,headers=headers)
    #提取reponse的信息
    str_json = res.json()
    #print(str_json)
    print('"%s"\n翻译的内容是:\n%s' % (str_json['translateResult'][0][0]['src'],str_json['translateResult'][0][0]['tgt']))

# 程序主入口
if __name__ == '__main__':
    while True:
        keyword = input('请输入需要翻译的内容:')
        if (keyword == 'q' or keyword == 'Q'):
            print('翻译结束')
            break
        translate(keyword)
        print('='*20)

 