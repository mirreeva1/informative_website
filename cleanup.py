import pandas as pd
from pathlib import Path

datafile = Path('data/raw/your_dataset.csv')
newfile = Path('data/processed/cleaned.csv')

with open(newfile, 'w') as f:
    for line in datafile.open():
        cleaned_line = line[1:-2] + '\n'
        f.write(cleaned_line)


