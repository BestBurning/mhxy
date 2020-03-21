# -*- coding: utf-8 -*-
import os

# 截图存档目录
img_dir_path = r'images'
flag_dir_path = r'images/flag'
sub_dir_path = r'images/sub'
data_dir_path = r'images/data'

model_dir_path = r'model'

driver_dir_path = r'driver'
##############

### images
img_sc_name = 'mhxy.jpg'
img_sc_path = os.path.join(img_dir_path,img_sc_name)

img_desktop_name = 'desktop.jpg'
img_desktop_path = os.path.join(img_dir_path,img_desktop_name)


### images/data/
train_dir = os.path.abspath(data_dir_path+'/train')
validation_dir = data_dir_path+'/validation'
new_dir_path = os.path.abspath(data_dir_path+'/new')

front_img_dir = os.path.join(train_dir,'front')
others_img_dir = os.path.join(train_dir,'others')

new_front_img_dir = os.path.abspath(new_dir_path+'/front')
new_others_img_dir = os.path.abspath(new_dir_path+'/others')

### model/
model_path = os.path.join(model_dir_path,'mhxy.h5')


### images/sub
fight_shape = (793,182,805,436)
fighting_img_name = 'fighting.jpg'
fighting_img_path =  os.path.join(sub_dir_path,fighting_img_name)


popup_sub_img_path = os.path.join(sub_dir_path,'pop_sub.jpg')


crop_4_img_names = ['1.jpg','2.jpg','3.jpg','4.jpg']
crop_4_img_paths = [ os.path.join(sub_dir_path,crop_4_img_name) for crop_4_img_name in crop_4_img_names ]

### images/flag

fighting_flag_img_name = 'fighting_flag.jpg'
fighting_flag_img_path = os.path.join(flag_dir_path,fighting_flag_img_name)


popup_flag_img_names = ['popup_flag_1.jpg','popup_flag_2.jpg']

popup_flag_img_paths = [ os.path.join(flag_dir_path,popup_flag_img_name) for popup_flag_img_name in popup_flag_img_names ]


mouse_flag_img_name = 'mouse_flag.jpg'
mouse_flag_img_path = os.path.join(flag_dir_path,mouse_flag_img_name)



### driver

driver_name = 'kmclass'

kmclass_dll_path = os.path.abspath(driver_dir_path+'/kmclassdll.dll').replace('\\','\\\\')

kmclass_driver_path = os.path.abspath(driver_dir_path+'/kmclass.sys').replace('\\','\\\\')


## 截图大小
screen_size = (812,663)
sub_size = (360,120)


### 移动偏移
## 弹框偏移
popup_move_shapes = [(-84,33,96,140),(-82,29,182,135)]

## 鼠标偏移
mouse_move_shape = (16,15)



if __name__ == '__main__':
    print('ok')
    print(kmclass_driver_path)