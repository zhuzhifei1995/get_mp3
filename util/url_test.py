# -*- coding:utf-8 -*-


from doing.get_mp3_one import get_mp3_one
from doing.get_mp3_three import get_mp3_three
from doing.get_mp3_two import get_mp3_two
from util import url_util, txt_util


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
    urls = txt_util.read_txt_line("../test/zhizhuma.txt")
    for url in urls:
        get_html_mp3(url)
    # html_url = 'https://mp.zhizhuma.com/qr.html?crcode=110000000F00000000000007D5BG1832&sh=sh&vt_=1638424021201' \
    #            '&share_=167235561 '
    # get_html_mp3(html_url)

