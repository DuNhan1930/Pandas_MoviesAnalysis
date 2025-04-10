import pandas as pd
import os

BASE_DIR = "/home/dunhan/PycharmProjects/Pandas_MoviesAnalysis"
CSV_PATH = os.path.join(BASE_DIR, "movies.csv")
data = pd.read_csv(CSV_PATH)
print(data.info())
print(data.describe().to_string())

print("Original release_date format:")
print(data.loc[10398:10403, ['release_date', 'release_year']])

# Parse release_date with known format, coerce errors
data['release_date'] = pd.to_datetime(data['release_date'], format='%m/%d/%y', errors='coerce')
print("release_date have mismatch format(e.g. 2067 instead of 1967) in some rows:")
print(data.loc[10398:10403, ['release_date', 'release_year']])

