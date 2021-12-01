# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/3/11 14:13
from my_utils.my_util import *
"""
图片补黑边
"""
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m"%'   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
    print(bar, end='', flush=True)

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

def size_same(path, save_path):
    image_list = fetch_all_imgs(path)
    for i in range(len(image_list)):
        image = image_list[i]
        image_name = os.path.basename(image)
        image = cv2_imread(image)
        black_image = make_black_img(image)
        #size = (512, 512)
        #image_resize = cv2.resize(black_image, size)  # resize
        image_resize = black_image  # 不resize
        cv2_imwrite(os.path.join(save_path, image_name), image_resize)
        process_bar(i / len(image_list), start_str = '', end_str = '100%', total_length = 10)

if __name__ == '__main__':
    path = r'D:\0-杜泓柳\数据集三 内部连续患者'
    case_list = os.listdir(path)
    for case in case_list:
        case_path = os.path.join(path, case)
        save_path = case_path + '_size'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        size_same(case_path, save_path)