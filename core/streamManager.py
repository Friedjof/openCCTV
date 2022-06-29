class HandDetection:
    detection: bool = True


class FaceDetection:
    detection: bool = True
    irises: bool = True
    mesh: bool = False
    contours: bool = True


class BodyDetection:
    detection: bool = False


class StreamManager:
    detection: bool = True
    streaming: bool = True

    hand_detection: HandDetection = None
    face_detection: FaceDetection = None
    body_detection: BodyDetection = None

    def __init__(self):
        self.hand_detection = HandDetection()
        self.face_detection = FaceDetection()
        self.body_detection = BodyDetection()
