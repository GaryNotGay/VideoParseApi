# Deploied On TencentCloud Serverless Cloud Function
# -*- coding: utf8 -*-
import requests
import json
import base64

cookies = {'SESSDATA':'Your Cookies'}

def ep2bvid(bzurl, urlcase):
    global VideoName
    ep2id_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    ep2id_data = {}
    ep2id_cookies = cookies
    ep2id_response = requests.get(url = bzurl, data=ep2id_data, headers=ep2id_headers, cookies=ep2id_cookies)
    ep2id_result = ep2id_response.content.decode("utf-8")
    start_char = '__INITIAL_STATE__='
    end_char = '(function(){var s;(s=document.currentScript'
    json_start_index = ep2id_result.rfind(start_char)
    json_end_index = ep2id_result.rfind(end_char)
    ep2id_json = json.loads(ep2id_result[json_start_index+len(start_char) : json_end_index-1])
    #print(ep2id_json)
    if urlcase == 3:
        VideoName = ep2id_json['h1Title']
        epid = bzurl.find('ep') + 2
        for index in range(len(ep2id_json['epList'])):
            if str(ep2id_json['epList'][index]['id']) == str(bzurl[epid: epid+7]):
                return_bvid = ep2id_json['epList'][index]['bvid']
                break

        return return_bvid
    elif urlcase == 1:
        VideoName = ep2id_json['videoData']['title']
        return bzurl[31:43]
    elif urlcase == 2:
        VideoName = ep2id_json['videoData']['title']
        return bzurl[31:43]


def main_handler(event, context):
    global VideoName
    '''
    print("Received event: " + json.dumps(event, indent = 2)) 
    print("Received context: " + str(context))
    print("Hello world")
    return("Hello World")
    '''
    bzurl = event['path'][6:]

    if len(bzurl) > 43:
        partable = 1
    else:
        partable = 0

    if bzurl[31:33] == 'BV':
        urlcase = 2
        if partable == 1:
            if bzurl[43] == '-':
                urlcase = 1
                bzurl = bzurl[0:43] + '?' + bzurl[44:]
    elif bzurl[25:32] == 'bangumi':
        urlcase = 3

    if urlcase == 1 or urlcase == 2:
        #bvid = bzurl[31:43]
        bvid = ep2bvid(bzurl, urlcase)
    elif urlcase == 3:
        bvid = ep2bvid(bzurl, urlcase)
    getCid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bvid + '&jsonp=jsonp'
    getCid_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    getCid_data = {}
    getCid_cookies = cookies
    getCid_response = requests.get(url = getCid_url, data=getCid_data, headers=getCid_headers, cookies=getCid_cookies)
    getCid_result = getCid_response.content.decode("utf-8")
    getCid_json = json.loads(getCid_result)
    if urlcase == 1:
        if len(bzurl) > 47:
            partid = int(bzurl[46:47])
        else:
            partid = int(bzurl[46])
        cid = getCid_json['data'][partid-1]['cid']
        partname = getCid_json['data'][partid-1]['part']
    else:
        cid = getCid_json['data'][0]['cid']
    #print(getCid_json['data'][partid-1])

    '''
    getName_url = 'https://api.bilibili.com/x/web-interface/archive/desc?&bvid=' + bvid + '&jsonp=jsonp'
    getName_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    getName_data = {}
    getName_cookies = cookies
    getName_response = requests.get(url = getName_url, data=getName_data, headers=getName_headers, cookies=getName_cookies)
    getName_result = getName_response.content.decode("utf-8")
    getName_json = json.loads(getName_result)
    if urlcase == 1:
        VideoName = getName_json['data'] + ' ' + partname
    elif urlcase == 2:
        VideoName = getName_json['data']
    elif urlcase == 3:
        VideoName = getCid_json['data'][0]['part']
    '''
    if urlcase == 1:
        VideoName += ' '
        VideoName += partname


    getSource_url = 'http://api.bilibili.com/x/player/playurl?cid=' + str(cid) + '&bvid=' + str(bvid) + '&jsonp=jsonp'
    getSource_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    getSource_data = {}
    getSource_cookies = cookies
    getSource_response = requests.get(url = getSource_url, data=getSource_data, headers=getSource_headers, cookies=getSource_cookies)
    getSource_result = getSource_response.content.decode("utf-8")
    getSource_json = json.loads(getSource_result)
    imagejson = {"高清 1080P60" : "116",
                "高清 720P60" : "74",
                "高清 1080P+" : "112",
                "高清 1080P" : "80",
                "高清 720P" : "64",
                "清晰 480P" : "32",
                "流畅 360P" : "16"}
    imagenameArray = getSource_json['data']['accept_description']
    #print(imagenameArray)
    json_media = {'VideoUrl':'',
                'VideoName':'',
                'VideoLength':'',
                '高清 1080P60':'',
                '高清 720P60':'',
                '高清 1080P+':'',
                '高清 1080P':'',
                '高清 720P':'',
                '清晰 480P':'',
                '流畅 360P':'',}
    json_media['VideoUrl'] = bzurl

    for index in range(len(imagenameArray)):
        imagename = imagenameArray[index]
        imagenum = int(imagejson[imagename])

        getSourceAgain_url = 'http://api.bilibili.com/x/player/playurl?cid=' + str(cid) + '&bvid=' + str(bvid) + '&qn=' + str(imagenum) + '&jsonp=jsonp'
        getSourceAgain_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        getSourceAgain_data = {}
        getSourceAgain_cookies = cookies
        getSourceAgain_response = requests.get(url = getSourceAgain_url, data=getSourceAgain_data, headers=getSourceAgain_headers, cookies=getSourceAgain_cookies)
        getSourceAgain_result = getSourceAgain_response.content.decode("utf-8")
        getSourceAgain_json = json.loads(getSourceAgain_result)
        downurl = getSourceAgain_json['data']['durl'][0]['url']
        json_media[imagename] = downurl
        print(getSourceAgain_url)
    json_media['VideoName'] = VideoName
    json_media['VideoLength'] = str(int(int(getSourceAgain_json['data']['durl'][0]['length']) / 1000))
    json_outstr = base64.b64encode(str(json_media).encode('utf-8')).decode('utf-8')
    json_out = {'Warnning':'Please Replace ?p=X To -p=X',
                'Encode':'Base64',
                'Key':'Null',
                'VideoUrl':'',
                'ParseResult':''}
    json_out['VideoUrl'] = bzurl           
    json_out['ParseResult'] = json_outstr

    #return json_media
    return json_out
