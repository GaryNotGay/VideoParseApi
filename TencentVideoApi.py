# Deploied On TencentCloud Serverless Cloud Function
# -*- coding: utf8 -*-
import requests
import json
import base64

cookie = {'Your Cookies':'Json Format',
          'vqq_vusession':'Maybe This Is The Most Important Parameter'}

# Just Record
idJson = {'320001': 'Mp3',
          '320069': '1080P H265 3Mbps',
          '320093': '1080P H264',
          '320143': '1080P H265 Fake-4K',
          '320144': 'Null',
          '320159': '1080P H265 Dolby',
          '320156': 'Null',
          '320161': 'Dolby',
          '320160': '4K H265 Dolby',
          '320164': '1080P H265 Dolby',
          '320179': '1080P H265 HDR10 Apple',
          '320194': '1080P H265 HDR10 Android',
          '320199': '1080P H265 Dolby',
          '321001': '270P H264',
          '321002': '480P H264',
          '321003': '720P H264',
          '321004': '1080P H264',
          '321005': '1080P H264 Dolby',
          '322000': 'Null',
          '322001': '270P H265',
          '322002': '480P H265',
          '322003': '720P H265',
          '322004': '1080P H265',
          '322005': 'Null',
          '322006': 'Null',
          '322011': '270P H265',
          '322012': '480P H265',
          '322013': '720P H265',
          '322014': '1080P H265',
          '322016': '4K H265',
          '322069': 'Null',
          '326013': 'Dolby Mp3',
          }

imageArray = ['fhd', 'shd', 'hd', 'sd']
imageJson = {'fhd':'1080P',
             'shd':'720P',
             'hd':'480P',
             'sd':'360P',
             }
JsonOut = {'VideoUrl':'',
           'VideoName':'',
           '1080P':'',
           '720P':'',
           '480P':'',
           '360P':''
          }
JsonEncode = {'Encode':'Base64',
              'Key':'Null',
              'VideoUrl':'',
              'ParseResult':''
              }

def url2vid(mzc):
    vid_url = 'http://union.video.qq.com/fcgi-bin/data?tid=698&appid=10071005&otype=json&appkey=0d1a9ddd94de871b&idlist=' + mzc
    vid_header = 'QZOutputJson='
    vid_result = requests.get(url=vid_url)
    vid_result_json = json.loads(vid_result.content.decode('utf-8')[len(vid_header):-1])
    vid_json = json.loads(vid_result_json['results'][0]['fields']['all_ids'].encode('utf-8'))
    return vid_json[0]['V']

def main_handler(event, context):
    
    qqurl = event['path'][4:]
    title_str = 'mzc00200'
    title_index = qqurl.find(title_str)
    if qqurl[title_index + len(title_str) + 7] == '/':
        urlcase = 1
    elif qqurl[title_index + len(title_str) + 7] == '.':
        urlcase = 2

    if urlcase == 1:
        html_str = '.html'
        html_index = qqurl.find(html_str)
        vid = qqurl[title_index+len(title_str)+8 : html_index]
    elif urlcase == 2:
        html_str = '.html'
        html_index = qqurl.find(html_str)
        mzc = qqurl[title_index : html_index]
        vid = url2vid(mzc)

    for index in range(len(imageArray)):
            m3u8 = ''
            url = 'https://vv.video.qq.com/getinfo'
            baseurl_definition = imageArray[index]
            #print(video_id)
            #print(filename)
            url_params = {
                    'otype': 'json',
                    'vid': vid,
                    'platform': 10801,
                    'defn': baseurl_definition,
                    'defnpayver': 1,
                    'sdtfrom': 'v4138',
                    'fhdswitch': 1,
                    'show1080p': 1,
                    'newnettype': 1,
                    'dtype': 3,
                    'sphls': 2,
            }
            url_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
            url_result_header = 'QZOutputJson='
            url_result = requests.get(url=url, params=url_params, headers=url_headers, cookies = cookie)
            url_result_json = json.loads(url_result.content.decode('utf-8')[len(url_result_header):-1])
            VideoName = url_result_json['vl']['vi'][0]['ti']
            m3u8 = url_result_json['vl']['vi'][0]['ul']['ui'][3]['url']
            JsonOut[imageJson[baseurl_definition]] = m3u8

    JsonOut['VideoUrl'] = qqurl
    JsonOut['VideoName'] = VideoName
    print(JsonOut)
    JsonEncode['VideoUrl'] = qqurl
    outstr = base64.b64encode(str(JsonOut).encode('utf-8')).decode('utf-8')
    JsonEncode['ParseResult'] = outstr
    return JsonEncode
