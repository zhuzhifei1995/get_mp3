# -*- coding:utf-8 -*-


# 读取文件的每一行
def read_txt_line(file_path):
    lines = []
    txt_file = open(file_path)
    line = txt_file.readline()
    while line:
        lines.append(line.strip())
        line = txt_file.readline()
    txt_file.close()
    return lines
