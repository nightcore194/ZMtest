from pathlib import Path

ENCODING = "UTF-8"

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR.joinpath('.env')