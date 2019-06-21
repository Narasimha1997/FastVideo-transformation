import queue
import time


class ServerQueue :

    def __init__(self, max_size = 1000):

        self.max_size = max_size
        self.queue = queue.Queue(maxsize = max_size)
        self.locked = True
    
    def insert(self, image) :

        if not self.locked :
            print("Wrote frame..")
            self.queue.put(image)
        
    def delete(self) :

        if not self.locked :
            return self.queue.get()
    
    def isEmpty(self) :

        if self.queue.empty() : return True
        return False
    
    def isFull(self):

        if self.queue.full() : return True
        return False
    
    def isLocked(self) :
        return self.locked
    

def write_to_server_queue(image, serverQueue) :

    if not serverQueue.isLocked(): 

        while serverQueue.isFull() : time.sleep(0.1)
        serverQueue.insert(image)

def yield_from_queue(serverQueue) :

    #this runs in an infinite loop, so call it from a thread
    while True :

        if not serverQueue.isLocked() and not serverQueue.isEmpty() :
            #package this in a HTTP Message : 
            frame = serverQueue.delete()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
