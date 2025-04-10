import pandas as pd
import os
import requests

# Set directories
BASE_DIR = "/home/dunhan/PycharmProjects/Pandas_MoviesAnalysis"
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(BASE_DIR, "movies.csv")
DATA_URL = "https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Download the dataset
def download_data():
    print(f"Downloading data from {DATA_URL}...")
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        with open(CSV_PATH, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Data downloaded successfully.")
    else:
        raise Exception(f"Failed to download data. Status: {response.status_code}")

# Load dataset and fix datetime format
def load_data():
    df = pd.read_csv(CSV_PATH)

    # Parse release_date with known format, coerce errors
    df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y', errors='coerce')

    # Identify rows with year mismatch (e.g. 2067 instead of 1967)
    mismatch_mask = df['release_date'].dt.year != df['release_year']

    # Fix those rows
    df.loc[mismatch_mask, 'release_date'] = pd.to_datetime(
        df.loc[mismatch_mask, 'release_year'].astype(str) + '-' +
        df.loc[mismatch_mask, 'release_date'].dt.month.astype(str).str.zfill(2) + '-' +
        df.loc[mismatch_mask, 'release_date'].dt.day.astype(str).str.zfill(2),
        errors='coerce'
    )
    return df

# Save DataFrame to CSV
def save_df(df, filename):
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)

# 1. Sort by release date
def analyze_release_dates(df):
    sorted_df = df.sort_values(by='release_date', ascending=False)
    save_df(sorted_df, 'movies_by_date.csv')
    print("Sorted by release date saved to 'movies_by_date.csv'")

# 2. High-rated movies
def analyze_high_rated(df):
    high_rated = df[df['vote_average'] > 7.5]
    sorted_high_rated = high_rated.sort_values(by='vote_average', ascending=False)
    save_df(sorted_high_rated, 'high_rated_movies.csv')
    print(f"{len(high_rated)} high-rated movies saved to 'high_rated_movies.csv'")

# 3. Revenue extremes
def analyze_revenue(df):
    highest = df.loc[df['revenue'].idxmax()]
    lowest = df.loc[df['revenue'].idxmin()]
    print("Revenue extremes:")
    print(f"Highest: {highest['original_title']} (${highest['revenue']:,})")
    print(f"Lowest: {lowest['original_title']} (${lowest['revenue']:,})")

# 4. Total revenue
def calculate_total_revenue(df):
    total = df['revenue'].sum()
    print(f"Total revenue: ${total:,}")

# 5. Most profitable movies
def analyze_profits(df):
    df['profit'] = df['revenue'] - df['budget']
    top_profits = df.sort_values(by='profit', ascending=False).head(10)
    save_df(top_profits[['original_title', 'budget', 'revenue', 'profit']], 'top_profit_movies.csv')
    print("Top 10 by profit saved to 'top_profit_movies.csv'")
    for _, row in top_profits.head(5).iterrows():
        print(f"{row['original_title']}: ${row['profit']:,}")

# 6. Most frequent directors and actors
def analyze_people(df):
    director_counts = df['director'].value_counts()
    top_director = director_counts.idxmax()
    print(f"Top director: {top_director} ({director_counts.max()} movies)")

    actor_series = df['cast'].str.split('|').explode()
    actor_counts = actor_series.value_counts()
    top_actor = actor_counts.idxmax()
    print(f"Top actor: {top_actor} ({actor_counts.max()} movies)")

# 7. Genre counts
def analyze_genres(df):
    all_genres = df['genres'].str.split('|').explode()
    genre_counts = all_genres.value_counts().reset_index()
    genre_counts.columns = ['genre', 'movie_count']
    save_df(genre_counts, 'genre_counts.csv')
    print("Genre counts saved to 'genre_counts.csv'")
    for _, row in genre_counts.head(3).iterrows():
        print(f"   - {row['genre']}: {row['movie_count']} movies")

# Main runner
if __name__ == "__main__":
    download_data()
    data = load_data()
    print(f"Dataset loaded: {len(data)} movies, {len(data.columns)} columns\n")

    analyze_release_dates(data)
    analyze_high_rated(data)
    analyze_revenue(data)
    calculate_total_revenue(data)
    analyze_profits(data)
    analyze_people(data)
    analyze_genres(data)

    print("\n All analyses complete!")
