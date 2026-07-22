from transformers import MarianMTModel, MarianTokenizer
import os
from src.config import Config

class TranslatorError(Exception):
    pass

class MarianTranslator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarianTranslator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        if self._initialized:
            return
        os.makedirs(Config.MODEL_DIR, exist_ok=True)
        try:
            self.tokenizer = MarianTokenizer.from_pretrained(
                Config.MODEL_NAME,
                cache_dir=Config.MODEL_DIR,
                local_files_only=False
            )
            self.model = MarianMTModel.from_pretrained(
                Config.MODEL_NAME,
                cache_dir=Config.MODEL_DIR,
                local_files_only=False
            )
            self._initialized = True
        except Exception as e:
            raise TranslatorError(str(e))

    def translate(self, text: str) -> str:
        if not self._initialized:
            self.initialize()
        if not text.strip():
            return ""
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            translated_tokens = self.model.generate(**inputs)
            result = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
            return result
        except Exception as e:
            raise TranslatorError(str(e))
