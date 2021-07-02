# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/4/15 11:19

import os
import sys
import io
import cv2
import skimage.transform as trans
import shutil
import numpy as np
from PIL import Image
from my_utils.mini_unet_model import mini_unet_model
from my_utils.model_encrypt import decrypt_file
from my_utils.my_until import *

sys.path.insert(0, r'E:\yzy_projects\znyx-trainer\trainer')

from mbsh.core.unet.data import *
from mbsh.core.unet_pp.segmentation_models import Unet, Xnet
from mbsh.core.images import save_img_file

from keras.engine.topology import load_weights_from_hdf5_group

def take_length(elem):
    return len(elem)

def resize_image(img, size):
    """
    resize 保持原图的长宽比
    """
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    iw, ih = image.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (0, 0, 0))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    img = np.array(new_image)
    return (scale, nw, nh), img[:, :, ::-1]


def imgread(img_path):
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)

def process_img(model, src_img, img_size, is_stable=False, change_value=None, x_h=0, y_h=0, w_h=0, h_h=0,
                fast_flag=False):
    src_img_bak = src_img.copy()

    if fast_flag:
        x1 = x_h
        y1 = y_h
        w1 = w_h
        h1 = h_h
        img_out = src_img_bak[y1:y1 + h1, x1:x1 + w1, :]
        return src_img, img_out, (x1, y1, w1, h1)

    src_h = src_img_bak.shape[0]
    src_w = src_img_bak.shape[1]

    new_w, new_h = img_size
    src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
    srcbak = src_img.copy()
    (scale, nw, nh), img = resize_image(src_img, img_size)

    # trans.resize把img从numpy.uint8类型转换为numpy.float64
    img = trans.resize(img, img_size)
    img = np.reshape(img, (1,) + img.shape)
    #     img = np.reshape(img.astype('float64'), (1,) + img.shape)

    # 模型识别图片, results为(1, 512, 512, 1)，是灰度图片
    results = model.predict(np.array(img), verbose = 0)

    # gray_img是（512，512）的灰度图，元素类型numpy.float32
    gray_img = results[0][:, :, 0]
    gray_img[np.where(gray_img <= 0.3)] = 0

    # heatmap转为灰度图
    bw_heatmap = np.uint8(255 * gray_img)
    bw_heatmap[bw_heatmap != 0] = 255
    _, ai_ctrs, _ = cv2.findContours(bw_heatmap.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ai_ctrs.sort(key = take_length, reverse = True)
    if len(ai_ctrs) >= 1:
        x, y, w, h = cv2.boundingRect(ai_ctrs[0])

        # 映射到原图尺寸的坐标系

        x = x - (new_w - nw) // 2
        y = y - (new_h - nh) // 2

        new_x = 0 if x < 0 else x
        new_y = 0 if y < 0 else y

        x1 = int(new_x / scale)
        y1 = int(new_y / scale)
        w1 = int(w / scale)
        h1 = int(h / scale)

        if is_stable:
            if abs(x1 - x_h) < change_value and abs(y1 - y_h) < change_value and abs(w1 - w_h) < change_value and abs(
                    h1 - h_h) < change_value:
                x1 = x_h
                y1 = y_h
                w1 = w_h
                h1 = h_h
    else:
        x1 = 0
        y1 = 0
        w1 = src_w
        h1 = src_h

    # 画矩形
    cv2.rectangle(src_img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 5)

    img_out = src_img_bak[y1:y1 + h1, x1:x1 + w1, :]
    return srcbak, img_out, (x1, y1, w1, h1)


if __name__ == '__main__':
    ### load encrypted model trained by zhangkuo
    file = r"E:\yzy_projects\model_data\裁边模型\u_model1.h5.e"
    model = mini_unet_model()
    dec_file = decrypt_file(file, file_handle = True)
    load_weights_from_hdf5_group(dec_file, model.layers)
    test_img_path = r"\\192.168.0.142\work_yzy\SfMLearner-master\data\resulting\formatted\data_input"
    result_path = r"\\192.168.0.142\work_yzy\SfMLearner-master\data\resulting\formatted\data_input_crop"

    # 参数设置
    img_size = (256, 256)

    # input_size
    input_size = img_size + (3,)

    # unet or unet++
    use_unet = False

    # 是否开启保持稳定的策略， x,y,w,h 变化大于一定值才更新
    is_stable = True
    change_value = 20   # x,y,w,h 任一值变化大于10 像素才更新

    for case in os.listdir(test_img_path):
        case_dir_path = os.path.join(test_img_path, case)
        result_case_dir_path = os.path.join(result_path, case)

        if not os.path.exists(result_case_dir_path):
            os.makedirs(result_case_dir_path)

        images = fetch_all_imgs(case_dir_path)
        print(case_dir_path)

        for img in images:
            image_np = imgread(os.path.join(case_dir_path, img))
            x_h,y_h,w_h,h_h = 0, 0, 0, 0
            img2video, img2jpg, (x1, y1, w1, h1) = process_img(model, image_np, img_size, is_stable, change_value, x_h,y_h,w_h,h_h, fast_flag=False)
            x_h,y_h,w_h,h_h = x1, y1, w1, h1
            io.imsave(os.path.join(result_case_dir_path, img.split('\\')[-1][:-4] + '.jpg'), img2jpg[:, :, :: -1])
print('-------------')