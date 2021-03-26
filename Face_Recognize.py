import cv2
import numpy as np
from dbms import db
import pickle
import face_recognition
pictureTaken=0
imageString=None
frame=None
faceScanned=False
namesList=[]
imagesList=[]
def feed():
    global pictureTaken
    global imageString
    global buffer1
    imageString=None
    pictureTaken=0
    faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    capture =cv2.VideoCapture(0)
    foundFace=False
    temp=[]
    while (pictureTaken==0):
        global buffer1
        success, frame=capture.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=6)
        if len(faces)!=len(temp):
            foundFace=False
        temp=faces
        for(x,y,h,w) in faces:

            print(x, y, h, w)
            if(foundFace==False):
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            else:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if(foundFace==False):
            if len(face_recognition.face_locations(frame))>0:
                foundFace=True
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

def recognizer():
    def compareFaces(frame):
        global namesList
        global imagesList
        print("LENGTH ",len(namesList))
        encodedFrame=face_recognition.face_encodings(frame,None,1,"large")[0]
        faceLocations=face_recognition.face_locations(frame)
        results=face_recognition.compare_faces(imagesList,encodedFrame)
        for value in results:
            if value==True:
                idx=results.index(True)
        print("YOU ARE ",namesList[idx])
    faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    capture =cv2.VideoCapture(0)

    foundface=False
    global faceScanned
    faceScanned=False
    temp=[]
    while (faceScanned==False):
        success, frame=capture.read()
        copiedFrame=frame
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(frame,scaleFactor=2,minNeighbors=10)
        if len(faces)!=len(temp):
            foundface=False
        temp=faces
        for(x,y,h,w) in faces:
            FaceFrame=frame
            #print(x, y, h, w)
            cv2.rectangle(copiedFrame,(x,y),(x+w,y+h),(0,255,0),2)
        if(foundface==False):
            if len(face_recognition.face_locations(frame))>0:
                print("FOUND")
                foundface=True
                goodFaceFrame=frame
        ret, buffer=cv2.imencode('.jpg',frame)
        buffer1=frame
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    compareFaces(goodFaceFrame)
    
    capture.release()
    cv2.destroyAllWindows()
def scanFace():
    global faceScanned
    faceScanned=1
    print("SCANNING...")
def updateValues(names,images):
    global namesList
    global imagesList
    namesList=names
    imagesList=images
