# mhxy
tensorflow实践：梦幻西游人物弹窗识别

## 环境描述
[Windows](https://www.microsoft.com/zh-cn/software-download/windows10)

```
C:\Users\SF>ver
Microsoft Windows [版本 10.0.18363.720]
```

[Python](https://www.python.org/downloads/)
```
C:\Users\SF>python --version
Python 3.7.6
```

[Tensorflow](https://www.tensorflow.org/install)
```
C:\Users\SF>python
Python 3.7.6 (tags/v3.7.6:43364a7ae0, Dec 19 2019, 00:42:30) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
2020-03-19 23:42:50.170828: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
>>> tf.__version__
'2.1.0'
```

[CUDA](https://developer.nvidia.com/cuda-downloads)
```
C:\Users\SF>nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Wed_Oct_23_19:32:27_Pacific_Daylight_Time_2019
Cuda compilation tools, release 10.2, V10.2.89

```

[cuDNN](https://developer.nvidia.com/cudnn)
```
C:\tools\cuda\include\cudnn.h

...
#define CUDNN_MAJOR 7

#define CUDNN_MINOR 6
#define CUDNN_PATCHLEVEL 5
#define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)
...
```

[梦幻西游](http://xyq.163.com/download/index.html?=xyqload)
```
启动方式   多标签版
分辨率     800x600
界面风格   暖风

```
![](https://github.com/BestBurning/mhxy/blob/master/images/github/mhxy_setting_1.jpg)
![](https://github.com/BestBurning/mhxy/blob/master/images/github/mhxy_setting_2.jpg)


## 运行

由于**鼠标点击**使用了[kmclassdll](https://github.com/BestBurning/kmclassdll)，所以需要开启 **测试模式** & **禁用强制驱动签名** 并 **重启**

`管理员身份`打开`CMD`
```
bcdedit /set nointegritychecks on

bcdedit /set testsigning on

shutdown  -r -t 0
```
重启后，`管理员身份`打开`CMD`

- 自动点击弹窗
```
python main.py --click 0
```

- 持续学习
```
python main.py --learn 0
```
如果使用`学习`功能的话，请下载[训练库](https://github.com/BestBurning/mhxy/releases)
更多代码解读可以参考[这里](https://di1shuai.com/tags/%E6%A2%A6%E5%B9%BB%E8%A5%BF%E6%B8%B8/)


## 成果展示

![](https://github.com/BestBurning/mhxy/blob/master/images/github/result.gif)

可以看到一次预测点击的耗时是在**4s**左右，欢迎**Star**

## 目录说明

- [driver](https://github.com/BestBurning/mhxy/blob/master/driver)  --  [kmclass键鼠驱动](https://github.com/BestBurning/kmclass)文件夹

- [images](https://github.com/BestBurning/mhxy/blob/master/images)  --  截图文件夹
  - [flag](https://github.com/BestBurning/mhxy/blob/master/images/flag)   -- 标识文件夹：战斗标识、鼠标标识、弹框标识 
  - [github](https://github.com/BestBurning/mhxy/blob/master/images/github)  -- github文件夹 
- [model](https://github.com/BestBurning/mhxy/blob/master/model)  --  tensorflow 模型文件夹

## 文件说明

- [auto_click.bat](https://github.com/BestBurning/mhxy/blob/master/auto_click.bat)   
运行弹框识别并点击的脚本

- [auto.py](https://github.com/BestBurning/mhxy/blob/master/auto.py)          
键鼠的包装

- [constant.py](https://github.com/BestBurning/mhxy/blob/master/constant.py)      
常量定义

- [data_model.py](https://github.com/BestBurning/mhxy/blob/master/data_model.py)    
模型训练、读取、预测

- [keymouse.py](https://github.com/BestBurning/mhxy/blob/master/keymouse.py)      
[kmclassdll](https://github.com/BestBurning/kmclassdll) 键鼠动态库调用

- [learn_clean.py](https://github.com/BestBurning/mhxy/blob/master/learn_clean.py)   
学习并清除学过的文件的脚本

- [main.py](https://github.com/BestBurning/mhxy/blob/master/main.py)          
程序入口

- [screen.py](https://github.com/BestBurning/mhxy/blob/master/screen.py)      
屏幕截图、图片处理相关

- [util.py](https://github.com/BestBurning/mhxy/blob/master/util.py)          
工具类  

## 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议