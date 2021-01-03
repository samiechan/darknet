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
            txt_file_input = str(CLASS_LIST.index(bbox[2])) + " " + str(float(bbox[4])+(float(bbox[5])-float(bbox[4]))/2) + " " + str(float(bbox[6])+(float(bbox[7])-float(bbox[6]))/2)+ " " + str(float(bbox[5])-float(bbox[4])) + " " + str(float(bbox[7])-float(bbox[6]))
            txt_file_path = "build\\darknet\\x64\\data\\obj\\%s.txt"%bbox[0]
            jpg_file_path = "build\\darknet\\x64\\data\\obj\\%s.jpg"%bbox[0]
            
            if img_name != bbox[0]:
                if not os.path.isfile(jpg_file_path):
                    key = "train/%s.jpg"%bbox[0]
                    destination = jpg_file_path
                    print("Downloading", jpg_file_path)
                    s3.Bucket(BUCKET_NAME).download_file(key, destination)                    
                    open(txt_file_path, 'w').close()
                    img_name = bbox[0]

            with open(txt_file_path, 'r') as f:
                if txt_file_input not in f.read():
                    print("Bouding box is not found in the text file. Adding to", txt_file_path)
                    print(txt_file_input)
                    with open(txt_file_path, 'w') as f2:
                        f2.write(txt_file_input + '\n')
