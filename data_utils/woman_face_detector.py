import face_recognition
import cv2

count = 571

for i in range(512):

    img_Url = 'data/foreign_woman/image_{}.jpg'.format(i)
    image = face_recognition.load_image_file(img_Url)

    # (top, right, bottom, left) order
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) > 1:
        continue

    try: 
        for idx, location in enumerate(face_locations):

            src = cv2.imread(img_Url, cv2.IMREAD_COLOR)
            height, width, channels = src.shape


            face_hieght = location[2] - location[0]
            face_width = location[1] - location[3] 
            
            face_top = location[0] - int(face_hieght * 0.7)
            face_bottom = location[2] + int(face_hieght * 0.5)
            face_left = location[3] - int(face_width * 0.5)
            face_right = location[1] + int(face_width * 0.5)

            if face_top <= 0 : face_top = 0
            if face_bottom >= height-1 : face_bottom = height
            if face_left <= 0 : face_left = 0 
            if face_right >= width-1 : face_right = width
            
            cv2.imwrite('data/woman_face/{}.jpg'.format(count), src[face_top:face_bottom, face_left:face_right])
    except:
        continue

    count += 1