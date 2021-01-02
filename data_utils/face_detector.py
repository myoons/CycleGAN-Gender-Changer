import os
import cv2
import math
import argparse
import face_recognition

parser = argparse.ArgumentParser(description='Process Gender')
parser.add_argument('--g', required=True, default='man', type=str,help='Gender')

args = parser.parse_args()


load_dir = 'C:/Users/grand/Desktop/ML/CycleGAN/data/{}'.format(args.g)
store_dir = 'C:/Users/grand/Desktop/ML/CycleGAN/data/{}face/'.format(args.g[0])
face_count = 0
image_list = os.listdir(load_dir)

for i in range(len(image_list)):

    try:
        img_Url = load_dir + '/image_{}.jpg'.format(i)
    except Exception as e:
        continue

    try:
        image = face_recognition.load_image_file(img_Url)
    except Exception as e:
        continue

    # (top, right, bottom, left) order
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) != 1 :
        continue
    else :
        location = face_locations[0]

    try: 
        src = cv2.imread(img_Url, cv2.IMREAD_COLOR)
        height, width, channels = src.shape

        face_height = location[2] - location[0]
        face_width = location[1] - location[3] 

        face_top = location[0] - math.ceil(face_height * 0.5)
        face_bottom = location[2] + math.floor(face_height * 0.2)
        face_left = location[3] - math.floor(face_width * 0.3)
        face_right = location[1] + math.ceil(face_width * 0.3)

        if (face_bottom-face_top) < 90 or (face_right-face_left) < 90 :
            continue
        
        if face_top <= 0 : face_top = 0
        if face_bottom >= height-1 : face_bottom = height
        if face_left <= 0 : face_left = 0 
        if face_right >= width-1 : face_right = width
        
        cv2.imwrite(store_dir+'{}.jpg'.format(face_count), src[face_top:face_bottom, face_left:face_right])
        face_count += 1

    except Exception as e:
        print ('Image : {} / For Loop Exception : {}'.format(i, e))
        continue