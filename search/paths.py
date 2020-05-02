import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_ADS_FILE = os.path.join(DATA_DIR, "raw", "ads.csv")
PROCESSED_ADS_FILE = os.path.join(DATA_DIR, "processed", "ads.txt")

MODELS_DIR = os.path.join(ROOT_DIR, "models")


def fasttext_model_file(dim: int) -> str:
    return os.path.join(MODELS_DIR, f"ads.{dim}.bin")