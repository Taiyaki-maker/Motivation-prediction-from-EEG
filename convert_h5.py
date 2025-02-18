#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:52:23 2024

@author: gonzaresu
"""
import os
import coremltools as ct
from tensorflow.keras.models import load_model

# ユーザーのホームディレクトリを取得
home_directory = os.path.expanduser("~")

# model.h5のパスを指定
model_path = os.path.join(home_directory, "Downloads", "fer_model_best.h5")

# Kerasモデルの読み込み
model = load_model(model_path)

'''

# CoreMLモデルに変換
coreml_model = ct.convert(model, inputs=[ct.ImageType(shape=(1, 48, 48, 1))])

# CoreMLモデルの保存
coreml_model.save('EmotionRecognition.mlmodel')

'''

import tensorflow as tf

# TensorFlow Liteモデルへの変換
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# TensorFlow Liteモデルの保存
with open('emotion_recognition.tflite', 'wb') as f:
    f.write(tflite_model)