# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/10 9:15
import re
from shutil import copyfile
from my_until import *

path = './荆门石化/20219-12（112例）'
save_path = path.replace('荆门石化', '荆门石化整理')
if not os.path.exists(save_path):
    os.mkdir(save_path)
imgs_list = os.listdir(path)
for img in imgs_list:
    img_name = re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\_]", "", img)
    img_folder = os.path.join(save_path, img_name)
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    if img[-6:-5] == '_':
        print('run：', img_name)
        continue
    else:
        input_path = path + '/' + img
        out_path = save_path + '/' + img_name + '/' + img
        copyfile(input_path, out_path)
print('finish：', save_path)
print('-----------------------------------')