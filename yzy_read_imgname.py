# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/2/17 18:43
from my_utils.my_util import *
from my_utils.yzy_excel_xls import *
from tqdm import tqdm
import math
from moviepy.editor import *
import time
import re

def read_imgname_xls(xls_path, input_list):
    """
    1.获取目录下所有图片名保存表格
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["img_id"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    id_list = fetch_all_imgs(input_list)
    for id in id_list:
        print('正在识别病人：', id)
        basename = os.path.basename(id)
        value_ = [[basename], ]
        EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格


def modify_case_imgname(input_path):
    """
    2.修改案例图片名
    """
    case_dir = os.listdir(input_path)
    for case in case_dir:
        all_files = fetch_all_imgs(os.path.join(input_path, case))
        for img in all_files:
            save_path, img_name = os.path.split(img)
            new_name = img_name.split(' ')[0]+'_bbox_.jpg'
            os.rename(img_name, new_name)

def modify_videoname(xls_path, input_path):
    """
    3.修改视频名称
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["case_name", "new_name"], ]
    if not os.path.exists(xls_path):
        EX.write_excel_xls(xls_path, sheet_name, sheet_title)

    id_list = os.listdir(input_path)
    id_list.sort(key = lambda x:int(x))
    #id_list.sort(key = lambda x:(int(re.sub('\.','', x).split('_')[0]), int(x.split('_')[1])))
    folder_name_list = []
    for i, folder_name in enumerate(id_list):
        print('正在识别病人：', folder_name)
        #img_list = os.listdir(os.path.join(input_path, folder_name))
        #img_name = img_list[0]
        id_path = os.path.join(input_path, folder_name)
        new_name = str(i).zfill(3) + '.mp4'
        new_path = os.path.join(input_path, new_name)
        os.rename(id_path, new_path)

        value_ = [[folder_name, new_name], ]
        folder_name_list.append(folder_name)
        EX.write_excel_xls_append(xls_path, value_)  # 病人信息写入表格

def xls_split_fragment(xls_path, input_path):
    """
    4.根据xls时间节点 在image中截出片断
    """
    EX = excel_xls()
    start_time = EX.read_excel_xls(xls_path, 0, 1)
    stop_time = EX.read_excel_xls(xls_path, 1, 2)
    id_list = os.listdir(input_path)
    n = 1
    for id in tqdm(id_list):
        img_path = os.path.join(input_path, id)
        imgs = fetch_all_imgs(img_path)
        save_mode = False
        for img in imgs:
            img_name = os.path.basename(img)
            if img_name[:-4] in start_time:
                print(img_name)
                save_mode = True
            if img_name[:-4] in stop_time:
                print(img_name)
                save_mode = False
                n += 1
            if save_mode:
                out_path = os.path.join(r'F:\张丽辉案例\image', str(n).zfill(3))
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                shutil.copyfile(img, os.path.join(out_path, img_name))

def time_trans(xls_path, out_xls):
    """
    5.时间转换
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["case_name", "start", "stop"], ]
    if not os.path.exists(out_xls):
        EX.write_excel_xls(out_xls, sheet_name, sheet_title)

    start_time = EX.read_excel_xls(xls_path, 0, 1)
    stop_time = EX.read_excel_xls(xls_path, 1, 2)
    for i, j in zip(start_time[1:], stop_time[1:]):
        case_name = i[:32]
        i_ = math.floor(int(i[33:]) / 25) - 1
        j_ = math.ceil(int(j[33:]) / 25)

        value_ = [[case_name, i_, j_], ]
        EX.write_excel_xls_append(out_xls, value_)

def Video_Clip(xls_path, video_path, out_path):
    """
    6.根据时间裁出视频片段
    """
    EX = excel_xls()
    case_name = EX.read_excel_xls(xls_path, 0, 1)
    start_time = EX.read_excel_xls(xls_path, 1, 2)
    stop_time = EX.read_excel_xls(xls_path, 2, 3)
    num = 86
    for i, j, k in zip(case_name[num:], start_time[num:], stop_time[num:]):
        video_ = os.path.join(video_path, i + '.mp4')
        j = math.floor(int(j))
        k = math.ceil(int(k))
        clips = VideoFileClip(video_).subclip(j, k)

        video = CompositeVideoClip([clips])
        out_ = os.path.join(out_path, i + '_' + str(j) + '_' + str(k) + '.mp4')
        if os.path.exists(out_):
            print('已存在:', out_)
            return
        video.write_videofile(out_)
        clips.close()
        video.close()
        time.sleep(1)

def check_xls(xls_path, gt_path, out_xls):
    """
    7.统计每张留图的label
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["image_name", "部位", "病种"], ]
    if not os.path.exists(out_xls):
        EX.write_excel_xls(out_xls, sheet_name, sheet_title)

    img_list = EX.read_excel_xls(xls_path, 1, 2)
    start_img_list = EX.read_excel_xls(gt_path, 2, 3)
    stop_img_list = EX.read_excel_xls(gt_path, 3, 4)
    gt_part_list = EX.read_excel_xls(gt_path, 6, 7)
    gt_type_list = EX.read_excel_xls(gt_path, 7, 8)
    for img in img_list[1:]:
        case_name = img[:32]
        time_name = img[33:-4]
        for i, j, p, t in zip(start_img_list, stop_img_list, gt_part_list, gt_type_list):
            case_name_2 = i[:32]
            start_time = i[33:]
            stop_time = j[33:]
            if case_name == case_name_2:
                if time_name >= start_time and time_name<= stop_time:
                    print(img, p, t)
                    value_ = [[img, p, t], ]
                    EX.write_excel_xls_append(out_xls, value_)

def check_score(xls_path, out_xls):
    """
    8.核对部位和病种正确数
    """
    EX = excel_xls()
    sheet_name = 'sheet1'
    sheet_title = [["image_name", "部位正确", "病种正确"], ]
    if not os.path.exists(out_xls):
        EX.write_excel_xls(out_xls, sheet_name, sheet_title)

    case_list = EX.read_excel_xls(xls_path, 0, 1)
    img_list = EX.read_excel_xls(xls_path, 1, 2)

    pre_part_list = EX.read_excel_xls(xls_path, 2, 3)
    pre_type_list = EX.read_excel_xls(xls_path, 3, 4)

    gt_part_list = EX.read_excel_xls(xls_path, 5, 6)
    gt_type_list = EX.read_excel_xls(xls_path, 6, 7)
    p, t = 0, 0
    for case, img, pre_part, pre_type, gt_part, gt_type in zip(case_list, img_list, pre_part_list, pre_type_list, gt_part_list, gt_type_list):
        if gt_part in pre_part:
            p = 1

        if pre_type in gt_type:
            t = 1

        value_ = [[img, p, t], ]
        EX.write_excel_xls_append(out_xls, value_)
        p, t = 0, 0

if __name__ == '__main__':
    # 1
    input_path = r'D:\0-杜泓柳\多病灶测试集150_原图\灵敏度测试\低风险gt\息肉150'
    xls_path = input_path + r'.xls'
    read_imgname_xls(xls_path, input_path)

    # 3
    # xls_path = r'F:\张丽辉案例\片段整理-1.xlsx'
    # video_path = r'D:\0-张丽辉视频_图片\139'
    # xls_split_fragment(xls_path, video_path)

    # xls_path = r'F:\张丽辉案例\片段整理-1.xlsx'
    # out_xls = r'F:\张丽辉案例\片段整理-2.xls'
    # time_trans(xls_path, out_xls)

    # 视频切分
    # video_path = r'\\192.168.0.60\public\测试视频\图文视频测试\139'
    # out_path = video_path+'_clip'
    # xls_path = r'F:\张丽辉案例\片段整理-2.xls'
    # Video_Clip(xls_path, video_path, out_path)

    # xls_path = r'F:\张丽辉案例\result_type.xls'
    # gt_xls = r'F:\张丽辉案例\还原视频片段整理-1(1).xlsx'
    # out_xls = r'F:\张丽辉案例\check.xls'
    # check_xls(xls_path, gt_xls, out_xls)

    # xls_path = r'D:\0-张丽辉\result_type_终.xls'
    # out_xls = r'D:\0-张丽辉\out.xls'
    # check_score(xls_path, out_xls)
print('-----------------')