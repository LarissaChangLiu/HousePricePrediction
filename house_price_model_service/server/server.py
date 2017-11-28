import numpy as np
import os
import pandas as pd
import pickle
import pyjsonrpc
import sys
import tensorflow as tf
import time

from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import linear_regression

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

PRICE_NORM_FACTOR = 100000

model = None


def loadModel():
    global model
    model = linear_regression.build_model(['from_api'])

loadModel()

print "Model loaded"

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print "Model update detected. Loading new model."
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        loadModel()


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def prediction(self, house):
        # # Run the model in prediction mode.
        print house
        input_dict = {
            "flooring": np.array([house['flooring']]),
            "fencing": np.array([house['fencing']]),
            "baths": np.array([house['baths']]),
            "beds": np.array([house['beds']]),
            "zip_code": np.array([house['zip_code']]),
            "built_yr": np.array([house['built_yr']]),
            "gutters": np.array([house['gutters']]),
            "sqft": np.array([house['sqft']])
        }
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            input_dict, shuffle=False)
        predict_results = model.predict(input_fn=predict_input_fn)
        for i, prediction in enumerate(predict_results):
            return PRICE_NORM_FACTOR * prediction["predictions"][0]
        
# Setup watchdog
observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting predicting server ..."
print "URL: http://" + str(SERVER_HOST) + ":" + str(SERVER_PORT)

http_server.serve_forever()