# -*- coding: utf8 -*-
import json
import time
import random
import hashlib
import base64
import requests
import urllib.parse

def md5(s):
    return hashlib.md5(s.encode('utf8')).hexdigest()

def getTM():
    return str(int(time.time() * 1000))

def get_kuid():
    macid = ''
    chars = 'abcdefghijklnmopqrstuvwxyz0123456789'
    size = len(chars)
    for i in range(32):
        macid += list(chars)[random.randint(0, size - 1)]
    return macid

def getVF(string):
    url = 'http://api.sometools.online/release/cmd5xdash/'+str(string)
    response = requests.get(url)
    result = response.content.decode('utf-8')
    return result[1:-1]

def getVideoInfo(url):
    response = requests.get(url)
    result = response.content.decode('utf-8')
    tvid_index_start = result.find('param[\'tvid\'] = \"')
    vid_index_start = result.find('param[\'vid\'] = \"')
    tvid = result[tvid_index_start+len('param[\'tvid\'] = \"'):vid_index_start]
    vid = result[vid_index_start+len('param[\'vid\'] = \"'):]
    start = result.find('page-info')
    end = result.find('video-info')
    resultJson = json.loads(result[start+len('page-info')+2: end-4])
    tvid = resultJson['tvId']
    vid = resultJson['vid']
    #print(tvid)
    #print(vid)
    return tvid, vid

def getUrl(tvid, vid, bid):
    baseurl = 'https://cache.video.iqiyi.com/dash?'
    #tvid = '2922791537225900'
    #bid = '600' 200--360P 300--540P 500--720P 600--1080P
    #vid = '0d753a6b6ee8b6d8b96505a5fec60d1e'
    src = '01010031010000000000' # static
    #salt h2l6suw16pbtikmotf0j79cej4n8uw13
    vt = '0' # static
    rs = '1' # static
    uid = '1087565853' # P0003
    ori = 'pcw' # static
    ps = '0' # static
    tm = getTM()
    #tm = '1606638369010'
    qd_v = '2' # static
    k_uid = '06620b78f2d7f96b516c5b55a20d853b'  # static
    #k_uid = get_kuid()
    pt = '0'  # static
    d = '0'  # static
    #authKey = '7ff96de0fcf393c9a7acbf5dba63e22c'
    authKey = md5("d41d8cd98f00b204e9800998ecf8427e"+tm+tvid)
    k_tag = '1'  # static
    ost = '0' # static
    ppt = '0'  # static
    # bop = '%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a0e1a63a7d64134d6b976194f798712efe50967ea82a3ee7351be279eb44a2bbb6%22%7D' # {"version":"10.0","dfp":"a0e1a63a7d64134d6b976194f798712efe50967ea82a3ee7351be279eb44a2bbb6"}
    # dfp = 'a0e1a63a7d64134d6b976194f798712efe50967ea82a3ee7351be279eb44a2bbb6'
    dfp = 'a0bc5541cebb2a45fba3d2a345595bcb9a5fd9ba71ff9606fd5a13bd92de5d3ace' # Cookie
    bop = '{"version":"10.0","dfp":"' + dfp + '"}'
    locale = 'zh_cn' # static
    prio = '%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D' # {"ff":"f4v","code":2}
    #prio = '{"ff":"f4v","code":2}'
    k_ft1 = '706436220846084'
    k_ft4 = '1162183859249156'
    k_ft5 = '1' # static
    #pck = 'baddHiyIfHUoV4nVedBHcxMRXWNbVv5rgIeLN6BWlawDBNMGBIntrNfRnm2harxD5Yp4c' # P00001
    pck = renewP()
    k_err_retries = '0' # static
    ut = '1' # static
    up = ''
    qdy = 'a'
    qds = '0'

    url = 'tvid='+tvid+'&bid='+bid+'&vid='+vid+'&src='+src+'&vt='+vt+'&rs='+rs+'&uid='+uid+'&ori='+ori+'&ps='+ps+'&k_uid='+k_uid+'&pt='+pt+'&d='+d+'&s=&lid=&cf=&ct=&authKey='+authKey+'&k_tag='+k_tag+'&ost='+ost+'&ppt='+ppt+'&dfp='+dfp+'&locale='+locale+'&prio='+prio+'&pck='+pck+'&k_err_retries='+k_err_retries+'&up=&qd_v='+qd_v+'&tm='+tm+'&qdy='+qdy+'&qds='+qds+'&k_ft1='+k_ft1+'&k_ft4='+k_ft4+'&k_ft5='+k_ft5+'&bop='+urllib.parse.quote(bop)+'&ut='+ut
    vf = getVF(url)
    finalurl = baseurl + url + '&vf=' + vf

    return finalurl

def getM3U8(url, bid):
    response = requests.get(url)
    result = response.content.decode('utf-8')
    first = 'try{__jp3('
    end = ');}catch(e){};'
    resultJson = json.loads(result[len(first):-len(end)-1])
    for index in range(len(resultJson['data']['program']['video'])):
        if resultJson['data']['program']['video'][index]['bid'] == int(bid) and 'scrsz' in resultJson['data']['program']['video'][index]:
            m3u8 = resultJson['data']['program']['video'][index]['m3u8']
    return m3u8

def getVideoDetail(tvid):
    url = 'https://pcw-api.iqiyi.com/video/video/baseinfo/' + str(tvid)
    response = requests.get(url)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    name = resultJson['data']['shortTitle']
    duration = resultJson['data']['durationSec']
    return name, duration

def renewP():
    url = COS-URL
    response = requests.get(url)
    result = response.content.decode('utf-8')
    return result

def main_handler(event, context):
    videourl = event['path'][9:]
    #videourl = 'https://www.iqiyi.com/v_bls6g65uj4.html'
    info = getVideoInfo(videourl)
    tvid = info[0]
    vid = info[1]
    #bid = 600
    bidarr = [200, 300, 500, 600]
    urlarr = {'VideoName':'', 'Duration':'', '1080P':'', '720P':'', '540P':'', '360P':''}
    for index in range(4):
        bid = bidarr[index]
        downurl = getUrl(str(tvid), str(vid), str(bid))
        apiurl = COS-URL
        response = requests.get(apiurl)
        m3u8url = response.content.decode('utf-8')[1:-1]
        if index == 0:
            urlarr['360P'] = m3u8url
        elif index == 1:
            urlarr['540P'] = m3u8url
        elif index == 2:
            urlarr['720P'] = m3u8url
        elif index == 3:
            urlarr['1080P'] = m3u8url
    detail = getVideoDetail(tvid)
    urlarr['VideoName'] = detail[0]
    urlarr['Duration'] = detail[1]

    html = {'Encode':'Base64',
            'Key':'Null',
            'VideoUrl':'',
            'ParseResult':''
            }
    html_out = base64.b64encode(str(urlarr).encode("utf-8")).decode("utf-8")
    html['VideoUrl'] = videourl
    html['ParseResult'] = html_out
    return html
