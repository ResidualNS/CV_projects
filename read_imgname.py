# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/17 18:43
import cv2
import os
import time
import numpy as np
from my_utils.my_until import *
from my_utils.draw_toolbox import *
from my_utils.yzy_excel_xls import *

def read_img_name(xls_path, path):
    """
    获取目录下指定文件夹里的图片名称与风险类型
    """
    EX = excel_xls()
    sheet_name = 'yzy'
    sheet_title = [["img_id", "风险类型"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    input_list = os.listdir(path)
    for input_ in input_list:
        if input_ not in ['6.肠化', '7.其他', '8.有框']:
            class_index = 1
        else:
            class_index = 0
        input_path = os.path.join(path, input_)
        id_list = os.listdir(input_path)

        for id in id_list:
            print('正在识别病人：', id)
            id_path = os.path.join(input_path, id)
            images_list = fetch_all_imgs(id_path)  # 获取图片路径列表
            for image in images_list:
                value_ = [[image.split('\\')[-1], class_index], ]
                EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格

def patient_name(xls_path, input_list):
    """
    获取目录下所有病人的图片名
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["img_id"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    id_list = fetch_all_imgs(input_list)
    for id in id_list:
        print('正在识别病人：', id)
        basename = os.path.basename(id)
        value_ = [[basename], ]
        EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格

def patient_folder_name(xls_path, input_path):
    """
    获取目录下所有病人的文件夹名
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["patient_id", "image_num"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    id_list = os.listdir(input_path)
    folder_name_list = []
    for folder_name in id_list:
        print('正在识别病人：', folder_name)
        #img_name=os.path.basename(id)
        if folder_name not in folder_name_list:
            id_path = os.path.join(input_path, folder_name)
            image_list = os.listdir(id_path)
            num = len(image_list)
            value_ = [[folder_name, num], ]
            folder_name_list.append(folder_name)
            EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格

def find_patient(xls_path, input_list, output):
    """
    通过病人图片名找图片
    """
    EX = excel_xls()
    check_list = EX.read_excel_xls(xls_path)
    if not os.path.exists(output):
        os.makedirs(output)

    img_list = fetch_all_files(input_list)
    n = 0
    for img in img_list:
        img_name = os.path.basename(img)
        #img_name = img_name[len(img_name.split('_')[0])+1:]
        if img_name in check_list:
            print('正在识别病人：', img)
            n += 1
            shutil.move(img, os.path.join(output, img_name))
    print(n)

    # for input_0 in input_list:
    #     id_list0= os.listdir(input_0)
    #     for id_0 in id_list0:
    #         input_list1 = os.path.join(input_0, id_0)
    #         id_list1 = os.listdir(input_list1)
    #         for id_1 in id_list1:
    #             input_list2 = os.path.join(input_list1, id_1)
    #             id_list2 = os.listdir(input_list2)
    #             for id_2 in id_list2:
    #                 input_list3 = os.path.join(input_list2, id_2)
    #                 id_list3 = os.listdir(input_list3)
    #                 for id_3 in id_list3:
    #                     if id_3 in check_list:
    #                         print('正在识别病人：', id_3)
    #                         shutil.copytree(os.path.join(input_list3, id_3), os.path.join(output, id_3))


if __name__ == '__main__':
    # input_list = [r"G:\02高风险课题\report\4号台report（无更改版）", r"G:\02高风险课题\report\5号台report"]
    # xls_path = r'E:\徐铭dataset\前瞻性病人\71.xlsx'
    # output = r'E:\徐铭dataset\前瞻性病人\data_71_report'

    # input_path = r'E:\张丽辉dataset\表面特征分类\标准测试集\白苔_cut'
    # xls_path = input_path + r'.xls'
    # patient_name(xls_path, input_path)

    input_list = r'E:\朱益洁dataset\数据准备\原图\结构异常_'
    xls_path = r'E:\朱益洁dataset\数据准备\原图\训练集-异常.xlsx'
    output = r'E:\朱益洁dataset\数据准备\原图\结构异常_size'
    find_patient(xls_path, input_list, output)

    # input_path = r'E:\徐铭dataset\前瞻性new\东院重跑108'
    # xls_path = r'E:\徐铭dataset\前瞻性new\东院重跑108.xls'
    # patient_folder_name(xls_path, input_path)

print('-----------------')