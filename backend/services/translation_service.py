import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from config import DEVICE, TRANSLATION_MODEL_NAME, DEFAULT_SOURCE_LANG, DEFAULT_TARGET_LANG


class TranslationService:

    def __init__(self):
        self.model, self.tokenizer = self.load_translation_model()

    def load_translation_model(self):
        print(f"Loading translation model: {TRANSLATION_MODEL_NAME}")
        dtype = torch.float16 if DEVICE == "cuda" else torch.float32
        tokenizer = AutoTokenizer.from_pretrained(
            TRANSLATION_MODEL_NAME,
            use_fast=False,
            trust_remote_code=True,
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            TRANSLATION_MODEL_NAME,
            torch_dtype=dtype,
            trust_remote_code=True,
        )
        model = model.to(torch.device(DEVICE))
        model.eval()
        return model, tokenizer

    def translate_lines(
        self,
        lines: list[str],
        source_lang: str | None = None,
        target_lang: str | None = None,
    ) -> list[str]:
        if not lines:
            return []

        src_lang = source_lang or DEFAULT_SOURCE_LANG
        tgt_lang = target_lang or DEFAULT_TARGET_LANG

        inputs = self.tokenizer(
            lines,
            return_tensors="pt",
            padding=True,
            truncation=True,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.inference_mode():
            outputs = self.model.generate(**inputs, max_new_tokens=512)

        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

    def translate(
        self,
        text: str,
        source_lang: str | None = None,
        target_lang: str | None = None,
    ) -> str:
        if not text:
            return ""
        return self.translate_lines([text], source_lang, target_lang)[0]


translation_service = TranslationService()
