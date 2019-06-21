from modules.runner import PyThread as pythread
import time
import queue

class QueueConsumer :

    def __init__(self, image_queue):
        
        self.queue_object = image_queue
    
    def retrive(self):

        #retrives the last element from the queue
        while self.queue_object.isEmpty() : 
            time.sleep(0.1) 
        return self.queue_object.delete()
    
    def isEmpty(self) :
        return self.queue_object.isEmpty()
    

    def keepRetriving(self, callback) :
        while True :
            if not self.queue_object.isEmpty() :
                callback(self.retrive()[0])
                

class ImageQueue :

    def __init__(self, size) :

       self.queue = queue.Queue(maxsize = size)
    
    def insert(self, image) :

        self.queue.put(image)
    
    def delete(self) :

        return self.queue.get_nowait()
    
    def isEmpty(self) :

        return self.queue.empty()
    
    def isFull(self) :
        
        return self.queue.full()
    

class QueueProducer :

    def __init__(self, queue_object) :

        self.queue_object = queue_object
    
    def insert(self, image_s) :

            while self.queue_object.isFull() : 
                time.sleep(0.1)
            self.queue_object.insert(image_s)


@pythread
def producer(queue_object, image_s) :
    queueProducer = QueueProducer(queue_object)
    queueProducer.insert(image_s)


@pythread
def consumer(queue_object, callback) :

    queueConsumer = QueueConsumer(queue_object)
    queueConsumer.keepRetriving(callback)



