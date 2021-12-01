# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/7 10:40
import cv2
import matplotlib.cm as mpcm


def gain_translate_table():
    label2name_table = {}
    #for class_name, labels_pair in dataset_common.VOC_LABELS.items():
        #label2name_table[labels_pair[0]] = class_name
    return label2name_table

label2name_table = gain_translate_table()

def colors_subselect(colors, num_classes=21):
    dt = len(colors) // num_classes
    sub_colors = []
    for i in range(num_classes):
        color = colors[i*dt]
        if isinstance(color[0], float):
            sub_colors.append([int(c * 255) for c in color])
        else:
            sub_colors.append([c for c in color])
    return sub_colors

colors = colors_subselect(mpcm.plasma.colors, num_classes=21)
colors_tableau = [(205, 205, 205), (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

def bboxes_draw_on_img(img, bboxes, conf_colour=0.57, thickness=2):
    scale = 0.4
    text_thickness = 2
    line_type = 2
    for i in range(len(bboxes)):
        bbox = bboxes[i]

        # Draw bounding boxes
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[2]), int(bbox[3]))
        if (p2[0] - p1[0] < 1) or (p2[1] - p1[1] < 1):
            continue
        if conf_colour <= 0.57:
            ret = cv2.rectangle(img, p1, p2, (255, 0, 0), thickness) #画矩形框
        elif conf_colour > 0.57:
            ret = cv2.rectangle(img, p1, p2, (0, 0, 255), thickness)  # 画矩形框

        # s = '%s/%.1f%%' % ('ca', scores[i]*100)  # 标签
        # p = []
        # p.append(p1)
        # p.append(p2)
        # #text_size is (width, height)
        # text_size, baseline = cv2.getTextSize(s, cv2.FONT_HERSHEY_SIMPLEX, scale, text_thickness)
        # p1 = (p1[0] - text_size[1], p1[1])
        # #cv2.rectangle(img, (p1[1] - thickness//2, p1[0] - thickness - baseline), (p1[1] + text_size[0], p1[0] + text_size[1]), color, -1)
        # #cv2.putText(img, s, (p1[1], p1[0] + baseline), cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), text_thickness, line_type)
        # cv2.putText(img, s, (p1[0], p1[1]), cv2.FONT_HERSHEY_COMPLEX, scale, (255,0,0),thickness=text_thickness, lineType=line_type)
        # plt.show()

    #print('---------------finish draw---------------')
    return img
