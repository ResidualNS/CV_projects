# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/4 14:00
import numpy as np
import os
from shutil import copyfile
from yzy_excel_xls import excel_xls
from my_until import *
'''
将文件夹1中与文件夹2同名的文件删除，保存为文件夹3，并去除文件名多余的符号，提取每个病人的名字输出xls。
'''
# def export_file(filepath, checkpath, outpath):
#     files_0 = os.listdir(filepath)
#     for i in files_0:
#         n = 0
#         if not os.path.isdir(filepath + '/' + i):   #这里是绝对路径，该句判断目录是否是文件夹
#             continue
#         else:
#             all_dirs, check_files = fetch_all_imgs(checkpath + '/' + i)
#             check_files_name = [x.split('\\')[-1][:-4] for x in check_files]
#
#             input_path_0 = filepath + '/' + i
#             out_path_0 = outpath + '/' + i
#             if not os.path.exists(out_path_0):
#                 os.makedirs(out_path_0)
#
#             files_1 = os.listdir(input_path_0)
#             for j in files_1:
#                 if not os.path.isdir(input_path_0 + '/' + j):  # 这里是绝对路径，该句判断目录是否是文件夹
#                     continue
#                 else:
#                     input_path_1 = input_path_0 + '/' + j
#                     out_path_1 = out_path_0 + '/' + j
#                     if not os.path.exists(out_path_1):
#                         os.makedirs(out_path_1)
#
#                     file_2 = os.listdir(input_path_1)
#                     # for k in file_2:
#                         # if not os.path.isdir(input_path_1 + '/' + k):  # 这里是绝对路径，该句判断目录是否是文件夹
#                         #     continue
#                         # else:
#                         #     input_path_2 = input_path_1 + '/' + k
#                         #     out_path_2 = out_path_1 + '/' + k
#                         #
#                         #     file_3 = os.listdir(input_path_2)
#                     if len(file_2) == 0:
#                         continue
#                     else:
#                         #value_ = [[input_path_2.split('/')[-3], input_path_2.split('/')[-2], input_path_2.split('/')[-1]], ]
#                         #EX.write_excel_xls_append(xls_path, value_)   #病人信息写入表格
#                         for img in file_2:
#                             if img[:-4] in check_files_name: #去掉重名图像
#                                 n += 1
#                                 continue
#                             else:
#                                 # if img[-14:-8] == '_hrisk' or img[-13:-9] == '_hrisk':   #去掉后缀
#                                 #     head, sep, tail = img.partition('_hrisk')
#                                 #     input_path_3 = input_path_2 + '/' + img
#                                 #     out_path_3 = out_path_2 + '/' + head + '.jpg'
#                                 #     copyfile(input_path_3, out_path_3)
#                                 # else:
#                                 input_path_2 = input_path_1 + '/' + img
#                                 out_path_2 = out_path_1 + '/' + img
#                                 copyfile(input_path_2, out_path_2)
#                         if len(out_path_1) == 0:
#                             os.removedirs(out_path_1)  # 删掉空文件夹
#         print('{} 去除了 {} 张图片！'.format(i,n))

def export_file_imgs(filepath, checkpath, outpath):
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


if __name__ == '__main__':
    filepath = 'E:/徐铭dataset/YOLO特异度测试/无病灶2898'
    checkpath= 'E:/徐铭dataset/YOLO特异度测试/预测有框'
    outpath = 'E:/徐铭dataset/YOLO特异度测试/无病灶288'

    # EX = excel_xls()
    # xls_path = '内外部验证-病灶.xls'
    # sheet_name = '有病灶'
    # sheet_title = [["医院名称", "病灶类型", "病人ID"], ]
    # if not os.path.exists(xls_path):
    #     EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    export_file_imgs(filepath, checkpath, outpath)
print("--------------finish----------------")