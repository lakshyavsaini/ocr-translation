import cv2
from config import DEVICE

from surya.foundation import FoundationPredictor
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor


class SuryaOCRService:

    def __init__(self):
        print("Initializing Surya OCR predictors (GPU Linux)")

        self.foundation = FoundationPredictor(device=DEVICE)

        self.detector = DetectionPredictor(
            foundation_predictor=self.foundation
        )

        self.recognizer = RecognitionPredictor(
            foundation_predictor=self.foundation
        )

    def extract_text(self, image):

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        detections = self.detector([image_rgb])[0]

        if not detections:
            return ""

        results = self.recognizer([image_rgb], [detections])[0]

        texts = []

        for line in results:
            texts.append(line.text)

        return "\n".join(texts)


surya_service = SuryaOCRService()
