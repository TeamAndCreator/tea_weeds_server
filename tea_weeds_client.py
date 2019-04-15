#-*-coding:utf-8 -*-
import cv2
import grpc

from protos import tea_weeds_pb2_grpc, tea_weeds_pb2

_HOST = '127.0.0.1'
_PORT = 6007


def classifier():
    ip, port = _HOST, _PORT
    conn = grpc.insecure_channel("127.0.0.1:6007")
    client = tea_weeds_pb2_grpc.TeaWeedDetectStub(channel=conn)

    img = cv2.imread('data/image.JPG')  # 读取一张图片
    high, width, channel = img.shape
    # print(f"{len(img.tostring())}")
    image = tea_weeds_pb2.Image(raw_data=img.tostring(), width=width, high=high, channel=channel)
    reply = client.classifier(tea_weeds_pb2.DetectRequest(image=image))
    result = [{"name": result.name, "probability": result.probability} for result in reply.result]

    print(result)


if __name__ == '__main__':
    classifier()
