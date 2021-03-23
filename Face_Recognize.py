import cv2
import numpy as np
from dbms import db
import pickle
pictureTaken=0
imageString=None
frame=None
def feed():
    global pictureTaken
    global imageString
    global buffer1
    imageString=None
    pictureTaken=0
    faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    capture =cv2.VideoCapture(0)

    while (pictureTaken==0):
        global buffer1
        success, frame=capture.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=10)
        for(x,y,h,w) in faces:
            
            print(x, y, h, w)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        ret, buffer=cv2.imencode('.jpg',frame)
        buffer1=frame
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()

def TakePicture():
    global pictureTaken
    global imageString
    global buffer1
    pictureTaken=1
    imageString=pickle.dumps(buffer1)
    return (imageString)
def sendToDatabase(name, ID, choice, image):
    myCursor = db.cursor()
    sql = "INSERT INTO "+choice+" (StudentID, Name, Image) VALUES (%s, %s, %s)"
    val=(ID,name,image)
    myCursor.execute(sql,val)
    db.commit()