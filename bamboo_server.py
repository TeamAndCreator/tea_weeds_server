import os
import time
from concurrent import futures

import grpc
import tensorflow as tf

from logger import logger
from protos import tea_weeds_pb2_grpc, tea_weeds_pb2
from src import bamboo
import numpy as np

_GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", '192.168.16.18:6006')
_HOST = _GRPC_SERVER_ADDRESS.split(":")[0]
_PORT = int(_GRPC_SERVER_ADDRESS.split(":")[1])
_SERVER_NAME = "bamboo_detect"


class TeaWeedDetectService(object):
    def __init__(self):
        self.model = bamboo.Tea()
        self.graph = tf.get_default_graph()

    def classifier(self, request, context):
        image = np.fromstring(request.image.raw_data, dtype=np.uint8).reshape(request.image.high, request.image.width,
                                                                              request.image.channel)
        with self.graph.as_default():
            result_dict = self.model.predict(image)
            results = [tea_weeds_pb2.Result(name=dict["name"], probability=dict["probability"]) for dict in result_dict]
            return tea_weeds_pb2.DetectReply(result=results)


def tea_weeds_server(max_workers=10, port=_PORT):
    options = [('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', 100 * 1024 * 1024)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), options=options)
    tea_weeds_pb2_grpc.add_TeaWeedDetectServicer_to_server(TeaWeedDetectService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    logger.info("tea_weeds_server start success...")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    # register(_SERVER_NAME, _HOST, _PORT)
    tea_weeds_server()
