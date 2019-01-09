import time
import imutils
import cv2
from imutils.video import FPS
from threading import Thread


class CameraStream:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.stopped = False
        self.frame = self.camera.read()

    def start(self):
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self

    def running(self):
        return not self.stopped

    def update(self):
        while True:
            if self.stopped:
                return

            _, self.frame = self.camera.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.camera.release()


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
    cv2.putText(frame, fps.fps(), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

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


