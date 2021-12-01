# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/7/29 14:08
from my_utils.my_util import *

def get_mask(image_path, out_path):
    '''
    mask形态学处理
    '''
    image_name = os.path.basename(image_path)
    img = cv2_imread(image_path)
    img = img[:, :, 0]
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret1, img_1 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_OTSU)
    # ret2, img_2 = cv2.threshold(img_1, 1, 255, cv2.THRESH_BINARY_INV)
    h, w = img.shape[0], img.shape[1]
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int((h+w)/200), int((h+w)/200)))
    img_2 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel1, iterations=10)
    img_2 = cv2.erode(img_2, kernel1, iterations = 2)
    cv2_imwrite(os.path.join(out_path, image_name), img_2)


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\result-\result0'
    out_path = r'C:\Users\Administrator\Desktop\result\result'
    images_list = fetch_all_files(path, followlinks = ('jpg', 'png', 'PNG', 'bmp', 'BMP', 'JPG'))  # 获取图片路径列表
    num = 0
    for image_path in images_list[:]:
        get_mask(image_path, out_path)
        num += 1
        print(num)

