# -*- coding: utf-8 -*-
##########################
####    程序入口      ####
##########################


import screen as sc
import util
import constant as c
import time
import auto
import data_model as dm
import os
import argparse

###  将新图加入训练集 并 训练模型
def move_learn():
    sc.dir_check()
    util.log_title('图片朝向确认')
    confirm = input(f'请确认路径  {os.path.abspath(c.new_front_img_dir)}   下图片朝向均为  > 前 <  : (确认后输入 Y , 输入其他退出) ')
    if confirm == 'Y' or confirm == 'y':
        confirm = input(f'请确认路径  {os.path.abspath(c.new_others_img_dir)}   下图片朝向均为  > 左 右 后 < : (确认后输入 Y , 输入其他退出)')
        if confirm == 'Y' or confirm == 'y':
            util.log_h1_start('开始')
            sc.move_new_to_train()
            dm.base()               
    util.log_h1_end('结束')

### 自动点击弹框
def auto_click():
    util.log_h1(f'前置准备')
    if sc.dir_check():
        auto.open_driver()
        dm.model_load()
        while(True):
            util.log_h1_start(f'开始')
            start_time = time.time()
            if sc.task():
                min_index = dm.model_predict(c.crop_4_img_paths)
                sc.save_data_img(min_index)
                target_x , target_y = sc.find_xy_indesktop(c.crop_4_img_paths[min_index])
                if target_x == 0 and target_y == 0:
                    util.log_title('匹配失败')
                else:
                    auto.move_to(target_x,target_y)
                    if sc.shot():
                        now_x,now_y =  sc.find_mouse_in_desktop()
                        move_x = target_x-now_x+c.mouse_move_shape[0]
                        move_y = target_y-now_y+c.mouse_move_shape[1]
                        auto.move_rel_click(move_x, move_y)
            end_time = time.time()
            cost_time = end_time - start_time
            util.log_h1_end(f'结束 耗时 %.3f' % cost_time)
            time.sleep(3)



parser = argparse.ArgumentParser()

parser.add_argument("--click", help="Auto Click", type=int)
parser.add_argument("--learn", help="Lean Clean", type=int)

args = parser.parse_args()

if args.click:
    auto_click()

if args.learn:
    move_learn()


if __name__ == '__main__':
    print('Bye~')
