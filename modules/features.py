import face_recognition
from PIL import Image, ImageDraw
import cv2
import numpy
import time
from modules.server_queue import write_to_server_queue

class FeaturesProcessor :

    def __init__(self, serverQueue, features_selectors = ["left_eye", "right_eye"]) :

        self.serverQueue = serverQueue
        self.features_selectors = features_selectors
        self.offset = 0
    
    def draw_landmarks(self, image, features):
        pil_image = Image.fromarray(image)
        for face_landmarks in features : 
            #draw 
            d = ImageDraw.Draw(pil_image, mode = 'RGBA')

            d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
            d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
            d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
            d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

    # Gloss the lips
            d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
            d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
            d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
            d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

    # Sparkle the eyes
            d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
            d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    # Apply some eyeliner
            d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
            d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
        
        ret, jpeg = cv2.imencode('.jpg', numpy.array(pil_image))
        write_to_server_queue(jpeg.tobytes(), self.serverQueue)
        #self.offset += 1


class FeatureGenerator : 

    def __init__(self, serverQueue) :

        self.landmark_processor = FeaturesProcessor(serverQueue)
    
    #demo function, writes all the features to 
    def face_callback(self, image_array) :

        features = face_recognition.face_landmarks(image_array)
        #pipleine : 
        self.landmark_processor.draw_landmarks(image_array, features)

