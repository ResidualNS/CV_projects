# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/4 14:00
import numpy as np
import os
from shutil import copyfile
from yzy_excel_xls import excel_xls
#from mbsh import logger

def export_file(filepath, checkpath, outpath):
    files_0 = os.listdir(filepath)
    for i in files_0:
        n = 0
        if not os.path.isdir(filepath + '/' + i):   #这里是绝对路径，该句判断目录是否是文件夹
            continue
        else:
            check_files = os.listdir(checkpath + '/' + i)
            check_files_name = [x[:-4] for x in check_files]

            input_path_0 = filepath + '/' + i
            out_path_0 = outpath + '/' + i
            if not os.path.exists(out_path_0):
                os.makedirs(out_path_0)

            files_1 = os.listdir(input_path_0)
            for j in files_1:
                if not os.path.isdir(input_path_0 + '/' + j):  # 这里是绝对路径，该句判断目录是否是文件夹
                    continue
                else:
                    input_path_1 = input_path_0 + '/' + j
                    out_path_1 = out_path_0 + '/' + j
                    if not os.path.exists(out_path_1):
                        os.makedirs(out_path_1)

                    file_2 = os.listdir(input_path_1)
                    for k in file_2:
                        if not os.path.isdir(input_path_1 + '/' + k):  # 这里是绝对路径，该句判断目录是否是文件夹
                            continue
                        else:
                            input_path_2 = input_path_1 + '/' + k
                            out_path_2 = out_path_1 + '/' + k

                            file_3 = os.listdir(input_path_2)
                            if len(file_3) == 0:
                                continue
                            else:
                                if not os.path.exists(out_path_2):
                                    os.makedirs(out_path_2)
                                value_ = [[input_path_2.split('/')[-3], input_path_2.split('/')[-2], input_path_2.split('/')[-1]], ]
                                EX.write_excel_xls_append(xls_path, value_)   #病人信息写入表格
                                for img in file_3:
                                    if img[:-4] in check_files_name: #去掉重名图像
                                        n += 1
                                        continue
                                    else:
                                        if img[-14:-8] == '_hrisk' or img[-13:-9] == '_hrisk':   #去掉后缀
                                            head, sep, tail = img.partition('_hrisk')
                                            input_path_3 = input_path_2 + '/' + img
                                            out_path_3 = out_path_2 + '/' + head + '.jpg'
                                            copyfile(input_path_3, out_path_3)
                                        else:
                                            input_path_3 = input_path_2 + '/' + img
                                            out_path_3 = out_path_2 + '/' + img
                                            copyfile(input_path_3, out_path_3)
                                if len(out_path_2) == 0:
                                    os.removedirs(out_path_2)  # 删掉空文件夹
        print('{} 去除了 {} 张图片！'.format(i,n))

if __name__ == '__main__':
    filepath = './内外部验证-病灶/原始有病灶'
    checkpath= './内外部验证-病灶/无病灶'
    outpath = './内外部验证-病灶/有病灶'

    EX = excel_xls()
    xls_path = '内外部验证-病灶.xls'
    sheet_name = '有病灶'
    sheet_title = [["医院名称", "病灶类型", "病人ID"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    patient_ID = export_file(filepath, checkpath, outpath)
    print("--------------finish----------------" )