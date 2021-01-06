# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/11 14:06
import os
import glob
from shutil import copyfile
from my_utils.my_until import *
'''
整理数据集：去除病人文件夹里的报告图片等
'''
def remove_file(file_path):
    all_files = fetch_all_files(file_path)
    i = 0
    for file in all_files:
        file_name = file.split('\\')[-1]
        if u'\u4e00' <= file_name <= u'\u9fff' or file_name.endswith(('doc', 'wps', 'bmp', 'txt')):
            os.remove(file)
            i += 1
            print(file)
    print('remove:', i)


if __name__ == '__main__':
    file_path = './荆门石化补充33'
    remove_file(file_path)