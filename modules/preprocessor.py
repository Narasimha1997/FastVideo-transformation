import numpy
import io
from PIL import Image
from modules.image_queue import ImageQueue, producer, consumer, QueueProducer
from modules.features import FeatureGenerator
import cv2

#for demo



IMAGE_SIZE = (256, 256)

def buffer_to_array(byte_buffer) :
    
    image = numpy.array(Image.open(io.BytesIO(byte_buffer)))
    print(image.shape)
    return image

class Preprocessor :

    def __init__(self, queue) :
        self.queue = queue
        
    
    def write_image_to_queue(self, image) :
        #image should be a byte array of 
        #just write image to the queue and do nothing

        #producer is an asynchronous function :
        image = buffer_to_array(image)
        producer(self.queue, [image])
    

    #a custom stage built for receiving videos from IPCAM
    def custom_ipcam_processor(self, video_steam_url) :

        cap = cv2.VideoCapture(video_steam_url)

        while(True):
            ret, frame = cap.read()
            frame = cv2.resize(frame, (500, 500))
            producer(self.queue, [frame])
            if cv2.waitKey(200) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            
    def custom_video_processor(self, video_file) :

        cap = cv2.VideoCapture(video_file)
        producer = QueueProducer(self.queue)

        while True :

            ret, frame = cap.read()
            frame = cv2.resize(frame, (600,600))

            #direct write to Queue , not using threads
            producer.insert([frame])

            cv2.imshow("DEMO", frame)

            if cv2.waitKey(20) & 0xFF == ord('q') :
                cv2.destroyAllWindows()
                break
    
    def custom_webcam_processor(self) :

         cap = cv2.VideoCapture(0)
         producer = QueueProducer(self.queue)

         while True :

             ret, frame = cap.read()

             frame = cv2.resize(frame, (400, 400))

             cv2.imshow("DEMO", frame)

             producer.insert([frame])

             if cv2.waitKey(2) & 0xFF == ord('q') :
                cv2.destroyAllWindows()
                break