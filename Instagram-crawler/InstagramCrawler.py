# Author: Wenxin Wang. Please contact wenxin.wxw@gmail.com if you have any questions.
# For studying and learning only. Please do not use for commercial use.

# Feature: This python app crawls photos and videos from Instagram.
# Usage: 
# 1. "pip install pyquery" https://pypi.org/project/pyquery/
# 2. Use your own "cookies, user-agent, and download path" of the Instragram.com
# 3. "python InstagramCrawler.py Instagram_user_name"


import os
import re
import sys
import json
import time
import random
import requests
from hashlib import md5
from pyquery import PyQuery as pq

url_base = 'https://www.instagram.com/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'

# Check your own user-agent/cookie info in Chrome developer tool -> network -> check "header" -> "cookie" + "user-agent"
# Fresh websites to catch the header info
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'cookie': 'fbsr_124024574287414=FPNRk-HnUOeCv8T8WDOsDy1SSaIi59kwL3wZLo5tg14.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFHWHFjdl9zODVMNldhY0hyOUM4TEJ4bWdubUJZUjlmeHdoZ2J3ZkdnM1QxTGZYdGVyTlkwX1JZRXFHaU1tT1hTQzRFX3BNQzRBbG9xZVpCYWVsUHo3MGhFaEVBTVNlRnRiZjNsNXI5VlR4OWltU00waUV0OGYwRHRwb0lGQmIxTnFpSGlQUk5rZzdBd3YtMXVlQUFDN2d2M3dFVHhXcnk5ZGQ3QlZsZGcwbWE0Y2h5b3lpZm5JR0FzcHdGU2tnT0xnYnpqczZMSW1iZS1Uc1pjT2Y2eGN2d2ZNbjZIdTJmYnN3aXp0bFBKeFFlUEh3cTB5ajlKelNOTzhzV2VzZWJDcjdZYURCTmFJX0ZKZVg4OHFSdUg0QjRDbWZCZDlUaC1Dd2xzY0RYU3J0Y0J4REtPVUNvZF9XcHZRRnZrUW91bXU1T1I1YmtOeVBiNTc0dHNQS0JQUSIsImlzc3VlZF9hdCI6MTUzODE4NTU2MiwidXNlcl9pZCI6IjE3NDMxMTY3OTUifQ; mid=W67ZxAALAAGS-ihA6ZrkWlP_a31r; mcd=3; fbm_124024574287414=base_domain=.instagram.com; csrftoken=LYhimz0Lh5POonBtSbqXoGu4ewDLbgLG; shbid=4340; rur=FRC; ds_user_id=1089707060; sessionid=1089707060%3AvDs4y4cEOw0DsM%3A9; shbts=1538187375.365298; urlgen="{\"71.92.194.252\": 20115}:1g64oR:36HvlluAtqCBeCiDHXHgmo-JYYs"'
}


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('Ask for web source code error. Error code:', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('Ask for web json error. Error code:', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)


def get_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print('Ask for photos binary stream error. Error code:', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_urls(html):
    urls = []
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    print('user_id：' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
            print(cursor, flag)
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for info in infos:
            if info['node']['is_video']:
                video_url = info['node']['video_url']
                if video_url:
                    print(video_url)
                    urls.append(video_url)
            else:
                if info['node']['display_url']:
                    display_url = info['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
        print(cursor, flag)
        # time.sleep(4 + float(random.randint(1, 800))/200)    # if count > 2000, turn on
    return urls


def main(user):
    url = url_base + user + '/'
    html = get_html(url)
    urls = get_urls(html)
	
	# Use your own download path here to substitue "C:\Users\文心\git\instagram\"
    dirpath = r'C:\Users\文心\git\instagram\{0}'.format(user)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for i in range(len(urls)):
        try:
            content = get_content(urls[i])
			
			# Use your own download path here to substitue "C:\Users\文心\git\instagram\"
            file_path = r'C:\Users\文心\git\instagram\{0}\{1}.{2}'.format(user, md5(content).hexdigest(), urls[i][-3:])
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    print('Downloading number {0} photo... '.format(i) + urls[i], ' {0} photos left'.format(len(urls)-i-1))
                    f.write(content)
                    f.close()
            else:
                print('Downloaded {0} photos'.format(i))
        except Exception as e:
            print(e)
            print('Failed to download this picture/video')


if __name__ == '__main__':
    user_name = sys.argv[1]
    start = time.time()
    main(user_name)
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'Totally spent {hour} hours {minu} minutes {sec} seconds')