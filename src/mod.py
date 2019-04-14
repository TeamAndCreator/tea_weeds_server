import os

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array

np.set_printoptions(precision=4)


class Tea(object):
    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "1"
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        tf.Session(config=config)
        self.model = load_model("model/mod.h5")
        self.label = pd.read_csv("data/name.csv", header=None)

    def preprocess_img(self, image):
        train_data = []  # 数据转码
        data = cv2.resize(image, (224, 224))
        data = img_to_array(data)
        data = data / 255.0
        train_data.append(data)
        train_data = np.array(train_data)
        return train_data

    def predict(self, image):
        image = self.preprocess_img(image)
        sign = self.model.predict(image)
        sign = [round(i, 4) for i in list(sign[0] * 100)]
        before = dict(zip(self.label[1], sign))
        after = dict(sorted(before.items(), key=lambda e: e[1], reverse=True))
        result = [{"name": key, "probability": value} for key, value in after.items()]
        return result


if __name__ == '__main__':
    model = Tea()
    data = cv2.imread('../data/image.JPG')  # 读取一张图片
    print(f"{data.shape}")
    model.predict(data)
