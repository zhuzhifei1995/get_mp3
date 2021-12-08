# -*- coding:utf-8 -*-


import requests
import urllib3
from pyquery import PyQuery

from util import url_util
from urllib3.exceptions import InsecureRequestWarning


# 请求地址类型
# https://mp.zhizhuma.com/book.htm?id=51239&sign=1b63e6
# https://mp.zhizhuma.com/book.htm?_appbiz=bookdetail&bookid=198969&srcchannel=5.12303.shop&id=198969&sign=462b6c
def get_mp3_three(mp3_code_url: str):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    urllib3.disable_warnings(InsecureRequestWarning)
    html = requests.get(mp3_code_url, verify=False, timeout=(2, 5), headers=url_util.header)
    pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
    mp3_html_links = pq_html('.body-content-wrapper .section-wrapper').items()
    for mp3_html_link in mp3_html_links:
        mp3_url = 'https://mp.zhizhuma.com' + mp3_html_link.attr('val')
        html = requests.get(mp3_url, verify=False, timeout=(2, 5), headers=url_util.header)
        pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
        if pq_html('#audio_media').length > 0:
            mp3_data['mp3_list'].append({
                'name': pq_html('.audio-title').text(),
                'url': pq_html('#audio_media').attr('src'),
            })
        else:
            chrome_get_html = url_util.open_chrome_get_html(mp3_url)
            pq_chrome_get_html = PyQuery(''.join([chrome_get_html.replace('</body>', '')
                                                 .replace('</html>', ''), '</body></html>', ]))
            html_mp3s = pq_chrome_get_html('.other-item')
            # print(html_mp3s)
            book_id = pq_chrome_get_html('#launch_book_id').text()
            book_code_id = pq_chrome_get_html('#launch_cr_id').text()
            for html_mp3 in html_mp3s.items():
                try:
                    mp3_new_url = 'https://mp.zhizhuma.com/share/audio.htm?rid=' + html_mp3.attr('rs-id') \
                                  + '&sign=' + html_mp3.attr('sign') + '&bid=' + book_id + '&cid=' + book_code_id
                except TypeError:
                    mp3_new_url = 'https://mp.zhizhuma.com/share/audio.htm'
                html_new_mp3 = requests.get(mp3_new_url, verify=False, timeout=(2, 5), headers=url_util.header)
                pq_new_html = PyQuery(''.join([html_new_mp3.text.replace('</body>', '')
                                              .replace('</html>', ''), '</body></html>', ]))
                if pq_new_html('#audio_media').length > 0:
                    mp3_data['mp3_list'].append({
                        'name': pq_new_html('title').text(),
                        'url': pq_new_html('#audio_media').attr('src'),
                    })
    return mp3_data
