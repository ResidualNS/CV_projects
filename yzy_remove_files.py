# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/11 14:06
from my_utils.my_util import *
from my_utils.yzy_excel_xls import *
import glob

def remove_xls_img(filepath, checkpath, outpath):
    '''
    1.读取xls中图片名移动图片
    '''
    files = fetch_all_imgs(filepath)
    EX = excel_xls()
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    check_list = EX.read_excel_xls(checkpath)
    check_list = [x.split('\\')[-1][:-4] for x in check_list]
    i = 0
    for img in files:
        img_name = os.path.basename(img)[:-4]
        if img_name in check_list:
            i += 1
            print('正在识别病人：', img)
            shutil.move(img, os.path.join(outpath, os.path.basename(img)))

    print(i)

def remove_xls_fold(filepath, checkpath, outpath):
    '''
    2.读取xls中案例名移动案例
    '''
    EX = excel_xls()
    check_list = EX.read_excel_xls(checkpath, 0, 1)
    fold_list__ = os.listdir(filepath)
    for fold__ in fold_list__:
        filepath__ = os.path.join(filepath, fold__)
        fold_list = os.listdir(filepath__)
        i = 0
        for fold_ in fold_list:
            if fold_.split('_')[-1] in check_list:
                print(fold_)
                source_path = os.path.join(filepath__, fold_)
                target_path = os.path.join(outpath, fold_)
                # if not os.path.exists(target_path):
                #     os.makedirs(target_path)
                i += 1
                shutil.move(source_path, target_path)
        print(i)

def remove_xls_video(filepath, checkpath, outpath):
    '''
    3.读取xls中视频名移动视频
    '''
    files = glob.glob(filepath + '/*.mp4')
    EX = excel_xls()
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    check_list = EX.read_excel_xls(checkpath)
    i = 0
    for img in files:
        img_name = os.path.basename(img)[:16]
        if img_name in check_list:
            i += 1
            print('正在识别病人：', img)
            shutil.move(img, os.path.join(outpath, os.path.basename(img)))

    print(i)

# def remove_xls_fold_xm(filepath, checkpath, savepath):
#     '''
#     4.徐铭案例移动
#     '''
#     EX = excel_xls()
#     check_list = EX.read_excel_xls(checkpath, 0, 1)
#     fold_list = os.listdir(filepath)
#
#     i = 0
#     for fold in fold_list[:]:
#         path1 = os.path.join(filepath, fold)
#         fold1_list = os.listdir(path1)
#         for fold1 in fold1_list:
#             path2 = os.path.join(path1, fold1)
#             fold2_list = os.listdir(path2)
#             for fold2 in fold2_list:
#                 path3 = os.path.join(path2, fold2)
#                 fold3_list = os.listdir(path3)
#                 for fold_ in fold3_list:
#                     if fold_ in check_list:
#                         source_path = os.path.join(path3, fold_)
#                         target_path = os.path.join(savepath, fold_)
#                         if not os.path.exists(target_path):
#                             i += 1
#                             print("正在移动第%d个案例：%s" % (i, fold_))
#                             shutil.move(source_path, target_path)

def remove_csv_img(img_path, csv_path):
    '''
    5.读取csv的图片名以及标签，按标签命名文件夹移动图片
    '''
    import pandas as pd
    data = pd.read_csv(csv_path)
    label_list = data.values.tolist()
    for image_name, label in label_list:
        image_path = os.path.join(img_path, image_name)
        save_path = os.path.join(img_path, str(label))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        out_path = os.path.join(save_path, image_name)
        shutil.move(image_path, out_path)


def remove_txt_img(img_path, txt_path):
    '''
    6.读取txt图片名，将图片按分类保存文件夹
    '''
    saves_path = txt_path[:-4]
    if not os.path.exists(saves_path):
        os.makedirs(saves_path)

    image_list = fetch_all_imgs(img_path)
    txt_list = []
    for line in open(txt_path):
        txt_list.append(line.strip())

    for image in image_list:
        image_name = os.path.basename(image)
        if image_name in txt_list:
            save_path = os.path.join(saves_path, image_name)
            shutil.move(image, save_path)
            print('正在move', save_path)
    print('ssssss')

def case_create_folder(input_dirs, folder_name='imgs'):
    '''
    7.每个案例中的图片添加一层文件夹 'imgs'
    '''
    for input_dir in input_dirs:
        cases = os.listdir(input_dir)
        for case in cases[:]:
            print(case)
            case_path = os.path.join(input_dir, case)

            files_list = fetch_all_files(case_path)
            imgs_path = os.path.join(case_path, folder_name)
            if not os.path.exists(imgs_path):
                os.makedirs(imgs_path)
                for file in files_list:
                    shutil.move(file, imgs_path)
                    print("finished one fold!")
        print("finished all cases!")

def id_create_folder(path, save_path):
    '''
    8.根据自身文件名创建病人文件夹
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    all_files = fetch_all_files(path)
    for img in all_files:
        img_name = os.path.basename(img)
        new_folder = img_name[:16]
        new_folder_path = os.path.join(save_path, new_folder)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        input_path = img
        out_path = os.path.join(save_path, new_folder, img_name)
        shutil.move(input_path, out_path)
    print('finish：', save_path)


if __name__ == '__main__':
    # # 1、2、3、4
    # filepath = r'\\192.168.0.60\public\测试视频\图文视频测试\139'
    # checkpath= r'\\192.168.0.60\public\测试视频\图文视频测试\\43.xls'
    # outpath = r'\\192.168.0.60\public\测试视频\图文视频测试\43'
    # remove_xls_img(filepath, checkpath, outpath)

    # 5
    # path = r'E:\yzy_projects\znyx-others\HL_cls\image'
    # csv_path = r'E:\yzy_projects\znyx-others\HL_cls\train_label.csv'
    # get_label(path, csv_path)

    # # 6
    # img_path = r'E:\朱益洁dataset\数据准备\5.11小肠镜异常图细分类\images'
    # txt_path = r'E:\朱益洁dataset\数据准备\5.11小肠镜异常图细分类\血管性病变.txt'
    # remove_txt_img(img_path, txt_path)

    # 7
    input_dirs = [r"G:\辅助阅片2\辅助阅片image_ori"]
    case_create_folder(input_dirs, folder_name = 'imgs')