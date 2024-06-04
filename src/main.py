from pathlib import Path

import pandas as pd
from loguru import logger

# import sys
# logger.info(f"sys.path: {sys.path}")
# sys.path.append(str(Path(__file__).resolve().parents[1]))
# logger.info(f"sys.path: {sys.path}")

from src.cleanup import clean_data
from src.create_sql import main as create_sql

if __name__ == "__main__":
    datafile = Path("data/raw/your_dataset.csv")
    newfile = Path("data/processed/cleaned.csv")
    logger.info(f"Cleaning data from {datafile} and saving it to {newfile}")
    clean_data(datafile, newfile)
    logger.success("Data has been cleaned successfully.")
    create_sql()
