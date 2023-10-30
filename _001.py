#py -3.6 -m pip install opencv-python
##執行影像辨識需要的封裝包
#有numpy與opencv-python
#-----------------圖形辨識所需要的模塊-------
import numpy as np#引用numpy軟體包的np
import cv2        #引用opencv-python
import math
from math import *
from tkinter import StringVar
import tkinter as tk
#--------------------------------------------
#----------------使用效顯是所需要的模塊------
#import 
cap = cv2.VideoCapture(0)# 抓取鏡頭畫面
#鏡頭參數設定
cap.set(cv2.CAP_PROP_BRIGHTNESS, 230)#亮度


#min = 1
#max = 255
'''
        double brightness = 100;//亮度100
        double contrast = 255;//對比255
        double saturation = 255;//飽和度255
        double sharpness = 255;//清晰度
        //double whitebalanceb = 10000;//Notebook Deluxe白平衡藍
        /*C920白平衡無法透過程式碼控制
        //double whitebalancer = 4000;//白平衡紅
        //double temperature = 4000;//
        //float wb = 4000;
        */
        double backlight = 0;//背光度
        double gain = 255;//增益
        double zoom = 130;//縮放
        double focus = 0;//焦距
        double exposure = -8;//曝光
        double pan = 0;//取景位置調整
        double tilt = 0;//傾斜
'''
'''def do_nothing(x):
    pass
cv2.namedWindow('d')
cv2.createTrackbar('min','d',0,20,do_nothing)
cv2.createTrackbar('nor','d',0,255,do_nothing)
cv2.createTrackbar('max','d',0,255,do_nothing)
'''
temp,temp1,temp2 = 0,0,0
d1vt,d2vt,d3vt = 0,0,0
wk = 350
window = tk.Tk()
window.title("Resule")
window.geometry('200x100')
e1 = StringVar()
e2 = StringVar()
e3 = StringVar()
e1.set("0")
e2.set("0")
e3.set("0")
def res(d1,d2,d3):	
	e1.set(d1)
	e2.set(d2)
	e3.set(d3)
v1 = tk.Label(window,textvariable = e1)	
v1.pack()
v2 = tk.Label(window,textvariable = e2)	
v2.pack()
v3 = tk.Label(window,textvariable = e3)	
v3.pack()		
window.update()

while(True):
     
    ret, frame = cap.read()# 將鏡頭畫面顯示在"顯示畫面"上
#-----------------------------------------------------------骰子面值點數的計算過程--------------------------------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# 將畫面灰階化
    
    ret, threshold = cv2.threshold(gray,163,255,cv2.THRESH_BINARY)#二值化影像
         
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))#定義結構元素   
   
    erodeimg = cv2.erode(threshold,kernel,iterations=13) #侵蝕影像

    dilateimg = cv2.dilate(erodeimg,kernel,iterations=13)#膨脹影像

    ret, rimg = cv2.threshold(dilateimg, 163,255,cv2.THRESH_BINARY_INV)#對調影像的黑白色

    (_, cnts, _) = cv2.findContours(rimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#透過對調顏色的影像找輪廓

    clone = frame.copy()#複製主要
    clone1 = frame.copy()#複製主要
    clone2 = frame.copy()#複製主要
    b = len(cnts)#骰子的總數
       
    if b == 1:#一個骰子的時候
        a1 = cnts [0]     #骰子的外輪廓         
        x,y,w,h = cv2.boundingRect(a1)#透過骰子外輪廓定義矩形範圍的來源
        roiimg = clone[y:y+h,x:x+w]   #定義矩形範圍  
        rotret = cv2.minAreaRect(a1)  #透過骰子的外輪廓定義矩形的最小範圍
        box = cv2.boxPoints(rotret)#透過定義的最小範圍來找出四個頂點
        box1,box2,box3,box4 = box[0],box[1],box[2],box[3]#將骰子的四個頂點帶入各自的索引編號
        #----------------------------------------------------------------圖像旋轉--------------------------------------------------------              
        withRect = math.sqrt((box4[0] - box1[0]) ** 2 + (box4[1] - box1[1]) ** 2)  # 矩形框的寬度
        heightRect = math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) **2)  #矩形框的高度 
        angle = acos((box4[0] - box1[0]) / withRect) * (180 / math.pi)  # 矩形框旋轉的角度    
        height = roiimg.shape[0]  # 原始圖像高度
        width = roiimg.shape[1]   # 原始圖像寬度
        rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋轉圖像
        heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))#按angle、寬度的sin與高度的cos定義新的高度
        widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle)))) #按angle、高度的sin與寬度的cos定義新的寬度 
        rotateMat[0, 2] += (widthNew - width) / 2
        rotateMat[1, 2] += (heightNew - height) / 2
        imgRotation = cv2.warpAffine(roiimg, rotateMat, (widthNew, heightNew), borderValue = (255, 255, 255))#會透過修正的角度繪製新的圖像
        #---------------------------------------------------------------------------------------------------------------------------------
        grayimgRotation = cv2.cvtColor(imgRotation,cv2.COLOR_BGR2GRAY)#修正角度圖像的灰階化
        ret, thresholdimgRotation = cv2.threshold(grayimgRotation,196,255,cv2.THRESH_BINARY)#修正角度圖像的二值化
        erodeimgRotation = cv2.erode(thresholdimgRotation,kernel,iterations = 10)#修正角度圖像的侵蝕        
        ret, thresholdINVimgRotation = cv2.threshold(erodeimgRotation,196,255,cv2.THRESH_BINARY_INV)#修正角度圖像的黑白反轉
        clonethresholdINVimgRotation = thresholdINVimgRotation.copy()#複製修正角度圖像
        (_,d1f,_)=cv2.findContours(clonethresholdINVimgRotation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#修正角度圖像的外輪廓尋找             
        xa,ya,wa,ha = cv2.boundingRect(d1f[0])#修飾圖像大小的定義矩形範圍的來源
        roiimgRB = imgRotation[ya:ya+ha,xa:xa+wa]#依照矩行範圍來修飾圖像
        cloneroiimgRB = roiimgRB.copy()#複製修飾的圖像
        grayroiimgRB = cv2.cvtColor(cloneroiimgRB,cv2.COLOR_BGR2GRAY)#修飾圖像的灰階化
        ret,thresholdroiimgRB = cv2.threshold(grayroiimgRB,252,255,cv2.THRESH_BINARY_INV)#修飾圖像的二值化
        eroderoiimgRB = cv2.erode(thresholdroiimgRB,kernel,iterations= 1)#修飾圖像的侵蝕
        (_,d1v,_) = cv2.findContours(eroderoiimgRB,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE) #透過修飾修飾圖像的親時尋找內輪廓(點數)
        d1vt = str(len(d1v)-1) #定義面值的結果  
        res(d1vt,0,0)#將面值的結果會出至圖型視窗
#------------------------------------------------------------------------------------------------------------------------------------------
        cv2.imshow('1',eroderoiimgRB)
        cv2.imshow("orgimg",frame)  #顯示原本的圖像     
        cv2.waitKey(wk)#延遲多少時間更新一次畫面

    elif b == 2:#兩個骰子的時候
        a1 = cnts [0]
        a2 = cnts [1]       
        x,y,w,h = cv2.boundingRect(a1)#定義第一個矩形範圍的來源
        x1,y1,w1,h1 = cv2.boundingRect(a2)#定義第二個矩形範圍來源
        roiimg = clone[y:y+h,x:x+w]   #定義第一個矩形範圍    
        roiimg1 = clone[y1:y1+h1,x1:x1+w1]#定義第二個矩形範圍
        rotret = cv2.minAreaRect(a1)
        rotret1 = cv2.minAreaRect(a2)
        box = cv2.boxPoints(rotret)
        Box = cv2.boxPoints(rotret1)
        box1,box2,box3,box4 = box[0],box[1],box[2],box[3]
        box11,box12,box13,box14 = Box[0],Box[1],Box[2],Box[3]
        #--------第一個骰子圖像旋轉--------              
        withRect = math.sqrt((box4[0] - box1[0]) ** 2 + (box4[1] - box1[1]) ** 2)   #矩形框的寬度
        heightRect = math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) **2)  #矩形框的高度 
        angle = acos((box4[0] - box1[0]) / withRect) * (180 / math.pi)  # 矩形框旋轉角度    
        height = roiimg.shape[0]  # 原始圖像高度
        width = roiimg.shape[1]   # 原始圖像寬度
        rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋轉圖像
        heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
        widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))
        rotateMat[0, 2] += (widthNew - width) / 2
        rotateMat[1, 2] += (heightNew - height) / 2
        imgRotation = cv2.warpAffine(roiimg, rotateMat, (widthNew, heightNew), borderValue = (255, 255, 255))
        #----------------------------------
        #--------第二個骰子圖像旋轉--------              
        withRect1 = math.sqrt((box14[0] - box11[0]) ** 2 + (box14[1] - box11[1]) ** 2)   #矩形框的寬度
        heightRect1 = math.sqrt((box11[0] - box12[0]) ** 2 + (box11[1] - box12[1]) **2)  #矩形框的高度 
        angle1 = acos((box14[0] - box11[0]) / withRect1) * (180 / math.pi)  # 矩形框旋轉角度    
        height1 = roiimg.shape[0]  # 原始圖像高度
        width1 = roiimg.shape[1]   # 原始圖像寬度
        rotateMat1 = cv2.getRotationMatrix2D((width1 / 2, height1 / 2), angle1, 1)  # 按angle角度旋轉圖像
        heightNew1 = int(width1 * fabs(sin(radians(angle1))) + height1 * fabs(cos(radians(angle1))))
        widthNew1 = int(height1 * fabs(sin(radians(angle1))) + width1 * fabs(cos(radians(angle1))))
        rotateMat1[0, 2] += (widthNew1 - width1) / 2
        rotateMat1[1, 2] += (heightNew1 - height1) / 2
        imgRotation1 = cv2.warpAffine(roiimg1, rotateMat1, (widthNew1, heightNew1), borderValue = (255, 255, 255))
        #---------------------------------
        grayimgRotation = cv2.cvtColor(imgRotation,cv2.COLOR_BGR2GRAY)#骰子面值得灰階化
        grayimgRotation1 = cv2.cvtColor(imgRotation1,cv2.COLOR_BGR2GRAY)#骰子面值得灰階化
        ret, thresholdimgRotation = cv2.threshold(grayimgRotation,196,255,cv2.THRESH_BINARY)#面值得二值化248,255
        ret, thresholdimgRotation1 = cv2.threshold(grayimgRotation1,196,255,cv2.THRESH_BINARY)#面值得二值化248,255
        erodeimgRotation = cv2.erode(thresholdimgRotation,kernel,iterations = 10)#面值的侵蝕 
        erodeimgRotation1 = cv2.erode(thresholdimgRotation1,kernel,iterations = 10)#面值的侵蝕   
        ret, thresholdINVimgRotation = cv2.threshold(erodeimgRotation,196,255,cv2.THRESH_BINARY_INV)#反轉
        ret, thresholdINVimgRotation1 = cv2.threshold(erodeimgRotation1,196,255,cv2.THRESH_BINARY_INV)#反轉
        clonethresholdINVimgRotation = thresholdINVimgRotation.copy()
        clonethresholdINVimgRotation1 = thresholdINVimgRotation1.copy()
        (_,d1f,_)=cv2.findContours(clonethresholdINVimgRotation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#面值的輪廓尋找
        (_,d2f,_)=cv2.findContours(clonethresholdINVimgRotation1,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#面值的輪廓尋找
        
        xa,ya,wa,ha = cv2.boundingRect(d1f[0])#定義矩形範圍的來源
        xa1,ya1,wa1,ha1 = cv2.boundingRect(d2f[0])#定義矩形範圍的來源
        roiimgRB = imgRotation[ya:ya+ha,xa:xa+wa]
        roiimgRB1 = imgRotation1[ya1:ya1+ha1,xa1:xa1+wa1]
        cloneroiimgRB = roiimgRB.copy()
        cloneroiimgRB1 = roiimgRB1.copy()
        grayroiimgRB = cv2.cvtColor(cloneroiimgRB,cv2.COLOR_BGR2GRAY)
        grayroiimgRB1 =cv2.cvtColor(cloneroiimgRB1,cv2.COLOR_BGR2GRAY)
        ret,thresholdroiimgRB = cv2.threshold(grayroiimgRB,252,255,cv2.THRESH_BINARY_INV)
        ret,thresholdroiimgRB1 = cv2.threshold(grayroiimgRB1,252,255,cv2.THRESH_BINARY_INV)
        eroderoiimgRB = cv2.erode(thresholdroiimgRB,kernel,iterations = 1)
        eroderoiimgRB1 = cv2.erode(thresholdroiimgRB1,kernel,iterations = 1)
        (_,d1v,_) = cv2.findContours(eroderoiimgRB,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        (_,d2v,_) = cv2.findContours(eroderoiimgRB1,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        d1vt = str(len(d1v)-1)#第一個骰子面值的結果        
        d2vt = str(len(d2v)-1)#第二個骰子面值的結果 
        res(d1vt,d2vt,0)

        #print(d1vt,d2vt)

        cv2.imshow('1',eroderoiimgRB)
        cv2.imshow('2',eroderoiimgRB1)
        cv2.imshow("orgimg",frame)
        cv2.waitKey(wk)

    elif b == 3:#三個骰子的時候
        a1 = cnts [0]
        a2 = cnts [1]
        a3 = cnts [2]        
        x,y,w,h = cv2.boundingRect(a1)#定義第一個矩形範圍的來源
        x1,y1,w1,h1 = cv2.boundingRect(a2)#定義第二個矩形範圍來源
        x2,y2,w2,h2 = cv2.boundingRect(a3)#定義第三個矩形範圍的來源
        roiimg = clone[y:y+h,x:x+w]   #定義第一個矩形範圍    
        roiimg1 = clone[y1:y1+h1,x1:x1+w1]#定義第二個矩形範圍
        roiimg2 = clone[y2:y2+h2,x2:x2+w2]#定義第三個矩形範圍        
        rotret = cv2.minAreaRect(a1)
        rotret1 = cv2.minAreaRect(a2)
        rotret2 = cv2.minAreaRect(a3)
        box = cv2.boxPoints(rotret)
        Box = cv2.boxPoints(rotret1)
        bOx = cv2.boxPoints(rotret2)
        box1,box2,box3,box4 = box[0],box[1],box[2],box[3]
        box11,box12,box13,box14 = Box[0],Box[1],Box[2],Box[3]
        box21,box22,box23,box24 = bOx[0],bOx[1],bOx[2],bOx[3]
        #--------第一個骰子圖像旋轉--------              
        withRect = math.sqrt((box4[0] - box1[0]) ** 2 + (box4[1] - box1[1]) ** 2)  # 矩形框的寬度
        heightRect = math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) **2)  #矩形框的高度 
        angle = acos((box4[0] - box1[0]) / withRect) * (180 / math.pi)  # 矩形框旋轉角度    
        height = roiimg.shape[0]  # 原始圖像高度
        width = roiimg.shape[1]   # 原始圖像寬度
        rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋轉圖像
        heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
        widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))
        rotateMat[0, 2] += (widthNew - width) / 2
        rotateMat[1, 2] += (heightNew - height) / 2
        imgRotation = cv2.warpAffine(roiimg, rotateMat, (widthNew, heightNew), borderValue = (255, 255, 255))
        #----------------------------------
        #--------第二個骰子圖像旋轉--------              
        withRect1 = math.sqrt((box14[0] - box11[0]) ** 2 + (box14[1] - box11[1]) ** 2)  # 矩形框的寬度
        heightRect1 = math.sqrt((box11[0] - box12[0]) ** 2 + (box11[1] - box12[1]) **2)  #矩形框的高度 
        angle1 = acos((box14[0] - box11[0]) / withRect1) * (180 / math.pi)  # 矩形框旋轉角度    
        height1 = roiimg1.shape[0]  # 原始圖像高度
        width1 = roiimg1.shape[1]   # 原始圖像寬度
        rotateMat1 = cv2.getRotationMatrix2D((width1 / 2, height1 / 2), angle1, 1)  # 按angle角度旋轉圖像
        heightNew1 = int(width1 * fabs(sin(radians(angle1))) + height1 * fabs(cos(radians(angle1))))
        widthNew1 = int(height1 * fabs(sin(radians(angle1))) + width1 * fabs(cos(radians(angle1))))
        rotateMat1[0, 2] += (widthNew1 - width1) / 2
        rotateMat1[1, 2] += (heightNew1 - height1) / 2
        imgRotation1 = cv2.warpAffine(roiimg1, rotateMat1, (widthNew1, heightNew1), borderValue = (255, 255, 255))
        #---------------------------------
        #--------第三個骰子圖像旋轉--------              
        withRect2 = math.sqrt((box24[0] - box21[0]) ** 2 + (box24[1] - box21[1]) ** 2)  # 矩形框的寬度
        heightRect2 = math.sqrt((box21[0] - box22[0]) ** 2 + (box21[1] - box22[1]) **2)  #矩形框的高度 
        angle2 = acos((box24[0] - box21[0]) / withRect2) * (180 / math.pi)  # 矩形框旋轉角度    
        height2 = roiimg2.shape[0]  # 原始圖像高度
        width2 = roiimg2.shape[1]   # 原始圖像寬度
        rotateMat2 = cv2.getRotationMatrix2D((width2 / 2, height2 / 2), angle2, 1)  # 按angle角度旋轉圖像
        heightNew2 = int(width * fabs(sin(radians(angle2))) + height2 * fabs(cos(radians(angle2))))
        widthNew2 = int(height * fabs(sin(radians(angle2))) + width2 * fabs(cos(radians(angle2))))
        rotateMat2[0, 2] += (widthNew2 - width2) / 2
        rotateMat2[1, 2] += (heightNew2 - height2) / 2
        imgRotation2 = cv2.warpAffine(roiimg2, rotateMat2, (widthNew2, heightNew2), borderValue = (255, 255, 255))
        #----------------------------------
        grayimgRotation = cv2.cvtColor(imgRotation,cv2.COLOR_BGR2GRAY)#骰子面值得灰階化
        grayimgRotation1 = cv2.cvtColor(imgRotation1,cv2.COLOR_BGR2GRAY)#骰子面值得灰階化
        grayimgRotation2 = cv2.cvtColor(imgRotation2,cv2.COLOR_BGR2GRAY)#骰子面值得灰階化
        ret, thresholdimgRotation = cv2.threshold(grayimgRotation,196,255,cv2.THRESH_BINARY)#面值得二值化248,255
        ret, thresholdimgRotation1 = cv2.threshold(grayimgRotation1,196,255,cv2.THRESH_BINARY)#面值得二值化248,255
        ret, thresholdimgRotation2 = cv2.threshold(grayimgRotation2,196,255,cv2.THRESH_BINARY)#面值得二值化248,255
        erodeimgRotation = cv2.erode(thresholdimgRotation,kernel,iterations = 10)#面值的侵蝕 
        erodeimgRotation1 = cv2.erode(thresholdimgRotation1,kernel,iterations = 10)#面值的侵蝕
        erodeimgRotation2 = cv2.erode(thresholdimgRotation2,kernel,iterations = 10)#面值的侵蝕
        ret, thresholdINVimgRotation = cv2.threshold(erodeimgRotation,196,255,cv2.THRESH_BINARY_INV)#反轉
        ret, thresholdINVimgRotation1 = cv2.threshold(erodeimgRotation1,196,255,cv2.THRESH_BINARY_INV)#反轉
        ret, thresholdINVimgRotation2 = cv2.threshold(erodeimgRotation2,196,255,cv2.THRESH_BINARY_INV)#反轉
        clonethresholdINVimgRotation = thresholdINVimgRotation.copy()
        clonethresholdINVimgRotation1 = thresholdINVimgRotation1.copy()
        clonethresholdINVimgRotation2 = thresholdINVimgRotation2.copy()
        (_,d1f,_)=cv2.findContours(clonethresholdINVimgRotation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#面值的輪廓尋找
        (_,d2f,_)=cv2.findContours(clonethresholdINVimgRotation1,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#面值的輪廓尋找
        (_,d3f,_)=cv2.findContours(clonethresholdINVimgRotation2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#面值的輪廓尋找		
        xa,ya,wa,ha = cv2.boundingRect(d1f[0])#定義矩形範圍的來源
        xa1,ya1,wa1,ha1 = cv2.boundingRect(d2f[0])#定義矩形範圍的來源
        xa2,ya2,wa2,ha2 = cv2.boundingRect(d3f[0])#定義矩形範圍的來源
        roiimgRB = imgRotation[ya:ya+ha,xa:xa+wa]
        roiimgRB1 = imgRotation1[ya1:ya1+ha1,xa1:xa1+wa1]
        roiimgRB2 = imgRotation2[ya2:ya2+ha2,xa2:xa2+wa2]
        cloneroiimgRB = roiimgRB.copy()
        cloneroiimgRB1 = roiimgRB1.copy()
        cloneroiimgRB2 = roiimgRB2.copy()
        grayroiimgRB = cv2.cvtColor(cloneroiimgRB,cv2.COLOR_BGR2GRAY)
        grayroiimgRB1 = cv2.cvtColor(cloneroiimgRB1,cv2.COLOR_BGR2GRAY)
        grayroiimgRB2 = cv2.cvtColor(cloneroiimgRB2,cv2.COLOR_BGR2GRAY)
        ret,thresholdroiimgRB = cv2.threshold(grayroiimgRB,252,255,cv2.THRESH_BINARY_INV)
        ret,thresholdroiimgRB1 = cv2.threshold(grayroiimgRB1,252,255,cv2.THRESH_BINARY_INV)
        ret,thresholdroiimgRB2 = cv2.threshold(grayroiimgRB2,252,255,cv2.THRESH_BINARY_INV)
        eroderoiimgRB = cv2.erode(thresholdroiimgRB,kernel,iterations = 1)
        eroderoiimgRB1 = cv2.erode(thresholdroiimgRB1,kernel,iterations = 1)
        eroderoiimgRB2 = cv2.erode(thresholdroiimgRB2,kernel,iterations = 1)
        (_,d1v,_) = cv2.findContours(eroderoiimgRB,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        (_,d2v,_) = cv2.findContours(eroderoiimgRB1,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        (_,d3v,_) = cv2.findContours(eroderoiimgRB2,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        d1vt = str(len(d1v)-1)#第一個骰子面值的結果
        d2vt = str(len(d2v)-1)#第二個骰子面值的結果        
        d3vt = str(len(d3v)-1)#第三個骰子面值的結果   
        res(d1vt,d2vt,d3vt)	
        #print(d1vt,d2vt,d3vt)

        cv2.imshow('1',eroderoiimgRB)
        cv2.imshow('2',eroderoiimgRB1)
        cv2.imshow('3',eroderoiimgRB2)
        cv2.imshow("orgimg",frame)
        cv2.waitKey(wk)
   
# When everything done, release the capture


cap.release()
cv2.destroyAllWindows()

#筆記
#mask = np.zeros(rimg.shape, dtype="uint8")  #依Contours圖形建立mask
#cv2.drawContours(mask, a1,-1, 255, fillbool) #255→白色, -1→塗滿  
#root.update()
#erodeimg = cv2.erode(threshold,kernel,iterations=13) #前面不用加ret,
#ret, rimg = cv2.threshold(dilateimg, 163,255,cv2.THRESH_BINARY_INV)#後面的INV為反轉影像顏色
'''
 #滑桿
    min = cv2.getTrackbarPos('min','d')
    nor = cv2.getTrackbarPos('nor','d')
    max = cv2.getTrackbarPos('max','d')
'''