# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/9 15:39
import cv2
import os
import numpy as np
import pickle
import shutil

def read_img_file(img_path):
    img_read = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img_read


def write_img_file(path, img_data):
    suffix = os.path.splitext(path)[-1]
    cv2.imencode(suffix, img_data)[1].tofile(path)


def cv2_imread(img_path):
    img_read = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img_read


def cv2_imwrite(path, img_write):
    suffix = os.path.splitext(path)[-1]
    cv2.imencode(suffix, img_write)[1].tofile(path)


def fetch_all_files(from_dir, followlinks=True, file_exts=None):
    """
    获取目录下所有文件
    """
    print('ss')
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


def fetch_all_imgs(from_dir, followlinks=True, file_exts=None):
    """
    获取目录下所有文件
    """
    all_imgs = []
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
            if name.endswith(('jpg', 'png', 'jpeg', 'bmp', 'BMP', 'JPG', 'PNG')):
                path_join = os.path.join(root, name)
                all_imgs.append(path_join)

    # logger.debug("fetch_all_files count=%s" % len(all_files))
    return all_imgs


def save_cache(data, file_path):
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file = open(file_path, 'wb')

    pickle.dump(data, file)
    file.close()


def load_cache(file_path):
    data = dict()
    if os.path.isfile(file_path):
        file = open(file_path, 'rb')
        data = pickle.load(file)
        file.close()
    else:
        print('cache file not exist: ' + file_path)

    return data


def resize_img(image):
    """
    resize 补黑边为边长size大小的正方形
    """
    h = image.shape[0]
    w = image.shape[1]
    a = max(h, w)

    image_new = np.zeros([a, a, 3], np.uint8)

    x1_new = int(a / 2 - w / 2)
    x2_new = x1_new + w
    y1_new = int(a / 2 - h / 2)
    y2_new = y1_new + h
    image_new[y1_new:y2_new, x1_new:x2_new] = image

    return image_new, a


def create_imgs_fold(input_dirs):
    for input_dir in input_dirs:
        paths = os.listdir(input_dir)
        for path in paths[:]:
            print(path)
            video_path = os.path.join(input_dir, path)
            files_list = fetch_all_files(video_path)
            imgs_path = os.path.join(video_path, "imgs")
            if not os.path.exists(imgs_path):
                os.makedirs(imgs_path)
                for file in files_list:
                    shutil.move(file, imgs_path)
        #         print("finished one fold!")
        print("finished all cases!")


class LabelResult(object):
    def __init__(self, label_name, class_name=None, class_index=0, confidence=0.0, tolerance=0.5, overlay=None
                 , img_path=None, predictions=None, overlay_box=None, has_activate=False, overlay_cam=None):
        if predictions is None:
            predictions = []
        self.label_name = label_name
        self.class_name = class_name if class_name else label_name
        self.confidence = confidence
        self.tolerance = tolerance
        self.class_index = class_index
        self.overlay = overlay
        self.overlay_box = overlay_box
        self.overlay_cam = overlay_cam
        self.predictions = predictions
        self.has_activate = has_activate
        self.img_path = img_path
        self.report_path = None
        # 触发的激活的label
        self.trigger_activate_label = None

    def merge_confidence(self, classes):
        """
        合并多个类别的置信度
        """
        conf = 0
        if self.predictions is None or len(self.predictions) < 1:
            return conf

        for class_index in classes:
            conf += self.predictions[class_index]
        conf = conf / np.sum(self.predictions)
        return int(conf * 100)

    def succeed(self):
        return self.confidence > self.tolerance

    def __str__(self):
        return " %s :%s, %s (%s)" % (self.label_name, self.class_index, self.class_name, self.confidence)

    def model_2_json(self):
        return {"labelName": self.label_name, "className": self.class_name, "confidence": self.confidence,
                "tolerance": self.tolerance, "classIndex": self.class_index, "overlay": self.overlay,
                "overlayBox": self.overlay_box, "has_activate": self.has_activate, "img_path": self.img_path,
                "report_path": getattr(self, "report_path", None), "overlay_cam": getattr(self, "overlay_cam", None),
                "trigger_activate_label": getattr(self, "trigger_activate_label", None)}

