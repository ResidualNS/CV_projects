# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/11 14:06
import os
import glob
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


def remove_report(file_path, saves_path, file2_path=None, file3_path=None):
    '''
    病灶留图文件夹、26部位留图文件夹、 活检留图文件夹 合并
    '''
    file_list = os.listdir(file_path)
    for file in file_list:
        save_path = os.path.join(saves_path, file)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        all_image = fetch_all_imgs(os.path.join(file_path, file))
        for image in all_image:
            shutil.copy(image, save_path)

        if file2_path:
            all_image2 = fetch_all_imgs(os.path.join(file2_path, file))
            for image2 in all_image2:
                shutil.copy(image2, save_path)

        if file3_path:
            all_image3 = fetch_all_imgs(os.path.join(file3_path, file))
            for image3 in all_image3:
                shutil.copy(image3, save_path)
        print(file)


if __name__ == '__main__':
    # file_path = './荆门石化补充33'
    # remove_file(file_path)
    file_path = r'E:\泽华dataset\图文报告系统\三医院案例\三医院30例_新模型留图'
    file2_path = r'E:\泽华dataset\图文报告系统\三医院案例\原始案例image文件夹\biopsy_result'
    file3_path = r'E:\泽华dataset\图文报告系统\三医院案例\原始案例image文件夹\risk_result'
    saves_path = r'E:\泽华dataset\图文报告系统\三医院案例\三医院AI复评'
    remove_report(file_path, saves_path, file2_path = file2_path, file3_path = file3_path)