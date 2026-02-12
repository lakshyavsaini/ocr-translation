class TranslationService:

    def __init__(self):
        self.model = self.load_translation_model()

    def load_translation_model(self):
        print("Loading translation model")
        model = "TRANSLATION_MODEL_PLACEHOLDER"
        return model

    def translate(self, text):
        translated = "translated output: " + text
        return translated

translation_service = TranslationService()
