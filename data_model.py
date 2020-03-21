# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
AUTOTUNE = tf.data.experimental.AUTOTUNE

import os
import numpy as np
import matplotlib.pyplot as plt
import math
from util import log_title as t
import constant as c


###################
def sumNum(dir_path):
    num = 0
    for lb in os.listdir(dir_path):
        for im_name in os.listdir(os.path.join(dir_path,lb)):
            num += 1
    return num

###################

total_train = None
total_val = None
batch_size = 128
epochs = None
IMG_HEIGHT = 100
IMG_WIDTH = 100
train_data_gen = None
val_data_gen = None
model = None

#######################


    
def count():
    t('统计')
    global total_train, total_val, epochs
    total_train = sumNum(c.train_dir)
    total_val = sumNum(c.validation_dir)
    epochs = math.ceil(total_train/batch_size)
    print('训练集标签 :',os.listdir(c.train_dir))
    print('训练集图片个数 :' , total_train)
    print("验证集个数 :", total_val)
    print(f'每批次训练个数: {batch_size}, 共要进行 {epochs} 轮训练')
    if total_train == 0:
        print('样本为0 无法训练')
        return False
    return True

def data_generator():
    t('数据生成器')
    global train_data_gen,val_data_gen

    train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
    validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

    train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=c.train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')
    val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=c.validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')

def model_summary():
    t('模型编译统计')
    global model 
    model = Sequential([
        Conv2D(16, (3,3), padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3,3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3,3), padding='same', activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
    model.summary()

def model_fit():
    t('开始训练')

    global model,epochs,train_data_gen,total_train,batch_size,val_data_gen,total_val

    history = model.fit_generator(
        train_data_gen,
        steps_per_epoch=total_train // batch_size,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val // batch_size
    )
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss=history.history['loss']
    val_loss=history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

def model_save():
    t('模型保存')
    global model
    model.save(c.model_path)
    print(f'model save -> {c.model_path}')

def model_load():
    t('模型读取')
    print(c.model_path)
    global model
    model = keras.models.load_model(c.model_path)
    model.summary()

def model_predict(paths):
    t('模型预测')
    global model
    imgs = [load_and_preprocess_image(path) for path in paths]
    imgs =  tf.convert_to_tensor(imgs)
    predictions = model.predict(imgs)
    predictions = [row[0] for row in predictions]
    print(predictions)
    min_index = predictions.index(min(predictions))
    print(f' 预测结果为 第 > {min_index + 1} < 张图片')
    return min_index

def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize(image, [IMG_WIDTH, IMG_HEIGHT])
  image /= 255.0  # normalize to [0,1] range
  return image

def load_and_preprocess_image(path):
  image = tf.io.read_file(path)
  return preprocess_image(image)

def base():
    if count():
        data_generator()
        model_summary()
        model_fit()
        model_save()
        return True


def load_fit_save():
    if count():
        data_generator()
        model_load()
        model_fit()
        model_save()
        return True
    return False
    
if __name__ == '__main__':
    # base()
    # model_load()
    # model_predict(c.crop_4_img_paths)
    t('结束')