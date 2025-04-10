import pandas as pd
import os

# Load data
BASE_DIR = "/home/dunhan/PycharmProjects/Pandas_MoviesAnalysis/data"
list_data = ['genre_counts.csv', 'movies_by_date.csv', 'high_rated_movies.csv','top_profit_movies.csv']
for i in list_data:
    CSV_PATH = os.path.join(BASE_DIR, i)
    df = pd.read_csv(CSV_PATH)
    print(i)
    print(df.head(10).to_string())
    print("")

