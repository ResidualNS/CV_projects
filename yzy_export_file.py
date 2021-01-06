# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/4 14:00
import numpy as np
import os
import re
from shutil import copyfile
from my_utils.yzy_excel_xls import excel_xls
from my_utils.my_until import *
'''
将文件夹1中与文件夹2同名的文件删除，保存为文件夹3，并去除文件名多余的符号，提取每个病人的名字输出xls。
'''
def export_file(filepath, checkpath, outpath):
    files_0 = os.listdir(filepath)
    for i in files_0:
        print(i)
        n = 0
        check_files = fetch_all_imgs(checkpath)
        check_files_name = [x.split('\\')[-1][:-4] for x in check_files]

        input_path_0 = os.path.join(filepath, i)
        out_path_0 = os.path.join(outpath, i)
        if not os.path.exists(out_path_0):
            os.makedirs(out_path_0)

        files_1 = os.listdir(input_path_0)
        for img in files_1:
            if img[:-4] in check_files_name:  # 去掉重名图像
                n += 1
                input_path_1 = os.path.join(input_path_0, img)
                image = cv2_imread(input_path_1)
                out_path_1 = os.path.join(out_path_0, img[:-4]+'.jpg')
                cv2_imwrite(out_path_1, image)

        if not os.listdir(out_path_0):
            os.rmdir(out_path_0)


def export_file_imgs(filepath, checkpath, outpath):
    '''
    两个文件夹里的图片相减
    '''
    files = fetch_all_imgs(filepath)
    check_files = fetch_all_imgs(checkpath)
    check_files_name = [x.split('\\')[-1][:-4] for x in check_files]
    n = 0
    for img in files:
        img_name = os.path.basename(img)
        if img_name[:-4] in check_files_name: #去掉重名图像
            n += 1
            out_ = outpath +'/'+ img.split('\\')[-1]
            copyfile(img, out_)
    print('{} 去除了 {} 张图片！'.format(img, n))

def remove_xls_img(filepath, checkpath):
    files = fetch_all_imgs(filepath)
    EX = excel_xls()
    check_list = EX.read_excel_xls(checkpath)
    check_list = [x.split('\\')[-1][:-4] for x in check_list]
    i = 0
    for img in files:
        img_name = os.path.basename(img)
        if img_name[:-4] in check_list:
            i += 1
            os.remove(img)
    print(i)

def id_create_folder(path, save_path):
    '''
    根据文件名创建病人文件夹
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    all_files = fetch_all_files(path)
    for img in all_files:
        img_name = os.path.basename(img)
        new_folder = img_name[:16]
        new_folder_path = os.path.join(save_path, new_folder)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        input_path = img
        out_path = os.path.join(save_path, new_folder, img_name)
        copyfile(input_path, out_path)
    print('finish：', save_path)


if __name__ == '__main__':
    # #1
    filepath = r'E:\徐铭dataset\内外部验证集-原图\宜昌一医'
    checkpath= r'E:\徐铭dataset\六家医院_终_基线信息\宜昌一医\01有病灶汇总\低风险'
    outpath = r'E:\徐铭dataset\六家医院_终_基线信息\宜昌一医\00非瘤变'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    export_file(filepath, checkpath, outpath)
    # #2
    # filepath = 'E:/徐铭dataset/YOLO特异度测试/无病灶2898'
    # checkpath= 'E:/徐铭dataset/YOLO特异度测试/预测有框'
    # outpath = 'E:/徐铭dataset/YOLO特异度测试/无病灶288'
    # export_file_imgs(filepath, checkpath, outpath)
    # xls_path = '内外部验证-病灶.xls'
    # sheet_name = '有病灶'
    # sheet_title = [["医院名称", "病灶类型", "病人ID"], ]
    # if not os.path.exists(xls_path):
    #     EX.write_excel_xls(xls _path, sheet_name, sheet_title)
    #3
    # filepath = r'E:\徐铭dataset\六家医院_终_基线信息\武汉市中心\预测有框_new'
    # checkpath= r'E:\徐铭dataset\六家医院_终_基线信息\武汉市中心\有病灶高风险-54.xlsx'
    # remove_xls_img(filepath, checkpath)
    #4
    # path = r'E:\徐铭dataset\六家医院_终_基线信息\人民医院\01有病灶汇总\805\低风险'
    # path_dir = os.listdir(path)
    # for _dir in path_dir:
    #     filepath = os.path.join(path, _dir)
    #     save_path = os.path.join(path+'_new', _dir)
    #     id_create_folder(filepath, save_path)

print("--------------finish----------------")