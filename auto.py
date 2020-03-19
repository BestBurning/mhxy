# -*- coding: utf-8 -*-
##########################
####    键鼠包装   ####
##########################

import os
import pyautogui
import random
from util import log_title as t
import time
import keymouse as km

pyautogui.PAUSE = random.random()/3
pyautogui.FAILSAFE = False           # 启用自动防故障功能


def open_driver():
    km.load_driver()
    
def move_to_click(x,y):
    t('绝对移动 点击')
    move_to(x,y)
    time.sleep(random.random()/21)
    km._left_button_down()
    time.sleep(random.random()/5)
    km._left_button_up()

def move_rel_click(x,y):
    t('相对移动 点击')
    move_rel(x,y)
    time.sleep(random.random()/20)
    km._left_button_down()
    time.sleep(random.random()/5)
    km._left_button_up()


def move_to(x,y):
    print(f'move to - > {(x,y)}')
    pyautogui.moveTo(x,y,duration=random.random()/2)

def move_rel(x,y):
    print(f'move rel - > {(x,y)}')
    pyautogui.moveRel(x,y,duration=random.random()/2)

	

if __name__ == '__main__':
    open_driver()
    move_to_click(341,437)