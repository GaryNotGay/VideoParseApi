# Deploied On TencentCloud Serverless Cloud Function
# -*- coding: utf8 -*-
import base64
import time
import requests
import json

def main_handler(event, context):

    videourl = event['path'][7:]
    print("Received event: " + json.dumps(event, indent = 2)) 
    print("Received context: " + str(context))
    print("Hello world")

    videoid = videourl[30:37]
    videotitle = videourl[23:29]
    cookies = {'Your Cookies':'Json Format'}
    did = cookies['__STKUUID']
    timestamp = int(time.time())

    mango_getname_api = 'https://pcweb.api.mgtv.com/video/info?vid=' + videoid + '&cid=' + videotitle + '&_support=10000000&               callback=jsonp_' + str(timestamp)
    mango_getname_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_getname_cookies = cookies
    mango_getname_response = requests.get(url = mango_getname_api, headers = mango_getname_headers, cookies=mango_getname_cookies)
    mango_getname_result = mango_getname_response.content.decode("utf-8")
    mango_getname_result_dict = json.loads(mango_getname_result)

    mango_videoname = mango_getname_result_dict['data']['info']['videoName']
    mango_videotitle = mango_getname_result_dict['data']['info']['title']

    jumpbaseurl = 'https://web-disp.titan.mgtv.com'
    tk2_base = "did=" + did + "|pno=1030|ver=0.3.0301|clit=" + str(int(timestamp/1000))
    tk2_base64 = base64.b64encode(tk2_base.encode("utf-8")).decode("utf-8")
    tk2_mod = tk2_base64.replace("+", "_").replace("/", "~").replace("=", "-")
    tk2_arr = list(tk2_mod)
    tk2_arr.reverse()
    tk2_out = ''.join(tk2_arr)

    mango_tk2pm2_api = "https://pcweb.api.mgtv.com/player/video?did=af0af9f3-35db-48fc-902e-e04e5e3bfb9b&suuid=&cxid=&tk2=" + tk2_out + "&video_id=" + videoid + "&type=pch5&_support=10000000&auth_mode=1&callback=jsonp_" + str(timestamp)
    mango_tk2pm2_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_tk2pm2_cookies = cookies
    mango_tk2pm2_response = requests.get(url = mango_tk2pm2_api, headers = mango_tk2pm2_headers, cookies=mango_tk2pm2_cookies)
    mango_tk2pm2_result = mango_tk2pm2_response.content.decode("utf-8")
    mango_tk2pm2_result_dict = json.loads(mango_tk2pm2_result[17:-1])
    mango_pm2 = mango_tk2pm2_result_dict['data']['atc']['pm2']
    mango_tk2 = mango_tk2pm2_result_dict['data']['atc']['tk2']

    mango_getsouce_api = 'https://pcweb.api.mgtv.com/player/getSource?_support=10000000&tk2=' + mango_tk2 + '&pm2=' + mango_pm2 + '&video_id=' + videoid + '&type=pch5&callback=jsonp_' + str(timestamp)
    mango_getsouce_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_getsouce_cookies = cookies
    mango_getsouce_response = requests.get(url= mango_getsouce_api, headers = mango_getsouce_headers, cookies=mango_getsouce_cookies)
    mango_getsouce_result = mango_getsouce_response.content.decode("utf-8")
    mango_getsouce_result_dict = json.loads(mango_getsouce_result[17:-1])
    jumpurl = ['', '', '', '']
    jumpurllen = len(mango_getsouce_result_dict['data'])
    for index in range(jumpurllen):
        jumpurl[index] = mango_getsouce_result_dict['data']['stream'][index]['url']

    json_outstr = {'VideoUrl' : '', 
                'VideoName' : '', 
                'VideoTitle' : '', 
                '360P' : '', 
                '540P' : '', 
                '720P' : '', 
                '1080P' : '',
                }
    json_outstr['VideoUrl'] = videourl
    json_outstr['VideoTitle'] = mango_videotitle
    json_outstr['VideoName'] = mango_videoname
    for index in range(jumpurllen):
        getm3u8url = jumpbaseurl + jumpurl[index]
        mango_getm3u8_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
        mango_getm3u8_cookies = cookies
        mango_getm3u8_response = requests.get(url= getm3u8url, headers = mango_getm3u8_headers, cookies=mango_getm3u8_cookies)
        mango_getm3u8_result = mango_getm3u8_response.content.decode("utf-8")
        mango_getm3u8_result_dict = json.loads(mango_getm3u8_result)
        m3u8 = mango_getm3u8_result_dict['info']
        if index == 0:
            json_outstr['360P'] = m3u8
        elif index == 1:
            json_outstr['540P'] = m3u8
        elif index == 2:
            json_outstr['720P'] = m3u8
        elif index == 3:
            json_outstr['1080P'] = m3u8

    html_out = base64.b64encode(str(json_outstr).encode("utf-8")).decode("utf-8")
    html = {'Encode':'Base64',
            'Key':'Null',
            'VideoUrl':'',
            'ParseResult':''
            }
    html['VideoUrl'] = videourl
    html['ParseResult'] = html_out
    return html
