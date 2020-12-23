# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/9 15:39
import cv2
import os
import numpy as np


def cv2_imread(img_path):
    img_read = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img_read

def cv2_imwrite(path, img_write):
    suffix = os.path.splitext(path)[-1]
    cv2.imencode(suffix, img_write)[1].tofile(path)

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
            if name.endswith(('jpg', 'png', 'jpeg', 'bmp', 'BMP', 'JPG')):
                path_join = os.path.join(root, name)
                all_imgs.append(path_join)

    # logger.debug("fetch_all_files count=%s" % len(all_files))
    return all_imgs

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
