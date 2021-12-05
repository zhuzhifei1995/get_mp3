# -*- coding:utf-8 -*-


import requests
import urllib3
from pyquery import PyQuery

from util import url_util
from urllib3.exceptions import InsecureRequestWarning


# 请求地址类型
# https://mp.zhizhuma.com/book.htm?id=51239&sign=1b63e6
# https://mp.zhizhuma.com/book.htm?_appbiz=bookdetail&bookid=198969&srcchannel=5.12303.shop&id=198969&sign=462b6c
def get_mp3_three(mp3_code_url):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    urllib3.disable_warnings(InsecureRequestWarning)
    html = requests.get(mp3_code_url, verify=False, timeout=(2, 5), headers=url_util.header)
    pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
    mp3_html_links = pq_html('.body-content-wrapper .section-wrapper').items()
    for mp3_html_link in mp3_html_links:
        mp3_url = 'https://mp.zhizhuma.com'+mp3_html_link.attr('val')
        html = requests.get(mp3_url, verify=False, timeout=(2, 5), headers=url_util.header)
        pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
        if pq_html('#audio_media').length > 0:
            mp3_data['mp3_list'].append({
                'name': pq_html('.audio-title').text(),
                'url': pq_html('#audio_media').attr('src'),
            })
    return mp3_data
