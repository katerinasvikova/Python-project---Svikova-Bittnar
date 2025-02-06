import pandas as pd
from Functions.Fetch import RealEstateFetcher
from Functions.Preprocess import preprocess_data

df = pd.read_csv('real_estate_prague.csv')

df = preprocess_data(df)

# Initialize the RealEstateFetcher class
real_estate_fetcher = RealEstateFetcher()

# Fetch new data and save it to the file (this will handle checking for new ads and saving)
new_data = real_estate_fetcher.fetch_and_save_data()

# Optionally, display the first few rows of the fetched data
print(new_data.head())
