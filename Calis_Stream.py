import requests
import numpy as np
import cv2
import time

ip = "192.168.1.66"
shot  = "http://" + ip + ":8080/shot.jpg"
photo = "http://" + ip + ":8080/photoaf.jpg"
flash_on  = "http://" + ip + ":8080/enabletorch"
flash_off = "http://" + ip + ":8080/disabletorch"

last_photos = []
stripes = cv2.imread('stripes.jpg', 1)
stripes = cv2.resize(stripes, (880, 165))

pic_num = 0
flash = False
while True:
    if len(last_photos) == 1:
        stripes[15:150,20:200] = cv2.resize(last_photos[-1], (180, 135))
    elif len(last_photos) == 2:
        stripes[15:150,20:200]  = cv2.resize(last_photos[-1], (180, 135))
        stripes[15:150,240:420] = cv2.resize(last_photos[-2], (180, 135))
    elif len(last_photos) == 3:
        stripes[15:150,20:200]  = cv2.resize(last_photos[-1], (180, 135))
        stripes[15:150,240:420] = cv2.resize(last_photos[-2], (180, 135))
        stripes[15:150,460:640] = cv2.resize(last_photos[-3], (180, 135))
    elif len(last_photos) >= 4:
        stripes[15:150,20:200]  = cv2.resize(last_photos[-1], (180, 135))
        stripes[15:150,240:420] = cv2.resize(last_photos[-2], (180, 135))
        stripes[15:150,460:640] = cv2.resize(last_photos[-3], (180, 135))
        stripes[15:150,680:860] = cv2.resize(last_photos[-4], (180, 135))
    

    img_resp = requests.get(shot)
    img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img_big = cv2.resize(img, (880, 660))
    img_stripes = np.concatenate((img_big, stripes), axis=0)
    cv2.imshow("Android Cam", img_stripes)

    k = cv2.waitKey(30)
    if k == 27:                  
        break
    elif k == -1:
        continue
    elif k == 32:
        print("Taking Pic")
        requests.get(flash_on)
        img_resp = requests.get(photo)
        requests.get(flash_off)
        img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img_4k = cv2.imdecode(img_arr, -1)
        cv2.imwrite("wapo_" + str(pic_num) + ".jpg", img_4k)
        pic_num += 1
        last_photos.append(img)
        print("Okay Cool")
    elif k == 102:
        if flash:
            requests.get(flash_off)
            flash = False
        else:
            requests.get(flash_on)
            flash = True
        
    else:
        print(k)
cv2.destroyAllWindows()

##img_resp = requests.get(photo)
##img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
##img = cv2.imdecode(img_arr, -1)
##cv2.imwrite("wapo.jpg", img)
##cv2.imshow("Android Cam", img)
##cv2.waitKey(0)
##cv2.destroyAllWindows()
