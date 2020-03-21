# -*- coding: utf-8 -*-
##########################
####    图片处理相关   ####
##########################

import win32gui
import shutil
import io
import sys
import os
import time
from skimage.metrics import structural_similarity
import cv2 as cv
from PIL import Image
from PyQt5.QtWidgets import QApplication
import constant as c
import util
import numpy as np
from matplotlib import pyplot as plt
#######
#######


hwnd_title = dict()


########
########

def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})


def dir_check():
    util.log_title('文件夹检查')
    dir_List = [
        c.img_dir_path,c.flag_dir_path,c.sub_dir_path,c.data_dir_path,
        c.train_dir,c.front_img_dir,c.others_img_dir,c.new_front_img_dir,c.new_others_img_dir
        ];
    for path in dir_List:
        dir_create(path)
        print(f'\t{path}\t\tok')
    return True


def dir_create(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'文件夹创建 -> {path}')


def time_str():
    localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #系统当前时间年份
    year=time.strftime('%Y',time.localtime(time.time()))
    #月份
    month=time.strftime('%m',time.localtime(time.time()))
    #日期
    day=time.strftime('%d',time.localtime(time.time()))
    #具体时间 小时分钟毫秒
    mdhms=time.strftime('%m%d%H%M%S',time.localtime(time.time()))
    return f'{year}_{month}_{day}_{mdhms}'



def shot():
    util.log_title('截图')
    win32gui.EnumWindows(get_all_hwnd, 0)
    mhxy_title = ''
    for h,t in hwnd_title.items():
        if t.startswith('梦幻西游 ONLINE'):
            mhxy_title = t
            print(mhxy_title)
            hwnd = win32gui.FindWindow(None, mhxy_title)
            app = QApplication(sys.argv)
            desktop_id = app.desktop().winId()
            screen = QApplication.primaryScreen()
            img_desk = screen.grabWindow(desktop_id).toImage()
            img_sc = screen.grabWindow(hwnd).toImage()
            img_desk.save(c.img_desktop_path)
            img_sc.save(c.img_sc_path)
            print(f'img_desktop save to -> {os.path.abspath(c.img_desktop_path)}')
            print(f'img_mhxy save to -> {os.path.abspath(c.img_sc_path)}')
    if mhxy_title == '':
        print('mhxy not start')
        return False
    return True

## 相似性判断
def compare_image(path_image1, path_image2):

    imageA = cv.imread(path_image1)
    imageB = cv.imread(path_image2)
    grayA = cv.cvtColor(imageA, cv.COLOR_BGR2GRAY)
    grayB = cv.cvtColor(imageB, cv.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(grayA, grayB, full=True)
    print("SSIM: {}".format(score))
    return score


## 战斗截图
def fight_crop():
    util.log_title('战斗标识截图')
    return crop(c.img_sc_path,c.fighting_img_path,c.fight_shape)


## 战斗标识截图
def fight_flag_crop():
    return crop(c.img_sc_path,c.fighting_flag_img_path,c.fight_shape)



#### 是否在战斗
def is_fight():
    util.log_title('状态判断')
    rate = compare_image(c.fighting_flag_img_path,c.fighting_img_path)
    if rate > 0.95:
        print('战斗 状态')
        return True
    else:
        print('非战斗 状态')
        return False


#### 图片检查
def image_check(img_path,size):
    util.log_title('截图检查')
    with Image.open(img_path) as img:
        if img.size == size:
            print(f'\t\tsize={size}\t\tok')
            return True
    print('Imgae Size Error')
    return False
            

### 弹窗判断
# 是  切分出包含4人物大图  360 * 120
# 否  False 
def popup_sub_crop():
    util.log_title('弹窗判断')
    shape_dict = {} 
    for i in range(len(c.popup_flag_img_paths)):
        shape,score = template_match(c.popup_flag_img_paths[i],c.img_sc_path)
        shape_dict[shape] = (score,i)
    
    print(shape_dict)
    max_shape = max(shape_dict, key=shape_dict.get)
    score,i = shape_dict[max_shape]
    print(f'最大区域 {max_shape} 最终得分为 {score}' )
    if score >=3 :
        sub_shape = (
            max_shape[0]+c.popup_move_shapes[i][0],
            max_shape[1]+c.popup_move_shapes[i][1],
            max_shape[2]+c.popup_move_shapes[i][2],
            max_shape[3]+c.popup_move_shapes[i][3]
        )
        print(f'弹框区域  {sub_shape}')
        return crop(c.img_sc_path,c.popup_sub_img_path,sub_shape)
    print(f'没有弹框')
    return False


#### 裁剪
def crop(source_path,target_path,shape):
    with Image.open(source_path) as img:

        fighting_flag_img = img.crop(shape)
        fighting_flag_img.save(target_path)
        return True    


#### 匹配
def template_match(template_path,src_path):

    
    img = cv.imread(src_path,0)
    img2 = img.copy()
    template = cv.imread(template_path,0)
    w, h = template.shape[::-1]
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED','cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    shape_dict = {}
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)  
        shape = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
        if shape_dict.get(shape) == None:
            shape_dict[shape] = 1;
        else:
            shape_dict[shape] = shape_dict[shape]+1        
        max_shape = max(shape_dict, key=shape_dict.get)
    return max_shape,shape_dict[max_shape]

### 根据index返回对应 图片在桌面的中心点
def find_xy_indesktop(template_path):
    util.log_title('坐标查找')
    shape,score = template_match(template_path,c.img_desktop_path)
    print(f'最高得分区域 {shape} 得分为 {score}')
    if score >= 3:
        x = (shape[2]+shape[0])//2
        y = (shape[3]+shape[1])//2
        print(f'中心点坐标为 {(x,y)}')
        return x,y
    else:
        print(f'所有区域得分均小于3，匹配失败')
        return 0,0
#### 
def find_mouse_in_desktop():    
    img = cv.imread(c.img_desktop_path,0)
    img2 = img.copy()
    template = cv.imread(c.mouse_flag_img_path,0)
    w, h = template.shape[::-1]
    
    img = img2.copy()
    shape_list = []
    threshold = 0.85
    res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    x = 10000
    y = 10000
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (top_left[0] + w, top_left[1] + h)  
        shape = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
        shape_list.append(shape)
        new_x = (shape[2]+shape[0])//2
        if new_x < x :        
            x = new_x
            y = (shape[3]+shape[1])//2

    print(f'中心点坐标为 {(x,y)}')
    return x,y


### 切成4份 360 * 120   ->    4  *  (90*120)
def crop_4():
    util.log_title('弹窗人物切分')
    w = 90
    h = 120
    for i in range(len(c.crop_4_img_names)):
        shape = (w*i, 0, w*(i+1), h)
        crop(c.popup_sub_img_path,c.crop_4_img_paths[i],shape)


###  数据保存
def save_data_img(front_index):
    for i in range(len(c.crop_4_img_paths)):
        save_path = ''
        if i == front_index:
            save_path = os.path.join(c.new_front_img_dir,time_str()+'_'+str(i)+'.jpg')
        else:
            save_path = os.path.join(c.new_others_img_dir,time_str()+'_'+str(i)+'.jpg')
        shutil.copyfile(c.crop_4_img_paths[i],save_path)

### 
def move_new_to_train():
    move_file(c.new_front_img_dir,c.front_img_dir)
    move_file(c.new_others_img_dir,c.others_img_dir)

def move_file(src_path,target_path):
    file_list=os.listdir(src_path)
    if len(file_list)>0:
        for file in file_list:
            shutil.move(
                os.path.join(src_path,file),
                os.path.join(target_path,file)
                )   
    print(f'{src_path} -> {target_path} 完毕')
####################################
####################################


def task():

    print()
    if shot():                                                          ## 截图
        if image_check(c.img_sc_path,c.screen_size):                    ## 检查截图大小
            fight_crop()                                                ## 战斗标识截图
            if is_fight():                                              ## 判断是否在战斗
                if popup_sub_crop():                                    ## 弹窗识别 与 人物区域切出
                    if image_check(c.popup_sub_img_path,c.sub_size):    ## 弹窗人物截图检查
                        crop_4()                                        ## 弹窗人物切分                   
                        print()
                        return True
    return False


if __name__ == '__main__':
    dir_check()