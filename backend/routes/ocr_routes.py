from fastapi import APIRouter, UploadFile, File, Body
from services.translation_service import translation_service
from services.text_post_processing import normalize_ocr_text
from services.surya_ocr_service import surya_service
from utils.image_utils import read_image_bytes, resize_for_ocr
from config import DEFAULT_SOURCE_LANG, DEFAULT_TARGET_LANG
import time
import base64
import logging
from PIL import Image
import io
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Surya predictors once at module level
print("Initializing Surya predictors...", flush=True)
foundation_predictor = FoundationPredictor()
recognition_predictor = RecognitionPredictor(foundation_predictor)
detection_predictor = DetectionPredictor()
print("Surya predictors ready!", flush=True)

@router.post("/ocr-translate")
async def ocr_translate(image: UploadFile = File(...)):

    file_bytes = await image.read()

    img = read_image_bytes(file_bytes)
    img = resize_for_ocr(img)

    # Step 1: OCR
    extracted_text = surya_service.extract_text(img)

    # Step 2: NEW — clean and merge OCR lines before translation
    processed_text = normalize_ocr_text(extracted_text)

    # Step 3: Translation
    translated_text = translation_service.translate(
        processed_text,
        DEFAULT_SOURCE_LANG,
        DEFAULT_TARGET_LANG,
    )

    return {
        "ocr_text": processed_text,
        "translated_text": translated_text
    }

@router.post("/infer")
async def ocr_only(request: dict = Body(...)):
    start_time = time.time()
    
    try:
        print(f"[1] Request received", flush=True)
        
        # Extract parameters from request
        image_b64 = request.get("image_b64")
        source_lang = request.get("language", DEFAULT_SOURCE_LANG)
        target_lang = request.get("target_language", DEFAULT_TARGET_LANG)
        print(
            f"[2] Source: {source_lang}, Target: {target_lang}, Image b64 length: {len(image_b64) if image_b64 else 0}",
            flush=True,
        )
        
        if not image_b64:
            return {
                "success": False,
                "error": "No image provided",
                "processing_time": 0
            }
        
        # Decode base64 image
        print(f"[3] Decoding base64...", flush=True)
        image_bytes = base64.b64decode(image_b64)
        print(f"[4] Decoded {len(image_bytes)} bytes", flush=True)
        
        # Convert to PIL Image
        print(f"[5] Converting to PIL Image...", flush=True)
        pil_image = Image.open(io.BytesIO(image_bytes))
        print(f"[6] Image size: {pil_image.size}, mode: {pil_image.mode}", flush=True)
        
        # Step 1: OCR using Surya directly
        print(f"[7] Starting OCR with Surya...", flush=True)
        predictions = recognition_predictor([pil_image], det_predictor=detection_predictor)
        print(f"[8] OCR complete. Pages: {len(predictions)}", flush=True)
        
        # Extract line-level text + boxes
        print(f"[9] Extracting lines + boxes from predictions...", flush=True)
        pages_payload = []
        all_lines = []
        all_translations = []
        for page in predictions:
            print(f"[9a] Page has {len(page.text_lines)} lines", flush=True)
            page_lines = []
            page_texts = []
            for line in page.text_lines:
                line_text = getattr(line, "text", None)
                if not line_text:
                    line_text = "".join([char.text for char in line.chars])
                line_text = line_text.strip()
                if not line_text:
                    continue

                page_texts.append(line_text)
                page_lines.append(
                    {
                        "text": line_text,
                        "bbox": line.bbox,
                        "polygon": line.polygon,
                    }
                )

            translations = translation_service.translate_lines(
                page_texts,
                source_lang,
                target_lang,
            )
            for payload, translated in zip(page_lines, translations):
                payload["translation"] = translated

            pages_payload.append(
                {
                    "width": pil_image.size[0],
                    "height": pil_image.size[1],
                    "lines": page_lines,
                }
            )

            all_lines.extend(page_texts)
            all_translations.extend(translations)

        extracted_text = "\n".join(all_lines)
        translated_text = "\n".join(all_translations)
        print(
            f"[10] Extracted {len(all_lines)} lines, total chars: {len(extracted_text)}",
            flush=True,
        )
        
        processing_time = time.time() - start_time
        
        payload = {
            "success": True,
            "text": extracted_text,
            "translated_text": translated_text,
            "pages": pages_payload,
            "processing_time": processing_time,
        }
        print(f"✓ OCR Success: {processing_time:.3f}s | Text: {extracted_text[:50]}...", flush=True)
        return payload
        
    except Exception as e:
        import traceback
        processing_time = time.time() - start_time
        error_msg = str(e) if str(e) else repr(e)
        traceback_str = traceback.format_exc()
        
        payload = {
            "success": False,
            "error": error_msg,
            "processing_time": processing_time
        }
        print(f"✗ OCR Error: {error_msg}", flush=True)
        print(f"✗ Traceback:\n{traceback_str}", flush=True)
        logger.error(f"OCR Inference Error: {error_msg}\n{traceback_str}")
        return payload