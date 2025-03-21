from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Open the webcam (change index or URL as needed)
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Optionally, you can resize or process the frame here
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # Yield frame in byte format for MJPEG streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    # Render the HTML template that displays the video
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the correct MIME type
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the app on all available IP addresses, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
  
