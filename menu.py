from flask import Flask, render_template, Response, request
import Face_Recognize

app=Flask(__name__)
global imageString
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/class_sign_in')
def class_sign_up():
    return render_template('classSignUp.html')

@app.route('/video_feed')
def video_feed():
    return Response(Face_Recognize.feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/class_registration')
def classRegistration():
    return render_template('ClassRegistration.html')

@app.route('/takepicture')
def takepicture():
    global imageString
    imageString=Face_Recognize.TakePicture()

@app.route('/register',methods=['POST'])
def register():
    global imageString
    Face_Recognize.sendToDatabase(request.form['Name'],request.form['ID'],imageString)
    return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)


