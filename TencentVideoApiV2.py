# -*- coding: utf8 -*-
import requests
import json
import time
import base64
import random
import math
import re
import urllib

#static
defn = { '270P': 'sd', '480P': 'hd', '720P': 'shd', '1080P': 'fhd'}
guid=cmid="f43616973df5c7173b04c5570b550e53"
unid="2b719ec2136e11eb981ca0429186d00a"
platform = "10201"
cookie = {
    # main cookie
    "main_login": "qq",
    "vqq_openid": "0AD48D3DD18736F8BD22554C572DC5FA",
    "vqq_appid": "101483052",
    "vqq_access_token": "FE3F45516920FDA355D550B4C4A83707",
    "vqq_vuserid": "110127313",
    "vqq_vusession": "oSqiXk3WIWdTzPJePJ3ykg..",
    # other dynaic cookie
    "vqq_refresh_token": "3398E835C7DC0CCAF48A3B3674CAFD18",
    "vqq_next_refresh_time": "5625",
    "vqq_login_time_init": "1607495621",
    # static cookie
    "pgv_pvid":"1297244150",
    "pgv_pvi":"3112349696",
    "pgv_info":"",
    "RK":"W8Lgg0oiF0",
    "ptcz":"e0e4d37cd28165a8e8d166ff979d377eaf92a68ab69c47c9941bf599f2016a34",
    "o_cookie":"1219436885",
    "pac_uid":"1_1219436885",
    "tvfe_boss_uuid":"6306a6a283914291",
    "iip":"0",
    "ptui_loginuin":"1219436885",
    "video_platform":"2",
    "video_guid":"63545d4804b49d11",
    "ssid":"s4148476470",
    "uid":"1540222",
    "login_time_last":"2020-12-9 14:33:42"
}

HEADERS = {
    "authority": "access.video.qq.com",
    "method": "GET",
    "path": "", #"/user/auth_refresh?vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe&type=qq&g_tk=&g_vstk=636569075&g_actk=2029750630&callback=jQuery19108465336335045099_1607495844456&_=1607495844457",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "referer": "https://v.qq.com/",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57",
    "cookie":""
}

vinfoparam = {
    "charge": "0",
    "defaultfmt": "auto",
    "otype": "ojson",
    "guid": None,
    "flowid": None,
    "platform": "10201",
    "sdtfrom": "v1010",
    "defnpayver": "1",   # 0
    "appVer": "3.5.57",
    "host": "v.qq.com",
    "ehost": None,    # base_url
    "refer": "v.qq.com",
    "sphttps": "1",
    "tm": None,
    "spwm": "4",
    "logintoken": None,   #
    "unid": None,
    "vid": None,
    "defn": None,
    "fhdswitch": "0",   # 1
    "show1080p": "1",
    "isHLS": "1",
    "dtype": "3",
    "sphls": "2",               # hls m3u8 content in json
    "spgzip": "1",
    "dlver": "2",
    "drm": "32",
    "hdcp": "0",
    "spau": "1",
    "spaudio": "15",
    "defsrc": "2",                # 1
    "encryptVer": "9.1",
    "cKey": None,
    "fp2p": "1",
    "spadseg": "3",            # "https:" === location.protocol ? 1 : 0,
    #"onlyGetinfo": "true",
    #"adsid": "",
    #"adpinfo": """,
}

adparam = {
    "pf": "in",
    "ad_type" : "LD|KB|PVL",
    "pf_ex": "pc",
    "url": None,    # base_url
    "refer": "v.qq.com",
    "ty": "web",
    "plugin": "1.0.0",
    "v" : "3.5.57",
    "coverid": None,
    "vid" : None,
    "pt": "",
    "flowid": None,
    "vptag": "",
    "pu": "-1",
    "chid": "0",
    "adaptor": "2",
    "dtype": "1",
    "live": "0",
    "resp_type": "json",
    "guid": None,
    "req_type" : "1",
    "from": "0",
    "appversion": "1.0.152",
    "uid": cookie["vqq_vuserid"],                  #vuserid
    "tkn": cookie["vqq_vusession"],   #vusession
    "lt": "qq",                          #main_login
    "platform": "10201",
    "opid": cookie["vqq_openid"],  #openid
    "atkn": cookie["vqq_access_token"],             #access_token
    "appid": cookie["vqq_appid"],                                   #appid
    "tpid": "106",
    "rfid": None
}

def getCookie():
    url = COS-URL
    result = requests.get(url)
    #print(result.content.decode('utf-8').replace("\'", "\"").encode('utf-8'))
    result_json = json.loads(result.content.decode('utf-8').replace("\'", "\"").encode('utf-8'))
    cookie["vqq_vuserid"] = str(result_json["vuserid"])
    cookie["vqq_vusession"] = result_json["vusession"]
    cookie["vqq_access_token"] = result_json["access_token"]

def cookie2header():
    cookies = ''
    for key in cookie:
        cookies += key
        cookies += '='
        cookies += cookie[key]
        cookies += ';'
    return cookies

# Powerd By Zsaim
def getid(url):  
    mode = [
        '.*v\.qq\.com/x/cover/(.*)\.html\?vid=(.*)',
        '.*v\.qq\.com/x/cover/(.*)/(.*)\.html',
        '.*v\.qq\.com/x/page/(.*)\.html',
    ]
    for _ in mode:
        matchres = re.match(_, url)
        if matchres == None:
            pass
        else:
            matchres = matchres.groups()
            vid = matchres[-1]
            if len(matchres) == 2:
                coverid = matchres[0]
            else:
                coverid = ""
    return vid, coverid

def getVideoInfo(url):
    response = requests.get(url)
    result = response.content.decode('utf-8')
    start = result.find('var VIDEO_INFO')
    index = start+1+len('var VIDEO_INFO')
    while result[index] != '}':
        index += 1
    #print(result[start+len('var VIDEO_INFO')+3: index+1])
    video_info = json.loads(result[start+len('var VIDEO_INFO')+3: index+1])
    return video_info['title'], video_info['duration']   #, video_info['vid']

def getTM():
    return str(int(time.time()))

def getCkey(vid, guid, tm):
    url = 'http://api.sometools.online/release/ckey91/10201+3.5.57+'+vid+'+'+guid+'+'+str(tm)
    response = requests.get(url)
    ckey = response.text[1:-1]
    return ckey

def createPID():
    a = 32
    b = ''
    for index in range(32):
        d = hex(math.floor(16*random.random()))
        b += d[2:]
    return b

def getFlowid(pid, plat):
    return createPID() + '_10201'

def getM3U8():
    data = {"buid":"vinfoad","adparam":None,"vinfoparam":None}
    data["adparam"] = urllib.parse.urlencode(adparam)
    data["vinfoparam"] = urllib.parse.urlencode(vinfoparam)
    datas = json.dumps(data)
    #print(datas)
    result = requests.post(url='https://vd.l.qq.com/proxyhttp', data=datas).text
    result_json = json.loads(result)
    video_info = json.loads(result_json["vinfo"])
    return video_info["vl"]["vi"][0]["ul"]["ui"][0]["url"]
    #print(video_info["vinfo"]["vl"]["vi"][0]["ul"]["ui"][0]["url"])

def getRFID(tm):
    return "8fbfbb360af08628d01a2f8cfc05149f_"+tm

def getTM1000():
    return str(int(time.time()*1000))

def time33(t):
    """
    time33: function(t) {
        for (var e = 0, n = t.length, i = 5381; e < n; ++e)
            i += (i << 5) + t.charAt(e).charCodeAt();
        return 2147483647 & i
    }
    """
    i = 5381
    for e in range(len(t)):
        i += (i << 5) + ord(t[e])
    return 2147483647 & i

def main_handler(event, context):
    url = event['path'][6:]

    JsonOut = {'VideoUrl':'',
           'VideoName':'',
           'VideoLength':'',
           '1080P':'',
           '720P':'',
           '480P':'',
           '270P':''
          }
    
    JsonEncode = {'Encode':'Base64',
                'Key':'Null',
                'VideoUrl':'',
                'ParseResult':''
                }

    for key in defn:
        vinfoparam["defn"] = defn[key]
        #url = "https://v.qq.com/x/cover/bzfkv5se8qaqel2/j002024w2wg.html"
        adparam["url"] = url
        vinfoparam["ehost"] = url
        adparam["refer"] = url
        adparam["guid"] = guid
        vinfoparam["guid"] = guid
        vinfoparam["unid"] = unid
        
        id = getid(url)
        vid = id[0]
        coverid = id[1]
        adparam["vid"] = vid
        vinfoparam["vid"] = vid
        adparam["coverid"] = coverid
        pid = createPID()
        tm = getTM()
        vinfoparam["tm"] = tm
        ckey = getCkey(vid, guid, tm)
        vinfoparam["cKey"] = ckey
        flowid = getFlowid(pid, platform)
        adparam["flowid"] = flowid
        vinfoparam["flowid"] = flowid
        vinfoparam["logintoken"] = cookie
        adparam["rfid"] = getRFID(tm)
        m3u8 = getM3U8()
        JsonOut[key] = m3u8

    VideoInfo = getVideoInfo(url)
    VideoName = VideoInfo[0]
    VideoDura = VideoInfo[1]
    JsonOut['VideoUrl'] = url
    JsonOut['VideoName'] = VideoName
    JsonOut['VideoLength'] = VideoDura

    JsonEncode['VideoUrl'] = url
    outstr = base64.b64encode(str(JsonOut).encode('utf-8')).decode('utf-8')
    JsonEncode['ParseResult'] = outstr

    return JsonEncode
