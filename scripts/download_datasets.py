"""
TruthLens UA — Download ISOT and optional UA datasets.
Run from project root: python scripts/download_datasets.py

ISOT Fake/Real News: Kaggle "Fake and Real News" or direct URLs.
"""
import os
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, desc: str = "") -> bool:
    try:
        print(f"Downloading {desc or url}...")
        urllib.request.urlretrieve(url, dest)
        print(f"  -> {dest}")
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        return False


def isot_from_kaggle():
    """Instructions: install kaggle CLI, place API key, then run:
    kaggle datasets download -d clmentbisaillon/fake-and-real-news-dataset -p data/
    unzip -o data/fake-and-real-news-dataset.zip -d data/
    """
    zip_path = DATA_DIR / "fake-and-real-news-dataset.zip"
    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(DATA_DIR)
        print("Extracted ISOT from existing zip.")
        return True
    print(
        "ISOT: Download from Kaggle manually:\n"
        "  1. https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset\n"
        "  2. Download -> place Fake.csv, True.csv into data/\n"
        "  Or: pip install kaggle; kaggle datasets download -d clmentbisaillon/fake-and-real-news-dataset -p data/"
    )
    return False


def main():
    print("TruthLens UA — dataset download")
    print("Data dir:", DATA_DIR)
    isot_from_kaggle()
    if (DATA_DIR / "Fake.csv").exists() and (DATA_DIR / "True.csv").exists():
        print("ISOT files present. Ready for notebooks/01_isot_fake_news_mlflow.ipynb")
    else:
        print("Place Fake.csv and True.csv in data/ for ISOT training.")


if __name__ == "__main__":
    main()
