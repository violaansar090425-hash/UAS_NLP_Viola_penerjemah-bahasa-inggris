import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "smarttranslate_secret_key_12345")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(BASE_DIR, "smarttranslate.db")
    DATASET_DIR = os.path.join(BASE_DIR, "dataset")
    DATASET_PATH = os.path.join(DATASET_DIR, "dataset.csv")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    MODEL_NAME = "Helsinki-NLP/opus-mt-id-en"
