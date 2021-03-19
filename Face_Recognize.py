import cv2
import numpy as np
from dbms import db
pictureTaken=0
imageString=None
frame=None
def feed():
    global pictureTaken
    global imageString
    global frame1
    imageString=None
    pictureTaken=0
    faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    capture =cv2.VideoCapture(0)

    while (pictureTaken==0):
        global frame1
        success, frame=capture.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=10)
        for(x,y,h,w) in faces:
            print(x, y, h, w)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        ret, buffer=cv2.imencode('.jpg',frame)
        print(frame)
        frame1=frame
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()

def TakePicture():
    global pictureTaken
    global imageString
    global frame1
    print("TEST ",frame1)
    pictureTaken=1
    imageString=np.ndarray.dumps(frame1)
    return (imageString)
def sendToDatabase(name, id, image):
    myCursor = db.cursor()
    myCursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")