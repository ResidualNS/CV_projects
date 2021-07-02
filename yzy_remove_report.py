# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/11 14:06
import os
import glob
import xlrd
from shutil import copyfile
from my_utils.my_until import *
from my_utils.yzy_excel_xls import *
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

def find_patient(xls_path, path):
    """
    通过病人图片名找图片
    """
    datas = xlrd.open_workbook(xls_path)
    table = datas.sheets()[0]
    input_path = os.path.join(path, 'image_size_2_box')
    check_list = fetch_all_files(input_path)
    check_list = [x.split('\\')[-1][:-6] for x in check_list]
    n = 0
    for i in range(table.nrows):
        image_list = table.row_values(i)
        image_name = str(image_list[0])
        if image_name in check_list:
            print(image_name)
            n += 1
            tt = ''
            if image_list[2] == '训练集':
                tt = 'train'
            elif image_list[2] == '测试集':
                tt = 'test'

            if image_list[1] == '凹陷':
                save_path_0 = os.path.join(path, tt, '0')
                if not os.path.exists(save_path_0):
                    os.makedirs(save_path_0)
                shutil.copyfile(os.path.join(input_path, image_name + '_0.jpg'), os.path.join(save_path_0, image_name + '_0.jpg'))
            elif image_list[1] == '隆起':
                save_path_1 = os.path.join(path, tt, '1')
                if not os.path.exists(save_path_1):
                    os.makedirs(save_path_1)
                shutil.copyfile(os.path.join(input_path, image_name + '_0.jpg'), os.path.join(save_path_1, image_name + '_0.jpg'))
            elif image_list[1] == '浅表':
                save_path_2 = os.path.join(path, tt, '2')
                if not os.path.exists(save_path_2):
                    os.makedirs(save_path_2)
                shutil.copyfile(os.path.join(input_path, image_name + '_0.jpg'), os.path.join(save_path_2, image_name + '_0.jpg'))
    print(n)

if __name__ == '__main__':
    # file_path = './荆门石化补充33'
    # remove_file(file_path)
    input_list = r'E:\张丽辉dataset\巴黎分型\数据准备'
    xls_path = r'E:\张丽辉dataset\巴黎分型\数据准备\0624胃内高风险病灶巴黎分型评图整理.xlsx'
    find_patient(xls_path, input_list)
