# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/3 10:44
import cv2
from PIL import Image
import os
import time
import numpy as np
import shutil
from yolo3.yolo import YOLO
from my_utils.draw_toolbox import *
from my_utils.box_save_csv import *

'''
测试yolo模型的灵敏度和特异度
'''

class test_img():
    def __init__(self, img_path, yolo_model):
        self.img_path = img_path
        self.yolo_model = yolo_model
        self.image = self.cv2_imread()

    def cv2_imread(self):
        img_read = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        return img_read

    def cv2_imwrite(self, path, img_write):
        suffix = os.path.splitext(path)[-1]
        cv2.imencode(suffix, img_write)[1].tofile(path)

    def is_valid_box(self, image, box):
        if len(image) == 0 or len(box) == 0:
            return False
        target = image[int(box[1]): int(box[3]), int(box[0]): int(box[2])]
        if len(target) == 0 or len(target[0]) == 0:
            return False
        avg = float(np.max(target)) - float(np.min(target))

        valid = avg > 50
        return valid

    def make_black_img(self, src_img):
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
        return black_img

    def test_bbox(self, min_ratio=0.02, max_ratio=1.0, min_level=0.03):
        img = self.make_black_img(self.image)
        yolo_model = self.yolo_model
        size = yolo_model.model_image_size
        print(size)
        image_resize = cv2.resize(img, size)
        boxes, scores, labels = yolo_model.predict_img(image_resize)

        check_boxes = []
        max_size = max_ratio * size[0]
        min_size = min_ratio * size[0]
        max_score = 0
        first_box = []
        for box, score, label in zip(boxes, scores, labels):
            if score < min_level:
                break
            if (box[2] - box[0]) > max_size or (box[3] - box[1]) > max_size:
                continue
            if (box[2] - box[0]) < min_size or (box[3] - box[1]) < min_size:
                continue
            # ignore other label
            if label > 0:
                continue
            if not self.is_valid_box(image_resize, box):
                continue
            # bbox = [float(x) * 224 / size for x in box]
            if score >= max_score:
                first_box = [int(box[1]), int(box[0]), int(box[3]), int(box[2])]
                max_score = score
        check_boxes.append(first_box)

        return check_boxes, max_score

    def draw_box(self, save_path, wukuang_path, youkuang_path):
        image_resize, size = self.make_black_img(self.image)
        bbox, score = self.test_bbox()
        if score == 0:
            self.cv2_imwrite(wukuang_path, self.image)
            print('-------无病灶--------')
        else:
            self.cv2_imwrite(youkuang_path, self.image)
            result_img = bboxes_draw_on_img(image_resize, score, bbox)
            self.cv2_imwrite(save_path, result_img)

    def save_csv(self, csv_path):
        bbox, score = self.test_bbox()
        if not os.path.exists(csv_path):
            create_csv(csv_path)
        write_csv(self.img_path, bbox, csv_path)

def fetch_all_files(from_dir, followlinks=True, file_exts=None):
    """
    获取目录下所有文件
    """
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(from_dir, followlinks=followlinks):
        if len(dirs) != 0:
            all_dirs.extend(dirs)
        for name in files:
            if file_exts:
                _, ext = os.path.splitext(name)
                if ext not in file_exts:
                    # logger.debug("exclude file %s,%s" % (name, ext))
                    continue

            path_join = os.path.join(root, name)
            all_files.append(path_join)

    # logger.debug("fetch_all_files count=%s" % len(all_files))
    return all_files

def load_yolo3_model(model_path, img_size):
    if not os.path.exists(model_path):
        print(" can not find file %s " % os.path.abspath(model_path))
        return
    print("  find file %s " % os.path.abspath(model_path))

    model = YOLO(model_path=model_path, model_image_size=img_size)

    return model


# def test_wl_YOLO_tnr(yolo_model):
#     input_dirs = [r"E:\徐铭dataset\宜昌一医_终\特异度测试\无病灶"]
#
#     box_dir = r"E:\徐铭dataset\宜昌一医_终\特异度测试\预测box结果"
#     if not os.path.exists(box_dir):
#         os.makedirs(box_dir)
#     save_dir = r"E:\徐铭dataset\宜昌一医_终\特异度测试\预测有框原图"
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#
#     for input_dir in input_dirs:
#         files = fetch_all_files(input_dir,
#                                 file_exts=[".jpg", ".Jpg", ".jpeg", ".PNG", ".png", ".Bmp", ".bmp", ".BMP", ".JPG"])
#         if len(files) < 1:
#             continue
#
#         for file in files[:]:
#             with open(file, 'rb') as img_file:
#                 bytes = img_file.read()
#                 nparr = np.fromstring(bytes, np.uint8)
#                 image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#             if not hasattr(image, "shape"):
#                 print(file)
#                 continue
#
#             file_name = os.path.basename(file)
#             T = test_img(file, yolo_model)
#
#             check_boxes, max_score = T.test_bbox(min_ratio=0.02, min_level=0.03)
#             # 取score最高的标记框
#             bbox = check_boxes[0]
#             if len(bbox) == 0:
#                 continue
#
#             # 保存预测有框的原图
#             save_path = os.path.join(save_dir, file_name)
#             save_img = cv2.resize(image, (720, 720))
#             cv2.imencode('.jpg', save_img)[1].tofile(save_path)
#
#             # 保存预测有框的box图
#             box_path = os.path.join(box_dir, file_name)
#             rect = bbox
#             bbox_img = cv2.resize(image, (720, 720))
#             scale = bbox_img.shape[0] / 224
#
#             x1, y1, x2, y2 = int(rect[0] * scale), int(rect[1] * scale), int(rect[2] * scale), int(rect[3] * scale)
#             cv2.rectangle(bbox_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
#             cv2.imencode('.jpg', bbox_img)[1].tofile(box_path)
#
#
# def test_wl_YOLO_tpr(yolo_model):
#     input_dirs = [r"E:\徐铭dataset\宜昌一医_终\灵敏度测试\低风险gt", \
#                   r"E:\徐铭dataset\宜昌一医_终\灵敏度测试\高风险gt"]
#
#     no_box_dir = r"E:\徐铭dataset\宜昌一医_终\灵敏度测试\预测无框"
#     if not os.path.exists(no_box_dir):
#         os.makedirs(no_box_dir)
#     box_dir = r"E:\徐铭dataset\宜昌一医_终\灵敏度测试\预测有框"
#     if not os.path.exists(box_dir):
#         os.makedirs(box_dir)
#
#
#     for input_dir in input_dirs:
#         files = fetch_all_files(input_dir,
#                                 file_exts=[".jpg", ".Jpg", ".jpeg", ".PNG", ".png", ".Bmp", ".bmp", ".BMP", ".JPG"])
#         if len(files) < 1:
#             continue
#
#         count = 0
#         for file in files[:]:
#             with open(file, 'rb') as img_file:
#                 bytes = img_file.read()
#                 nparr = np.fromstring(bytes, np.uint8)
#                 image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#             if not hasattr(image, "shape"):
#                 print(file)
#                 continue
#
#             file_name = os.path.basename(file)
#             box_path = os.path.join(box_dir, file_name)
#             no_box_path = os.path.join(no_box_dir, file_name)
#
#             T = test_img(file, yolo_model)
#             check_boxes, max_score = T.test_bbox(min_ratio=0.02, min_level=0.03)
#             # 取score最高的标记框
#             bbox = check_boxes[0]
#             save_img = cv2.resize(image, (720, 720))
#
#             if len(bbox) == 0:
#                 cv2.imencode('.jpg', save_img)[1].tofile(no_box_path)
#                 continue
#             cv2.imencode('.jpg', save_img)[1].tofile(box_path)
#
# def check_images():
#     del_imgs = os.listdir(r"E:\徐铭dataset\高低风险测试\除外805预测无框")
#     print(del_imgs)
#     input_dirs = [r"E:\徐铭dataset\高低风险测试\除外805\低风险", \
#                   r"E:\徐铭dataset\高低风险测试\除外805\高风险"]
#     n =0
#     for input_dir in input_dirs:
#         files = fetch_all_files(input_dir,
#                                 file_exts=[".jpg", ".Jpg", ".jpeg", ".PNG", ".png", ".Bmp", ".bmp", ".BMP", ".JPG"])
#         if len(files) < 1:
#             continue
#
#         for file in files:
#             file_name = os.path.basename(file)
#             if file_name in del_imgs:
#                 n += 1
#                 os.remove(file)
#     print(n)



if __name__ == '__main__':
    model_path = './model_data/y_model1.h5'
    # images_path = './Dataset/05荆门石化分类汇总 白光分类'
    # saves_path = images_path + '_yolo'
    # wukuang_path = images_path + '_yolo_wukuang'
    # youkuang_path = images_path + '_yolo_youkuang'
    image_size = (352, 352)
    #
    # dirs_list, images_list = fetch_all_files(images_path)  # 获取图片路径列表
    # for d in dirs_list:
    #     if not os.path.exists(saves_path + '/' + d):
    #         os.makedirs(saves_path + '/' + d)
    #     if not os.path.exists(wukuang_path + '/' + d):
    #         os.makedirs(wukuang_path + '/' + d)
    #     if not os.path.exists(youkuang_path + '/' + d):
    #         os.makedirs(youkuang_path + '/' + d)

    yolo_model = load_yolo3_model(model_path, image_size)  # 导入模型
    #test_wl_YOLO_tpr(yolo_model)
    #test_wl_YOLO_tnr(yolo_model)
    #check_images()

    # start_time = time.time()
    # for image_path in images_list:
    #     print('正在识别图片：', image_path)
    #     # 实例化类
    #     T = test_img(image_path, model)
    #
    #     # 预测并画框可视化、分文件夹原图保存（有框-无框）
    #     save_path = image_path.replace(images_path, saves_path)
    #     save_path = save_path[:-4] + '_box.jpg'
    #     wukuang = image_path.replace(images_path, wukuang_path)
    #     youkuang = image_path.replace(images_path, youkuang_path)
    #     T.draw_box(save_path, wukuang, youkuang)
    #
    #     # # 预测后将box坐标存csv
    #     # csv_path = saves_path + '/' + save_path.split('\\')[-2] + '.csv'
    #     # T.save_csv(csv_path)
    #
    # end_time = time.time()
    # print('time:', end_time - start_time)
print('-----------------------------------------')
