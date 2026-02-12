import cv2
import numpy as np

def read_image_bytes(file_bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def resize_for_ocr(img, max_size=1280):
    h, w = img.shape[:2]
    scale = min(max_size / max(h, w), 1.0)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h))
