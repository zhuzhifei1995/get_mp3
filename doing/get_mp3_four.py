# -*- coding:utf-8 -*-


# http://www.pingdianedu.com:8101/files/html/hearing/hearing5-2.html
import requests
from pyquery import PyQuery

from util import url_util


def get_mp3_four(mp3_code_url: str):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    html = requests.get(mp3_code_url, verify=False, timeout=(2, 5), headers=url_util.header)
    pq_html = PyQuery(''.join([html.text.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
    if pq_html('source').length > 0:
        mp3_data['mp3_list'].append({
            'name': pq_html('source').attr('src').split('/')[-1],
            'url': pq_html('source').attr('src'),
        })
    return mp3_data
