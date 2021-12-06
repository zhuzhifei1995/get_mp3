# -*- coding:utf-8 -*-


from doing.get_mp3_one import get_mp3_one
from doing.get_mp3_three import get_mp3_three
from doing.get_mp3_two import get_mp3_two
from util import url_util


def get_html_mp3(mp3_code_url):
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    if mp3_code_url is not None:
        url_type = url_util.get_url_type(mp3_code_url)
        print('需要获取声音文件的链接为:' + mp3_code_url
              + '----------------------链接的类型为：' + str(url_type))
        if url_type == '1':
            mp3_data = get_mp3_one(mp3_code_url)
        elif url_type == '2':
            mp3_data = get_mp3_two(mp3_code_url)
        elif url_type == '3':
            mp3_data = get_mp3_three(mp3_code_url)
        else:
            mp3_data['contentCode'] = url_type
    else:
        url_type = '-1'
        mp3_data['contentCode'] = url_type
    print(mp3_data)


if __name__ == '__main__':
    '''
     html_url = 'https://mp.zhizhuma.com/book.htm?_appbiz=bookdetail&bookid=198969&srcchannel=5.12303.shop&id=198969&sign=462b6c' 
     html_url = 'https://mp.zhizhuma.com/book.htm?id=51239&sign=1b63e6'
     
     html_url = 'https://mp.zhizhuma.com/qr.html?crcode=120GDQOQB80'
     html_url = 'https://mp.zhizhuma.com/qr.html?crcode=110000000F00000001000007IZCD1B79'
     html_url = 'https://mp.zhizhuma.com/share/audio.htm?rid=35304649&sign=404363&bid=198969&cid=27514970'
     
     html_url = 'https://mp.zhizhuma.com/q?c=120GM6JC98D&wxParamQr=1&sh=sh&vt_=1636632141914'
    '''

    html_url = 'https://mp.zhizhuma.com/book.htm?id=202053&sign=f6efa5#27908816'
    get_html_mp3(html_url)

