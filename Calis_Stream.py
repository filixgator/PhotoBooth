import requests
import numpy as np
import cv2
import time
import datetime
from urllib.request import urlopen

def url_to_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
##    image_Gra = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE).astype(float) / 255.0
    image_RGB = cv2.imdecode(image, 1)
    return image_RGB

def build_filters():
    filters = []
    ksize = 30
    for theta in np.arange(0, np.pi, np.pi / 16):
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        kern /= 1.5*kern.sum()
        filters.append(kern)
    return filters
 
def process_inhaler(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)
    return accum, img

def show_3(full_img):
    font                   = cv2.FONT_HERSHEY_TRIPLEX
    bottomLeftCornerOfText = (475,600)
    fontScale              = 18
    fontColor              = (0,0,0)
    lineType               = 18

    cv2.putText(full_img,'3', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    fontColor              = (255,255,255)
    lineType               = 8

    cv2.putText(full_img,'3', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    return full_img
def show_2(full_img):
    font                   = cv2.FONT_HERSHEY_TRIPLEX
    bottomLeftCornerOfText = (475,600)
    fontScale              = 18
    fontColor              = (0,0,0)
    lineType               = 18

    cv2.putText(full_img,'2', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    fontColor              = (255,255,255)
    lineType               = 8

    cv2.putText(full_img,'2', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    return full_img
def show_1(full_img):
    font                   = cv2.FONT_HERSHEY_TRIPLEX
    bottomLeftCornerOfText = (475,600)
    fontScale              = 18
    fontColor              = (0,0,0)
    lineType               = 18

    cv2.putText(full_img,'1', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    fontColor              = (255,255,255)
    lineType               = 8

    cv2.putText(full_img,'1', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    return full_img
    
    

def take_pic(photo, last_photos, stripes, wrapping_paper, pic_num, background):
    for i in range(4):
        frames = 0
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
            background[75:900,200:1080] = img_stripes
            if ((frames > 0)  and (frames < 5)):
                background = show_3(background)
    ##        if ((frames > 10) and (frames < 20)):
    ##            print("-")
            if ((frames > 8) and (frames < 13)):
                background = show_2(background)
    ##        if ((frames > 30) and (frames < 40)):
    ##            print("-")
            if ((frames > 16) and (frames < 21)):
                background = show_1(background)
    ##        if ((frames > 50) and (frames < 60)):
    ##            print("-")
            if (frames > 24):
    ##            print("Taking Pic")
            ##    requests.get(flash_on)
                img_resp = requests.get(photo)
            ##    requests.get(flash_off)
                img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
                img_4k = cv2.imdecode(img_arr, -1)
            ##        img_4k, gray_img = process_inhaler(img_4k, filters)
                date_and_time = datetime.datetime.now().strftime("%I_%M_%p_%B_%d_%Y_")
                cv2.imwrite(str(date_and_time) + str(pic_num) + ".jpg", img_4k)
                pic_num += 1
                if len(last_photos) >= 4:
                    del last_photos[:]
                    stripes = wrapping_paper[130:295, 0:880].copy()
                last_photos.append(img_4k)
                print(str(date_and_time) + str(pic_num) + ".jpg")
                len(last_photos)
                break
            
            cv2.imshow("Posada FM", background)
            k = cv2.waitKey(30)
            frames = frames + 1
    return pic_num

ip = "10.12.5.48"
shot  = "http://" + ip + ":8080/shot.jpg"
photo = "http://" + ip + ":8080/photoaf.jpg"
flash_on  = "http://" + ip + ":8080/enabletorch"
flash_off = "http://" + ip + ":8080/disabletorch"

url_trees = 'https://raw.githubusercontent.com/filixgator/PhotoBooth/master/trees.jpg'
url_snow  = 'https://raw.githubusercontent.com/filixgator/PhotoBooth/master/snow_flakes.jpg'
url_background = 'https://raw.githubusercontent.com/filixgator/PhotoBooth/master/background_1.jpg'
url_red_gradient = 'https://raw.githubusercontent.com/filixgator/PhotoBooth/master/colors.jpg'

last_photos = []
wrapping_paper = cv2.imread('trees.jpg', 1)
##wrapping_paper = url_to_image(url_trees)
stripes = wrapping_paper[130:295, 0:880].copy()
snow = cv2.imread('noche_buenas.jpg', 1)
##snow = url_to_image(url_background)
background = snow[0:1024,0:1280]

txt_mask = np.zeros((background.shape[0],background.shape[1]), np.uint8)
##mask_color = cv2.imread('red_gradient.jpg', 1)
mask_color = url_to_image(url_red_gradient)
mask_color = cv2.resize(mask_color, (1280, 1024))

font                   = cv2.FONT_HERSHEY_TRIPLEX
bottomLeftCornerOfText = (400,50)
fontScale              = 2
fontColor              = (255)
lineType               = 2

cv2.putText(txt_mask,'192.168.1.214', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

txt_mask_inv = cv2.bitwise_not(txt_mask)
background_1 = cv2.bitwise_and(background, background, mask=txt_mask_inv)
background_2 = cv2.bitwise_and(mask_color, mask_color, mask=txt_mask)
background = background_1 + background_2

filters = build_filters()

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
    background[75:900,200:1080] = img_stripes
    
    cv2.imshow("Posada FM", background)
##    cv2.imshow("Text Mask", txt_mask)

    k = cv2.waitKey(30)
    if k == 27:                  
        break
    elif k == -1:
        continue
    elif k == 32:
        pic_num = take_pic(photo, last_photos, stripes, wrapping_paper, pic_num, background)
##        requests.get(flash_on)
##        img_resp = requests.get()
##        requests.get(flash_off)
##        img_arr  = np.array(bytearray(img_resp.content), dtype=np.uint8)
##        img_4k = cv2.imdecode(img_arr, -1)
####        img_4k, gray_img = process_inhaler(img_4k, filters)
##        date_and_time = datetime.datetime.now().strftime("%I_%M_%p_%B_%d_%Y_")
##        cv2.imwrite(str(date_and_time) + str(pic_num) + ".jpg", img_4k)
##        pic_num += 1
##        if len(last_photos) >= 4:
##            del last_photos[:]
##            stripes = wrapping_paper[130:295, 0:880].copy()
##        last_photos.append(img_4k)
##        print(str(date_and_time) + str(pic_num) + ".jpg")
##        len(last_photos)
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
