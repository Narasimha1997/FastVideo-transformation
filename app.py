
from flask import Flask, request, jsonify, render_template, Response
from modules.image_queue import ImageQueue
from modules.preprocessor import Preprocessor, consumer
from modules.features import FeatureGenerator
from modules.runner import PyThread as pythread
from modules.server_queue import ServerQueue, yield_from_queue

app = Flask(__name__)

#create Image and Server Queues
imageQueue = ImageQueue(1000)
serverQueue = ServerQueue(1000)

@pythread
def start_server() :

    app.run(port = 10000, host = '192.168.0.103')


@app.route('/')
def render_index() :

    return render_template('index.html')

@app.route('/api/video_feed')
def video_feed() :

    #first open the server queue :
    serverQueue.locked = False
    return Response(yield_from_queue(serverQueue), mimetype = 'multipart/x-mixed-replace; boundary=frame')


#run everything here  :
if __name__ == "__main__" :

    #define process pipeline : 
    start_server()
    consumer(imageQueue, FeatureGenerator(serverQueue).face_callback)

    pp = Preprocessor(imageQueue)
    pp.custom_webcam_processor()

    
    



