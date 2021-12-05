# -*- coding:utf-8 -*-


import requests
import urllib3
from pyquery import PyQuery

from util import url_util
from urllib3.exceptions import InsecureRequestWarning

# 请求地址类型
# https://mp.zhizhuma.com/qr.html?crcode=110000000F00000001000007IZCD1B79
# https://mp.zhizhuma.com/qr.html?crcode=120GDQOQB80
# https://mp.zhizhuma.com/share/audio.htm?rid=35304649&sign=404363&bid=198969&cid=27514970
from util.url_util import open_chrome_get_html


def get_mp3_one(mp3_code_url: str):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    urllib3.disable_warnings(InsecureRequestWarning)
    html = requests.get(mp3_code_url, verify=False, timeout=(2, 5), headers=url_util.header)
    pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
    if pq_html('#audio_media').length > 0:
        mp3_data['mp3_list'].append({
            'name': pq_html('title').text(),
            'url': pq_html('#audio_media').attr('src'),
        })
    else:

    return mp3_data


if __name__ == '__main__':
    print(get_mp3_one('https://mp.zhizhuma.com/qr.html?crcode=120GDQOQB80'))
