from PIL import Image
from numpy import ndarray, asarray

import cv2
import mediapipe as mp

from .detector import PoseDetector, FaceDetector, HandDetector
from .streamManager import StreamManager


class VideoCamera(object):
    def __init__(self, manager):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh

        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        self.stream_manager: StreamManager = manager

        self.body_detector = PoseDetector()
        self.face_detector = FaceDetector(self.stream_manager)
        self.hand_detector = HandDetector()

        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if self.manager.recognition:
            print("[INFO] Recognition")
            rgb_image = self.detector.detect(frame)

        ret, jpeg = cv2.imencode('.jpg', rgb_image)

        return jpeg.tobytes()

    @staticmethod
    def result(image: ndarray) -> bytes:
        frame = cv2.imencode('.jpg', asarray(image))[1]
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n'

    def loop(self):
        while True:
            success, img = self.cap.read()

            if not success:
                break

            canvas: ndarray = asarray(
                Image.new('RGB', (img.shape[1], img.shape[0]), color=(255, 255, 255))
            )

            if self.stream_manager.detection:
                if self.stream_manager.body_detection.detection:
                    body_results = self.body_detector.get_results(img)
                    img = self.body_detector.draw(img, body_results)

                if self.stream_manager.face_detection.detection:
                    face_results = self.face_detector.get_results(img)
                    img = self.face_detector.draw(img, face_results)

                if self.stream_manager.hand_detection.detection:
                    hand_results = self.hand_detector.get_results(img)
                    img = self.hand_detector.draw(img, hand_results)

            # Flip the image horizontally for a selfie-view display.
            try:
                yield self.result(img)
            except Exception as e:
                print(e)
                break
