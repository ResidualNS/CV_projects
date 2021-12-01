# -*- coding: utf-8 -*-
# __author__:YZY
# 2020/12/8 13:38
import os
import csv
import json

def create_csv(csv_path):
    heads = ['filename', 'file_size', 'file_attributes', 'region_count', 'region_id', 'region_shape_attributes',
             'region_attributes']
    with open(csv_path, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(heads)

def write_csv(image_path, bbox, csv_path):
    image_size = os.path.getsize(image_path)
    image_name = image_path.split('\\')[-1]
    box = bbox[0]
    if box == 0:
        print('------no box------')
    else:
        x = box[0]
        y = box[1]
        w = box[2] - box[0]
        h = box[3] - box[1]
        box_dict = {"name": "rect", "x": int(x), "y": int(y), "width": int(w), "height": int(h)}

        values = [image_name, image_size, "{}", 1, 0, json.dumps(box_dict), "{}"]

        with open(csv_path, 'a+', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(values)
        print('------finish write_csv------')

