import cv2
from dbms import db
import pickle
import face_recognition
myCursor = db.cursor()
myCursor.execute("SELECT * FROM ai")
myresult = myCursor.fetchall()


def encodeImage(frame,x,y,h,w):
    encodedFrame=face_recognition.face_encodings(frame,None,1,"large")[0]
    faceLocations=face_recognition.face_locations(frame)
    print(len(encodedFrame))
    print(faceLocations)

    results=face_recognition.compare_faces([encodedImage,encodedJayash,encodedUmar1,encodedUmar2],encodedFrame)
    distances=face_recognition.face_distance([encodedImage,encodedJayash,encodedUmar1,encodedUmar2],encodedFrame)
    print(results)
    print(distances)
for x in myresult:
  print(x[0])
  image=pickle.loads(x[2])
  #cv2.imwrite("test.jpg",image)

encodedImage=face_recognition.face_encodings(image)[0]
imgJayash=face_recognition.load_image_file('testjayash.jpg')
encodedJayash=face_recognition.face_encodings(imgJayash)[0]

imgUmar1=face_recognition.load_image_file('testumar1.jpg')
encodedUmar1=face_recognition.face_encodings(imgUmar1)[0]

imgUmar2=face_recognition.load_image_file('testumar2.jpg')
encodedUmar2=face_recognition.face_encodings(imgUmar2)[0]

faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
capture =cv2.VideoCapture(0)

foundface=False
while (True):
    success, frame=capture.read()
    copiedFrame=frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frame,scaleFactor=1.05,minNeighbors=10)
    for(x,y,h,w) in faces:
        FaceFrame=frame
        print(x, y, h, w)
        x1=x
        y1=y
        h1=h
        w1=w
        cv2.rectangle(copiedFrame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',copiedFrame)
    if(foundface==False):
        if len(face_recognition.face_locations(FaceFrame))>0:
            foundface=True
            goodFaceFrame=FaceFrame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.imwrite("testt.jpg",FaceFrame)
encodeImage(goodFaceFrame,x1,y1,h1,w1)

capture.release()
cv2.destroyAllWindows()