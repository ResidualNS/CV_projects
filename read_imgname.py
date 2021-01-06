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

    for input_ in input_list:
        id_list = fetch_all_imgs(input_)
        for id in id_list:
            print('正在识别病人：', id)
            basename = os.path.basename(id)
            base, name = os.path.splitext(basename)
            newname = base[:-2]+name
            #id_path = os.path.join(input_, id) # 获取图片路径列表
            value_ = [[newname], ]
            EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格

def patient_folder_name(xls_path, input_list):
    """
    获取目录下所有病人的文件夹名
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["patient_id"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    id_list = fetch_all_imgs(input_list)
    folder_name_list = []
    for id in id_list:
        print('正在识别病人：', id)
        #img_name=os.path.basename(id)
        id_path = os.path.join(input_list, id) # 获取图片路径列表
        folder_name = id_path.split('\\')[-2]
        if folder_name not in folder_name_list:
            value_ = [[folder_name], ]
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
        if img_name in check_list:
            print('正在识别病人：', img)
            n += 1
            shutil.copyfile(img, os.path.join(output, img_name))
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
    input_list = r'E:\泽华dataset\低风险四分类模型训练+测试用图\息肉+黏膜下病变训练集【无病理】\息肉训练集'
    xls_path = r'E:\泽华dataset\dataset\res_train\2-息肉_0.05.xls'
    output = r'E:\泽华dataset\低风险四分类模型训练+测试用图\息肉+黏膜下病变训练集【无病理】\息肉训练集_0.05'
    find_patient(xls_path, input_list, output)
print('-----------------')