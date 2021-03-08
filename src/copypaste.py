import cv2
import os
import numpy as np
from copy_paste import CopyPaste
from coco import CocoDetectionCP
from visualize import display_instances
import albumentations as A
import random
from matplotlib import pyplot as plt

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from copy_paste import CopyPaste
import json
from skimage import measure

def create_json_images(image_filename,image_data,id):
    tmps = []

    tmp = dict()
    tmp["license"] = 1
    tmp["id"] = id
    tmp["file_name"] = image_filename
    tmp["width"] = image_data.shape[1]
    tmp["height"] = image_data.shape[0]
    tmp["date_captured"] = ""
    tmp["coco_url"] = "dummy_words"
    tmp["flickr_url"] = "dummy_words"
    return [tmp]


def create_json_annotations(masks,bboxes,id,annotation_id):
    tmps = []


    annotation_list = []


    for ix, bbox in enumerate(bboxes):
        tmp={}

        tmp["bbox"]=bbox[:4]

        contours = measure.find_contours(masks[ix], 0.8)
        tmp_segmentation_list = []

        for contour in contours:
            for a in contour:
                tmp_segmentation_list.append(int(a[1]))
                tmp_segmentation_list.append(int(a[0]))


        # print(segmentation_list)
        tmp["segmentation"] = [tmp_segmentation_list]
        tmp["id"] = annotation_id
        tmp["image_id"] = id
        tmp["category_id"] = bbox[4]
        tmp["area"] = (bbox[2]) * (bbox[3])
        tmp["iscrowd"] = 0
        annotation_list.append(tmp)
        annotation_id=annotation_id+1

    return annotation_list,annotation_id
    

transform = A.Compose([
    #   A.RandomScale(scale_limit=(-0.9, 1), p=1), #LargeScaleJitter from scale of 0.1 to 2
    #   A.PadIfNeeded(256, 256, border_mode=0), #constant 0 border
    #   A.RandomCrop(256, 256),
    #   A.HorizontalFlip(p=0.5),
    #   CopyPaste(blend=True, sigma=1, pct_objects_paste=0.5, p=1)
    ], bbox_params=A.BboxParams(format="coco")
)


data = CocoDetectionCP(
    './coco/images/', 
    './coco/annotations.json', 
    transform
)

json_open = open('./coco/annotations.json', 'r')
json_load = json.load(json_open)

new_json_obj=json_load.copy()

# del new_json_obj['images']
# del new_json_obj['annotations']
# new_json_obj['images']=[]
# new_json_obj['annotations']=[]

image_id=0
for obj in new_json_obj['images']:

    if obj['id'] > image_id:
        image_id=obj['id']

annotation_id=0
for obj in new_json_obj['annotations']:
    print(obj['id'])
    if obj['id'] > annotation_id:
        annotation_id=obj['id']

NUMBER_ID=image_id+1

id=image_id+1
annotation_id=annotation_id+1

for index in range(len(data)):
    img_data = data[index]
    image = img_data['image']
    masks = img_data['masks']
    bboxes = img_data['bboxes']


    os.makedirs("output", exist_ok=True)

    #image filename
    image_filename="test{:003}.png".format(id)

    print("output/"+image_filename)
    cv2.imwrite("output/"+image_filename,image)


    new_json_obj["images"].extend(create_json_images(image_filename,image,id))
    annotation_list,annotation_id=create_json_annotations(masks,bboxes,id,annotation_id)
    new_json_obj["annotations"].extend(annotation_list)

    id=id+1
    # if id==1002:
    #     break

with open("testcoco.json", 'w') as outfile:
    json.dump(new_json_obj, outfile)