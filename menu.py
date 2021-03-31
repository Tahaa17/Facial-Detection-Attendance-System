from flask import Flask, render_template, Response, request, send_file
import Face_Recognize
from dbms import db
import pickle
import face_recognition
import datetime
global imageString
global namesList
namesList=[]
global imagesList
imagesList=[]

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/class_sign_in')
def class_sign_up():
    return render_template('classSignUp.html')

@app.route('/video_feed')
def video_feed():
    return Response(Face_Recognize.feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/detection_feed')
def detection_feed():
    global namesList
    global imagesList
    return Response(Face_Recognize.recognizer(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/class_registration')
def classRegistration():
    return render_template('ClassRegistration.html')

@app.route('/takepicture')
def takepicture():
    global imageString
    imageString=Face_Recognize.TakePicture()

@app.route('/scanface')
def scanface():
    Face_Recognize.scanFace()

@app.route('/queryDB')
def queryDB():
    name=request.query_string.decode("utf-8")
    print("NAME ",name)
    myCursor = db.cursor()
    myCursor.execute("SELECT * FROM "+name)
    myresult = myCursor.fetchall()
    myCursor.close()
    studentNames=[]
    studentImages=[]
    for row in myresult:
        print(row[0])
        studentNames.append(row[1])
        studentImages.append(face_recognition.face_encodings(pickle.loads(row[2]),None,1,"large")[0])
    print("Images length",len(studentImages))
    print("Names length",len(studentNames))
    Face_Recognize.updateValues(studentNames,studentImages)


@app.route('/register',methods=['POST'])
def register():
    global imageString
    Face_Recognize.sendToDatabase(request.form['Name'],request.form['ID'],request.form['classes'],imageString)
    return render_template('index.html',message="Successfully registered for "+request.form['classes'])

@app.route('/getMatch')
def getMatch():
    print("THIS GETS CALLED")
    match=Face_Recognize.getMatch()
    if(match!=None):
        return match
    return "No Match Found"

@app.route('/confirmStudent')
def confirmStudent():
    name=request.query_string.decode("utf-8")
    args=name.split('?')
    print(name)
    print(args)
    now = datetime.datetime.now()
    myCursor = db.cursor()
    sql = "UPDATE "+args[0]+" SET LastLogin =%s WHERE Name = %s"
    vals=(now,args[1])
    myCursor.execute(sql,vals)
    db.commit()
    print("Student signs in")
    return render_template('index.html',message=args[1]+" you were signed in!")

@app.route('/recognitionFail')
def recognitionFail():
    return render_template('classSignUp.html',message="Sorry for the inconvinience! Please try again!")

@app.route('/jutrImage')
def jutrImage():
    filename= 'jutr_logo_final.png'
    return send_file(filename, mimetype='Facial-Detection-Attendance-System\jutr_logo_final.png')

@app.route('/BG')
def BG():
    filename= 'background.jpg'
    return send_file(filename, mimetype='Facial-Detection-Attendance-System\backgrounds.jpg')

if __name__=='__main__':
    app.run(debug=True)

