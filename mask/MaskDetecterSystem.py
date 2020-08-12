from cv2 import cv2
import time
import numpy as np
import pygame
import threading

#提醒1
def slogan_short():
    
    timeplay=1.5
    global playflag_short
    playflag_short=0
    while True:       
        if playflag_short==1:
            track = pygame.mixer.music.load(file_slogan_short)
            print("--------Please wear mask")
            pygame.mixer.music.play()
            time.sleep(timeplay)
            playflag_short=0
            
        time.sleep(0)
        #print("slogan_shorttread running")
#提醒2
def slogan():
    timeplay=18
    global playflag
    playflag=0
    while True:       
        if playflag==1:
            track = pygame.mixer.music.load(file_slogan)
            print("--------Please wear mask")
            pygame.mixer.music.play()
            time.sleep(timeplay)
            playflag=0
        time.sleep(0)
        #print("slogantread running")
def nothing(x):  # 滑动条的回调函数
    pass

#必要初始化
def facesdetecter_init():
    #多线程进行播放
    image=cv2.imread("E:/Onedrive/UIUC/Summer 2020/2020HackIllinois/SU2020HACKILLINOIS/code/images/backgound.jpg")
    cv2.imshow('skin',image)
    #滑动条
    cv2.createTrackbar("minH", "skin", 15, 180, nothing)
    cv2.createTrackbar("maxH", "skin", 25, 180, nothing)

#主要程序，识别特征，和比较肤色区域
def facesdetecter(image):
    #用于计算帧率
    start = time.time()#开始时间

    image=cv2.GaussianBlur(image,(5,5),0)#高斯滤波
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#将图片转化成灰度
    image2=image.copy()

    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)#将图片转化成HSV格式
    #cv2.imshow("hsv",hsv)#显示HSV图

    H,S,V=cv2.split(hsv)
    #cv2.imshow("hsv-H",H)#显示HSV图明度

    minH=cv2.getTrackbarPos("minH", 'skin')
    maxH=cv2.getTrackbarPos("maxH", 'skin')
    if minH>maxH:
        maxH=minH

    thresh_h=cv2.inRange(H,minH,maxH)#0-180du 提取人体肤色区域
    cv2.imshow("skin",thresh_h)#显示肤色图
    

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)#人脸检测
    eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)#眼睛检测
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)#画框标识脸部
    for (x,y,w,h) in eyes:
        frame = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)#画框标识眼部

    #
    #眼部区域和口罩部区域确定以及面积计算
    total_area_mask=0#口罩区域面积初始化
    total_area_eyes=0#口罩区域面积初始化

    #如果找到眼睛将进行区域确定和面积计算，确定区域方法就是左眼睛左上角和右眼睛右下角的框为眼部区域，往下两倍高度为口罩部
    if len(eyes)>1:

        #眼睛区域
        rect_eyes=[]  
        (x1,y1,w1,h1)=eyes[0]#即左眼坐标
        for (x,y,w,h) in eyes[1:]:            
            (x2,y2,w2,h2)=(x,y,w,h)
            rect_eyes.append((x1,y1,x2+w2-x1,y2+h2-y1))
            (x1,y1,w1,h1)=(x2,y2,w2,h2)

        for (x,y,w,h) in rect_eyes:
            frame = cv2.rectangle(image,(x,y),(x+w,y+h),(255,250,255),2)
            thresh_eyes=thresh_h[y:y+h,x:x+w]
            contours, hierarchy = cv2.findContours(thresh_eyes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #寻找前景 
            cv2.drawContours(image,contours,-1,(0,255,0),3)
            for cont in contours:
                Area = cv2.contourArea(cont)  # 计算轮廓面积           
                total_area_eyes+=Area
        print("total_area_eyes=",total_area_eyes)
        frame = cv2.putText(image,"Eyes Area : {:.3f}".format(total_area_eyes),(120,40),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)#绘制
         
        #口罩区域
        rect_mask=[(x,y+h,w,h*2)]
        for (x,y,w,h) in rect_mask:
            frame = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
            thresh_mask=thresh_h[y:y+h,x:x+w]
            #image2[y:y+h,x:x+w]=thresh_h
            contours, hierarchy = cv2.findContours(thresh_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #寻找前景 
            cv2.drawContours(image,contours,-1,(0,0,255),3)
            for cont in contours:
                Area = cv2.contourArea(cont)  # 计算轮廓面积           
                total_area_mask+=Area
        print("total_area_mask=",total_area_mask)
        frame = cv2.putText(image,"Mask Area : {:.1f}".format(total_area_mask),(120,80),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)#绘制
            
        #print("{}-prospect:{}".format(count,Area),end="  ") #打印出每个前景的面积

        #面积比较以及播放语音
        if total_area_eyes<total_area_mask:
            print("------------无口罩")
            global playflag_short
            playflag_short=1
            frame = cv2.putText(image,"NO MASK",(rect_eyes[0][0],rect_eyes[0][1]-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)#绘制
            

        if total_area_eyes>total_area_mask:
            global thread_slogan
            print("------------------戴口罩")
            global playflag
            playflag=1
            frame = cv2.putText(image,"HAVE MASK",(rect_eyes[0][0],rect_eyes[0][1]-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)#绘制
    
    #计算帧率
    end = time.time()#结束时间
    fps=1 / (end-start)#帧率
    frame = cv2.putText(image,"fps:{:.3f}".format(fps),(550,15),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)#绘制
      
    cv2.imshow("face",image)#显示最终图片
    #facesdetecter()函数结束


#语音提醒
file_slogan=r'radio/slogan.mp3'
file_slogan_short=r'radio/slogan_short.mp3'
pygame.mixer.init(frequency=16000, size=-16, channels=2, buffer=4096)

#脸部的识别非必须
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_cascade.load("E:/Onedrive/UIUC/Summer 2020/2020HackIllinois/SU2020HACKILLINOIS/code/data/haarcascades/haarcascade_frontalface_default.xml")#一定要告诉编译器文件所在的具体位置
'''此文件是opencv的haar人脸特征分类器'''

#主要还是通过眼睛位置进行区域判断
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
eyes_cascade.load("E:/Onedrive/UIUC/Summer 2020/2020HackIllinois/SU2020HACKILLINOIS/code/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml")#一定要告诉编译器文件所在的具体位置
'''此文件是opencv的haar眼镜特征分类器'''


if __name__ == '__main__':
    
    facesdetecter_init()#初始化
    capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ref,frame=capture.read()
        if ref==False:
            print("打开摄像头错误")
            break
        #等待30ms显示图像，若过程中按“Esc”退出
        c= cv2.waitKey(30) & 0xff 
        if c==27:
            capture.release()
            break

        cv2.imshow("framelive",frame)#摄像头实时视频
        facesdetecter(frame)#对视频检测

    cap.release()
    cv2.destroyAllWindows()