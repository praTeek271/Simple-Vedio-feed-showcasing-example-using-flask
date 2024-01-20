from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# OpenCV VideoCapture object (initialized as None)
video_capture = None

# Variable to control video streaming
streaming = False

def initialize_camera():
    global video_capture
    if video_capture is None or not video_capture.isOpened():
        video_capture = cv2.VideoCapture(0)

def generate_frames():
    global streaming
    initialize_camera()
    while streaming:
        if video_capture is None or not video_capture.isOpened():
            break

        success, frame = video_capture.read()
        if not success:
            break

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start')
def start():
    global streaming
    if not streaming:
        streaming = True
    return 'Streaming started!'

@app.route('/stop')
def stop():
    global streaming
    streaming = False
    return 'Streaming stopped!'

@app.route('/reset')
def reset():
    global video_capture
    if video_capture is not None:
        video_capture.release()
        video_capture = None
    return 'Video capture released!'

if __name__ == '__main__':
    app.run(debug=True)
