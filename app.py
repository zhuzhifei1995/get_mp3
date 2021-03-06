# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify, render_template

from doing.get_mp3_four import get_mp3_four
from doing.get_mp3_one import get_mp3_one
from doing.get_mp3_three import get_mp3_three
from doing.get_mp3_two import get_mp3_two
from util import url_util

app = Flask(__name__)


@app.route('/index.html', methods=['GET', 'POST'])
def get_mp3():
    mp3_data = {
        'contentCode': 0,
        'mp3_list': []
    }
    mp3_code_url = request.form.get('mp3_code_url')
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
        elif url_type == '4':
            mp3_data = get_mp3_four(mp3_code_url)
        else:
            mp3_data['contentCode'] = url_type
    else:
        url_type = '-1'
        mp3_data['contentCode'] = url_type
    print(mp3_data)
    return render_template('index.html', mp3_data=mp3_data, mp3_code_url=mp3_code_url)


# @app.route('/index.html', methods=['GET', 'POST'])
# def get_index():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
