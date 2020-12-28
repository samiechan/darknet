import csv
import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET_NAME = 'open-images-dataset'
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
CLASS_LIST = ['/m/03bt1vf','/m/04yx4']
img_name = "111111111111"

with open('build\\darknet\\x64\\data\\obj\\oidv6-train-annotations-bbox.csv', "r") as csvfile:
    bboxs = csv.reader(csvfile, delimiter=',', quotechar='|')
    for bbox in bboxs:
        if bbox[2] in CLASS_LIST:
            if img_name != bbox[0]:
                if not os.path.isfile("build\\darknet\\x64\\data\\obj\\%s.jpg"%bbox[0]):
                    key = "train/%s.jpg"%bbox[0]
                    destination = "build\\darknet\\x64\\data\\obj\\%s.jpg"%bbox[0]
                    s3.Bucket(BUCKET_NAME).download_file(key, destination)
                    out_file = open("build\\darknet\\x64\\data\\obj\\%s.txt"%bbox[0], 'w')
                    img_name = bbox[0]
            if img_name == bbox[0]:
                    out_file.write(str(CLASS_LIST.index(bbox[2])) + " " + str(float(bbox[4])+(float(bbox[5])-float(bbox[4]))/2) + " " + str(float(bbox[6])+(float(bbox[7])-float(bbox[6]))/2)+ " " + str(float(bbox[5])-float(bbox[4])) + " " + str(float(bbox[7])-float(bbox[6])) + '\n')
