# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/9 9:38
import csv
from my_utils.my_util import *
'''
根据csv标注信息裁框，生成resnet分类数据集
'''

def load_csv(csv_path, image_name):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        bbox = []
        for r in reader:
            if r[0] == image_name:
                box_dict = eval(r[5])
                if len(box_dict) == 0:
                    return []
                x = box_dict["x"]
                y = box_dict["y"]
                w = box_dict["width"]
                h = box_dict["height"]
                box = [x, y, w + x, h + y]
                bbox.append(box)

    return bbox

def cut_box(image_path, bbox,save_path, area_ = 0.0, bias_ = 0.0 ):
    if len(bbox) == 0:
        return
    image = cv2_imread(image_path)
    h = image.shape[0]
    w = image.shape[1]

    for i, box in enumerate(bbox):
        max_ = max(h, w)
        a = max_
        image_new = np.zeros([a, a, 3], np.uint8)  # 创建一个长边为边长的正方形全黑图像
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        w_box = x2 - x1
        h_box = y2 - y1
        s_box = (w_box+h_box)/2
        bias_scale = int(bias_ * s_box)
        if w_box > area_ * a and h_box > area_ * a:
            x1 = x1 - bias_scale
            y1 = y1 - bias_scale
            x2 = x2 + bias_scale
            y2 = y2 + bias_scale
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if y2 > h:
                y2 = h
            if x2 > w:
                x2 = w
            w_box = x2 - x1
            h_box = y2 - y1

            image_box = image[y1:y2, x1:x2]  # 在原图中裁出box区域

            x1_new = int(a/2 - w_box/2)
            x2_new = x1_new + w_box
            y1_new = int(a/2 - h_box/2)
            y2_new = y1_new + h_box
            if x1_new < 0:
                x1_new = 0
            if y1_new < 0:
                y1_new = 0
            if x2_new > a:
                x2_new = a
            if y2_new > a:
                y2_new = a

            image_new[y1_new:y2_new, x1_new:x2_new] = image_box
            image_new = cv2.resize(image_new, (224, 224))
            cv2_imwrite(save_path + '_' + str(i) + '.jpg', image_new)

def cut_box_b(image_path, bbox, save_path, area_=0.0, bias_=0.0):
    if len(bbox) == 0:
        return
    image = cv2_imread(image_path)
    h = image.shape[0]
    w = image.shape[1]

    for i, box in enumerate(bbox):
        max_ = max(h, w)
        a = 224
        image_new = np.zeros([a, a, 3], np.uint8)  # 创建一个长边为边长的正方形全黑图像
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        w_box = x2 - x1
        h_box = y2 - y1
        s_box = (w_box + h_box) / 2
        bias_scale = int(bias_ * s_box)
        if w_box > area_ * max_ and h_box > area_ * max_:
            x1 = x1 - bias_scale
            y1 = y1 - bias_scale
            x2 = x2 + bias_scale
            y2 = y2 + bias_scale
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if y2 > h:
                y2 = h
            if x2 > w:
                x2 = w
            w_box = x2 - x1
            h_box = y2 - y1

            image_box = image[y1:y2, x1:x2]  # 在原图中裁出box区域
            x1_new = int(a / 2 - w_box / 2)
            x2_new = x1_new + w_box
            y1_new = int(a / 2 - h_box / 2)
            y2_new = y1_new + h_box
            if x1_new < 0:
                x1_new = 0
            if y1_new < 0:
                y1_new = 0
            if x2_new > a:
                x2_new = a
            if y2_new > a:
                y2_new = a
            if image_box.shape[0] >= 224 or image_box.shape[1] >= 224:
                image_box = make_black_img(image_box)
                image_box = cv2.resize(image_box, (224, 224))
                image_new = image_box
            else:
                image_new[y1_new:y2_new, x1_new:x2_new] = image_box
            cv2_imwrite(save_path + '_' + str(i) + '.jpg', image_new)

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

if __name__ == '__main__':
    path = r'E:\宫德馨dataset\数据准备\褪色调\原图'
    cls = r'\非瘤变-测试集'
    images_path = path + cls
    out_path = path
    saves_path = out_path + cls + '_cut'
    csv_path = r'E:\宫德馨dataset\数据准备\褪色调\褪色调.csv'
    if not os.path.exists(saves_path):
        os.makedirs(saves_path)

    images_list = fetch_all_files(images_path, followlinks = ('jpg', 'png', 'jpeg', 'bmp', 'BMP', 'JPG'))  # 获取图片路径列表
    for image_path in images_list[:]:
        print('正在裁剪图片：', image_path)
        image_name = os.path.basename(image_path)
        bbox = load_csv(csv_path, image_name)
        save_path = os.path.join(saves_path, image_name[:-4])
        cut_box_b(image_path, bbox, save_path, area_ = 0.00, bias_ = 0.0)
    print('---------------finish----------------------')