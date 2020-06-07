import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

RAW_ADS_PATH = os.path.join(DATA_DIR, "raw", "ads.csv")
PROCESSED_ADS_PATH = os.path.join(DATA_DIR, "processed", "ads.txt")
CATEGORY_DATA_PATH = os.path.join(DATA_DIR, "interim", "categories.csv")
FASTTEXT_CATEGORY_TRAIN_PATH = os.path.join(DATA_DIR, "processed", "categories.train")
FASTTEXT_CATEGORY_TEST_PATH = os.path.join(DATA_DIR, "processed", "categories.test")
LOCATIONS_PATH = os.path.join(DATA_DIR, "processed", "locations.txt")

MODELS_DIR = os.path.join(ROOT_DIR, "models")
LOCATIONS_VECTORIZER_PATH = os.path.join(MODELS_DIR, "ads.location.vectorizer.pkl")

TOKENIZER_PATH = os.path.join(MODELS_DIR, "tokenizer.pkl")


def fasttext_model_file(module: str, dim: int, extension: str) -> str:
    return os.path.join(MODELS_DIR, f"ads.{module}.{dim}.{extension}")
