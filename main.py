import time

import imutils
import cv2
from imutils.video import FPS
from threading import Thread
from queue import Queue


class CameraStream:
    def __init__(self, queueSize = 3):
        self.camera = cv2.VideoCapture(0)
        self.stopped = False
        self.queue = Queue(maxsize=queueSize)
        self.current = self.camera.read()

    def start(self):
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self

    def hasMore(self):
        return not self.stopped
        # return self.queue.qsize() > 0

    def update(self):
        while True:
            if self.stopped:
                return

            _, self.current = self.camera.read()
            # if self.queue.qsize() >= 2:
            #     return
            #
            # # if not self.queue.full():
            # grabbed, frame0 = self.camera.read()
            # if not grabbed:
            #     self.stop()
            #     return
            #
            # self.queue.put(frame0)

    def read(self):
        return self.current
        # return self.queue.get()

    def stop(self):
        self.stopped = True
        self.camera.release()


# cap = cv2.VideoCapture(0)
camera = CameraStream()
camera.start()
time.sleep(1)

fps = FPS().start()

while camera.hasMore():
    # Capture frame-by-frame
    frame = camera.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame and fps
    cv2.putText(frame, "Slow", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show frame
    cv2.imshow('frame', gray)
    fps.update()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# When everything done, release the capture
camera.stop()
cv2.destroyAllWindows()


