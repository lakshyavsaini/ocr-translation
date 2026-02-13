import torch
import cv2
from config import DEVICE
from PIL import Image

# patch for pad_token_id issue
from transformers.configuration_utils import PretrainedConfig
if not hasattr(PretrainedConfig, "pad_token_id"):
    PretrainedConfig.pad_token_id = 0

from surya.foundation import FoundationPredictor
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor


class SuryaOCRService:

    def __init__(self):
        print("Initializing Surya OCR predictors (YOUR API VARIANT)")

        dtype = torch.float16 if DEVICE == "cuda" else torch.float32

        # foundation is required ONLY for recognition predictor
        self.foundation = FoundationPredictor(
            device=DEVICE,
            dtype=dtype
        )

        # detection uses device + dtype directly
        self.detector = DetectionPredictor(
            device=DEVICE,
            dtype=dtype
        )

        # recognition requires foundation_predictor positional argument
        self.recognizer = RecognitionPredictor(
            self.foundation
        )

    def extract_text(self, image):
        # Convert numpy/cv2 image to PIL Image (Surya requires PIL Images)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        detections = self.detector([pil_image])[0]

        if not detections:
            return ""

        results = self.recognizer([pil_image], [detections], det_predictor=self.detector)[0]

        texts = [line.text for line in results]

        return "\n".join(texts)


surya_service = SuryaOCRService()
