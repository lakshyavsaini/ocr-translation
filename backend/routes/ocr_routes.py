from fastapi import APIRouter, UploadFile, File
from services.surya_ocr_service import surya_service
from services.translation_service import translation_service
from utils.image_utils import read_image_bytes, resize_for_ocr

router = APIRouter()

@router.post("/ocr-translate")
async def ocr_translate(image: UploadFile = File(...)):

    file_bytes = await image.read()

    img = read_image_bytes(file_bytes)
    img = resize_for_ocr(img)

    extracted_text = surya_service.extract_text(img)

    translated_text = translation_service.translate(extracted_text)

    return {
        "ocr_text": extracted_text,
        "translated_text": translated_text
    }
