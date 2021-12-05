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
        if pq_html('div.other-item').length > 0:
            mp3_url = 'https://mp.zhizhuma.com' + pq_html('.section-wrapper').attr('val')
            mp3_url_html = open_chrome_get_html(mp3_url)
            pq_mp3_url_html = PyQuery(''.join([mp3_url_html.replace('</body>', '')
                                              .replace('</html>', ''), '</body></html>', ]))
            print(pq_mp3_url_html)
            book_id = pq_mp3_url_html('#launch_book_id').text()
            book_code_id = pq_mp3_url_html('#launch_cr_id').text()
            book_items = pq_mp3_url_html('.other-item')
            for book_item in book_items.items():
                mp3_code_get_url = 'https://mp.zhizhuma.com/share/audio.htm?rid=' + book_item.attr('rs-id') \
                                   + '&sign=' + book_item.attr('sign') + '&bid=' + book_id + '&cid=' + book_code_id
                print(mp3_code_get_url)
                code_html = requests.get(mp3_code_get_url, verify=False, timeout=(2, 5), headers=url_util.header)
                pq_code_html = PyQuery(''.join([code_html.text.replace('</body>', '')
                                               .replace('</html>', ''), '</body></html>', ]))
                if pq_code_html('#audio_media').length > 0:
                    mp3_data['mp3_list'].append({
                        'name': pq_code_html('title').text(),
                        'url': pq_code_html('#audio_media').attr('src'),
                    })
    return mp3_data


if __name__ == '__main__':
    print(get_mp3_one('https://mp.zhizhuma.com/qr.html?crcode=120GDQOQB80'))
