import sys
import numpy as np
import cv2
import pytesseract
import os
from django.conf import settings
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','todoapp.settings')
#import django
#django.setup()

#from todolist.models import Ocr
#좌측상단부터 반시계방향으로 0,1,2,3번 좌표
def reorderPts(pts):
    idx=np.lexsort((pts[:,1], pts[:, 0 ]))# 칼럼 0 --> 칼럼 1 순으로 정렬한 인덱스를 반환
    pts=pts[idx] # x 좌표로 정렬(idx순서대로 정렬)
    if pts[0, 1]> pts[1, 1]:
        pts[[0,1]]=pts[[1,0]]

    if pts[2, 1]< pts[3, 1]:
        pts[[2,3]]=pts[[3,2]]
    return pts

# 추출 text 저장 함수
def strToTxt(txtName, outText):
    with open('C:/deep/opencv/image/'+ txtName + '.txt', 'w', encoding='utf-8') as f:
        f.write(outText)
        f.close()

def readcontents():
    text = open('C:/deep/opencv/image/20201029.txt', 'r', encoding='utf-8')
    data = text.read()
    print(data)
    text.close

def opencv_ocr(path):
    src=cv2.imread(path,1) #src = cv2.imread(path, cv2.IMREAD_COLOR)
    #src=cv2.resize(src, (420,600))

    dw, dh= 600, 400 #원래 720, 400
    srcQuad=np.array([[0,0],[0,0],[0,0],[0,0]],np.float32)
    dstQuad=np.array([[0,0],[0,dh],[dw,dh],[dw,0]], np.float32)#좌측상단부터 반시계방향
    dst=np.zeros((dh,dw), np.uint8)

    src_gray=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    th, src_bin=cv2.threshold(src_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #외곽선 검출
    contours, _ =cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for pts in contours:
        #너무 작은 객체 제외
        if cv2.contourArea(pts) < 1000:
            continue
        #외곽선 근사화
        approx=cv2.approxPolyDP(pts, cv2.arcLength(pts, True)* 0.02, True)
        #컨벡스가 아니면 제외
        if not cv2.isContourConvex(approx) or len(approx) != 4:
            continue
        srcQuad=reorderPts(approx.reshape(4, 2).astype(np.float32))
        pers=cv2.getPerspectiveTransform(srcQuad, dstQuad)
        dst=cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)
        dst_rgb=cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        # print(pytesseract.image_to_string(dst_rgb, lang='Hangul+eng'))
        custom_config = r'--oem 3 --psm 6' #psm 6 아니면 11
        outText=pytesseract.image_to_string(dst_rgb, lang='Hangul+eng+kor', config=custom_config) #lang='Hangul+eng'
        return outText



        
    



    #cv2.imwrite(path, src)

#cv2.imshow('src', src)
#cv2.imshow('dst', dst)
#cv2.waitKey()
#cv2.destroyAllWindows()