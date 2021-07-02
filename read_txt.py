# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/5/11 17:13
from my_utils.my_until import *
'''
读取txt图片名，将图片按分类保存文件夹
'''

# path = r'E:\朱益洁dataset\数据准备\5.11小肠镜异常图细分类'
# image_path = os.path.join(path, 'images')
# txt_path = os.path.join(path, '血管性病变.txt')
# saves_path = txt_path[:-4]
# if not os.path.exists(saves_path):
#     os.makedirs(saves_path)
#
# image_list = fetch_all_imgs(path)
# txt_list = []
# for line in open(txt_path):
#     txt_list.append(line.strip())
#
# for image in image_list:
#     image_name = os.path.basename(image)
#     if image_name in txt_list:
#         save_path = os.path.join(saves_path, image_name)
#         shutil.copyfile(image, save_path)
#         print('正在copy', save_path)
# print('ssssss')

'''
将部位标签文件导入案例文件夹中
'''
case_path = r'E:\张丽辉dataset\图文报告2.0\测试案例24例\image'
part_path = r'E:\张丽辉dataset\图文报告2.0\测试案例24例\part_label'
case_list = os.listdir(case_path)
part_list = os.listdir(part_path)
for part in part_list:
    case_name = part[:-11]
    if case_name in case_list:
        shutil.copy(os.path.join(part_path, part), os.path.join(case_path, case_name))

print('..')