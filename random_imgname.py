# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/1/30 9:39
import re
from shutil import copyfile
from my_utils.my_until import *
from my_utils.yzy_excel_xls import *
import random


def make_black_img(src_img):
    img = src_img.copy()
    src_h = img.shape[0]
    src_w = img.shape[1]
    max_size = max(src_w, src_h)
    black_img = np.zeros([max_size, max_size, 3], np.uint8)

    if src_w > src_h:
        y1_del = int((src_w - src_h) / 2)
        y2_del = y1_del + src_h
        black_img[y1_del:y2_del, 0:src_w] = src_img

    elif src_h > src_w:
        x1_del = int((src_h - src_w) / 2)
        x2_del = x1_del + src_w
        black_img[0:src_h, x1_del:x2_del] = src_img
    else:
        black_img = src_img
    return black_img

def random_imgname(path, save_path):
    '''
    图片尺寸归一化并重命名
    '''
    fold_list = os.listdir(path)
    for fold in fold_list:
        target_fold = os.path.join(save_path, fold)
        if not os.path.exists(target_fold):
            os.makedirs(target_fold)
        fold_path = os.path.join(path, fold)
        image_list = os.listdir(fold_path)
        j = 0
        for image in image_list:
            j += 1
            image_path = os.path.join(fold_path, image)
            image =cv2_imread(image_path)
            black_image = make_black_img(image)
            size = (480, 480)
            image_resize = cv2.resize(black_image, size)
            target_path = os.path.join(target_fold, str(j)+'.jpg')
            cv2_imwrite(target_path, image_resize)
        print(fold)


def random_folername(path, save_path, xlsx_input_path, xlsx_save_path):
    '''
    文件夹名打乱随机评图
    '''
    fold_list = os.listdir(path)
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["patient_id", "num"], ]
    if not os.path.exists(xlsx_save_path):
        EX.write_excel_xls(xlsx_save_path, sheet_name, sheet_title)

    check_list = EX.read_excel_xls(xlsx_input_path, 0, 1)
    check_list_2 = EX.read_excel_xls(xlsx_input_path, 1, 2)
    for check_2 in check_list_2:
        check_list.append(check_2)
    X = random.sample(range(1, 61), 60)
    for fold in fold_list:
        if fold in check_list:
            i = check_list.index(str(fold))
            value_ = [[check_list[i], X[i]], ]
            EX.write_excel_xls_append(xlsx_save_path, value_)
            source_fold = os.path.join(path, fold)
            target_fold = os.path.join(save_path, str(X[i]))
            if not os.path.exists(target_fold):
                os.makedirs(target_fold)
            image_list = fetch_all_imgs(source_fold)
            for image in image_list:
                shutil.copy(image, target_fold)


if __name__ == '__main__':
    # path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\三医院医师采图30例_crop'
    # save_path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\三医院医师采图30例_crop_resize'
    # random_imgname(path, save_path)

    xlsx_input_path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\30+30.xlsx'
    xlsx_save_path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\60.xls'
    path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\60_resize'
    save_path = r'E:\泽华dataset\图文报告系统\三医院案例\30+30随机打乱评图\60_random_result'
    random_folername(path, save_path, xlsx_input_path, xlsx_save_path)
print('-----------------------------------')
