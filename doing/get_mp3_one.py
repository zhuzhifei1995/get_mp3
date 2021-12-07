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
        new_html = url_util.open_chrome_get_html(mp3_code_url)
        pq_new_html = PyQuery(''.join([new_html.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
        html_mp3s = pq_new_html('.other-item')
        if html_mp3s.length > 0:
            book_id = pq_new_html('#launch_book_id').text()
            book_code_id = pq_new_html('#launch_cr_id').text()
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
        else:
            for qr_html in pq_new_html('.section-wrapper').items():
                mp3_url = 'https://mp.zhizhuma.com' + qr_html.attr('val')
                mp3_url_html = requests.get(mp3_url, verify=False, timeout=(2, 5), headers=url_util.header)
                pq_mp3_url_html = PyQuery(
                    ''.join([mp3_url_html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
                if pq_mp3_url_html('#audio_media').length > 0:
                    mp3_data['mp3_list'].append({
                        'name': pq_mp3_url_html('title').text(),
                        'url': pq_mp3_url_html('#audio_media').attr('src'),
                    })

    return mp3_data
