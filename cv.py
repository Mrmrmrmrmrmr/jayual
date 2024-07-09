from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)  # 웹캠에서 비디오 캡처 객체 생성 (기본 카메라는 0번 장치)

    if not camera.isOpened():
        raise RuntimeError("카메라를 열 수 없습니다.")

    while True:
        # 프레임 읽기
        success, frame = camera.read()
        if not success:
            break

        # 프레임을 JPEG 포맷으로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 프레임을 yield하여 웹 브라우저에 전달
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
