# -*- coding:utf-8 -*-


import requests
import urllib3
from pyquery import PyQuery
from util import url_util
from urllib3.exceptions import InsecureRequestWarning


# 请求地址类型 http://www.hdsdjf.com/smp/yytlj08.aspx
def get_mp3_two(mp3_code_url):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    urllib3.disable_warnings(InsecureRequestWarning)
    html = requests.get(mp3_code_url, verify=False, timeout=(2, 5), headers=url_util.header)
    pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))

    if pq_html('a').length > 0:
        link_url = pq_html('a').attr('href')
        link_html = requests.get(link_url, verify=False, timeout=(2, 5), headers=url_util.header)
        pq_link_html = PyQuery(''.join([link_html.text.replace
                                        ('</body>', '').replace('</html>', ''), '</body></html>', ]))
        mp3_links = pq_link_html('.tab ul li')
        if mp3_links.length > 0:
            mp3_id = mp3_links.attr('data-l-id')
            link_url = link_url.replace('dt/bi', 'cm/pl')
            mp3_html_url = link_url + '&l_id' + mp3_id
            mp3_html = requests.get(mp3_html_url, verify=False, timeout=(2, 5), headers=url_util.header)
            pq_mp3_html = PyQuery(''.join([mp3_html.text.replace
                                           ('</body>', '').replace('</html>', ''), '</body></html>', ]))
            for mp3_url in pq_mp3_html('.playlist_song').items():
                mp3_data['mp3_list'].append({
                    'name': mp3_url.attr('data-t'),
                    'url': mp3_url.attr('data-u'),
                })
        else:
            for mp3_url in pq_link_html('.playlist_song').items():
                mp3_data['mp3_list'].append({
                    'name': mp3_url.attr('data-t'),
                    'url': mp3_url.attr('data-u'),
                })
            return mp3_data
    else:
        return mp3_data

    return mp3_data
