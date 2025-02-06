import pandas as pd
from Functions.Fetch import fetch_estates_data
from Functions.Preprocess import preprocess_data

df = pd.read_csv('real_estate_prague.csv')

df = preprocess_data(df)
