# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/21 18:43
import numpy as np
import os
from shutil import copyfile
from yzy_excel_xls import excel_xls
from my_until import *

filepath = 'E:/yzy_projects/wl_risk_test/dataset_test/宜昌中心特异度高低风险测试/低风险gt'
checkxls = 'E:/yzy_projects/wl_risk_test/dataset_test/宜昌中心特异度高低风险测试/低风险gt/error.xlsx'
outpath = 'E:/yzy_projects/wl_risk_test/dataset_test/宜昌中心特异度高低风险测试/低风险error'
if not os.path.exists(outpath):
    os.makedirs(outpath)
files = fetch_all_imgs(filepath)
E=excel_xls()
check_files = E.read_excel_xls(checkxls)
n = 0
for f in files:
    img = cv2_imread(f)
    files_name = os.path.basename(f)[:-4]
    if files_name+'.jpg' in check_files or files_name+'.BMP' in check_files:
        n += 1
        cv2_imwrite(os.path.join(outpath,files_name+'.jpg'), img)
print('sssssss')
