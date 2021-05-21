# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/21 18:43
import numpy as np
import os
from shutil import copyfile
from my_utils.yzy_excel_xls import excel_xls
from my_utils.my_until import *
import pandas as pd

filepath = r'E:\yzy_projects\wl_risk_test\dataset_test\荆门石化特异度高低风险测试\低风险gt'
checkxls = r'E:\yzy_projects\wl_risk_test\dataset_test\荆门石化特异度高低风险测试\低风险gt/error.xlsx'
outpath = r'E:\yzy_projects\wl_risk_test\dataset_test\荆门石化特异度高低风险测试\低风险gt_error'
if not os.path.exists(outpath):
    os.makedirs(outpath)
files = fetch_all_imgs(filepath)
E=excel_xls()
check_files = E.read_excel_xls(checkxls)
check_files_name = [x.split('\\')[-1] for x in check_files]
n = 0
for f in files:
    img = cv2_imread(f)
    files_name = os.path.basename(f)
    if files_name in check_files_name:
        n += 1
        cv2_imwrite(os.path.join(outpath, files_name), img)
print('sssssss')

# path =r'E:\yzy_projects\wl_risk_test\dataset_test\武汉市中心特异度高低风险测试'
# E = excel_xls()
# files = fetch_all_imgs(path+'\低风险gt')
#
# df_data = {}
# df_data = pd.DataFrame(df_data)
# print(df_data)
#
# name_list=[]
# for img in files:
#     image = cv2_imread(img)
#     img_name = os.path.basename(img)[:-4]
#     out_path = img.replace('低风险gt', '低风险new')[:-4]+'.jpg'
#     if not os.path.exists(out_path.split('\\' + img_name)[0]):
#         os.makedirs(out_path.split('\\' + img_name)[0])
#     cv2_imwrite(out_path, image)
#     name_list.append(img_name)
# df_data["img_name"] = name_list
#
# xlsx_path = os.path.join(path, "名字.xlsx")
# writer = pd.ExcelWriter(xlsx_path)
# df_data.to_excel(writer)
# writer.save()