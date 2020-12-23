# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/10 9:15
import re
from shutil import copyfile
from my_until import *
from yzy_excel_xls import *

def id_create_folder(path):
    '''
    根据文件名中的病人名字（中文）创建病人文件夹并归纳
    '''
    #path = './武汉市中心 张姮/2019'
    save_path = path.replace('武汉市中心 张姮', '武汉市中心 张姮_整理')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    all_files = fetch_all_files(path)
    for img in all_files:
        img_name = img.split('\\')[-1]
        new_name = re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\_\\\]", "", img_name)
        img_folder = os.path.join(save_path, new_name)
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        if img[-6:-5] == '_':
            print('run：', new_name)
            continue
        else:
            input_path = img
            out_path = save_path + '/' + new_name + '/' + img_name
            copyfile(input_path, out_path)
    print('finish：', save_path)

def check_create_folder(path, xls_path):
    save_path = path.replace('武大人民_终', '武大人民_终2.0' )
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    E = excel_xls()
    check_list = E.read_excel_xls(xls_path)
    all_files = fetch_all_imgs(path)
    n=0
    for img in all_files:
        img_name = os.path.basename(img)
        if img_name in check_list:
            image =cv2_imread(img)
            img_folder = img.split('\\'+img_name)[0].replace('武大人民_终', '武大人民_终2.0')
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            cv2_imwrite(os.path.join(img_folder, img_name), image)

if __name__ == '__main__':
    path = 'E:/徐铭dataset/武大人民_终/灵敏度测试/低风险gt'
    xls_path = 'E:/徐铭dataset/武大人民_终/1.xlsx'
    check_create_folder(path, xls_path)
print('-----------------------------------')

