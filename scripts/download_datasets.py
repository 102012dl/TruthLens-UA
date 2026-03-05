"""
TruthLens UA — Download ISOT and optional UA datasets.
Run from project root: python scripts/download_datasets.py

ISOT: auto-download from UVic (no login), or Kaggle "Fake and Real News".
"""
import io
import zipfile
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# UVic ISOT dataset (same as in github.com/102012dl/TruthLens notebook)
UVIC_ISOT_ZIP = "https://onlineacademiccommunity.uvic.ca/isot/wp-content/uploads/sites/7295/2023/03/News-_dataset.zip"


def _find_case_insensitive(folder: Path, filename: str) -> Optional[Path]:
    if not folder.exists():
        return None
    target = filename.lower()
    for p in folder.iterdir():
        if p.is_file() and p.name.lower() == target:
            return p
    return None


def isot_from_uvic() -> bool:
    """Download ISOT from UVic, extract to data/, ensure Fake.csv and True.csv."""
    if (DATA_DIR / "Fake.csv").exists() and (DATA_DIR / "True.csv").exists():
        print("ISOT: Fake.csv and True.csv already in data/")
        return True
    try:
        import urllib.request

        print("Downloading ISOT from UVic...")
        req = urllib.request.urlopen(UVIC_ISOT_ZIP, timeout=300)
        data = req.read()
        req.close()
    except Exception as e:
        print(f"  UVic download failed: {e}")
        return False
    try:
        with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
            # Extract to a temp subdir to avoid cluttering data/
            extract_dir = DATA_DIR / "_isot_extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            zf.extractall(extract_dir)
        # Find True.csv / Fake.csv case-insensitively in extracted tree
        true_src = _find_case_insensitive(extract_dir, "True.csv")
        fake_src = _find_case_insensitive(extract_dir, "Fake.csv")
        for f in extract_dir.rglob("*.csv"):
            if f.name.lower() == "true.csv":
                true_src = true_src or f
            elif f.name.lower() == "fake.csv":
                fake_src = fake_src or f
        if true_src and fake_src:
            import shutil

            shutil.copy2(true_src, DATA_DIR / "True.csv")
            shutil.copy2(fake_src, DATA_DIR / "Fake.csv")
            print("  -> data/True.csv, data/Fake.csv")
            shutil.rmtree(extract_dir, ignore_errors=True)
            return True
        print("  UVic zip did not contain True.csv/Fake.csv in expected names.")
    except Exception as e:
        print(f"  Extract/copy failed: {e}")
    return False


def isot_from_kaggle():
    """If zip already in data/, extract it. Else print Kaggle instructions."""
    zip_path = DATA_DIR / "fake-and-real-news-dataset.zip"
    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(DATA_DIR)
        print("Extracted ISOT from existing zip.")
        return True
    print(
        "Kaggle fallback: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset\n"
        "  Place Fake.csv, True.csv into data/"
    )
    return False


def main():
    print("TruthLens UA — dataset download")
    print("Data dir:", DATA_DIR)
    if isot_from_uvic():
        pass
    elif not ((DATA_DIR / "Fake.csv").exists() and (DATA_DIR / "True.csv").exists()):
        isot_from_kaggle()
    if (DATA_DIR / "Fake.csv").exists() and (DATA_DIR / "True.csv").exists():
        print("ISOT ready. Run notebooks/01_isot_fake_news_mlflow.ipynb")
    else:
        print("Place Fake.csv and True.csv in data/ for ISOT training.")


if __name__ == "__main__":
    main()
