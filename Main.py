from Functions.Fetch import fetch_estates_data
from Functions.Preprocess import preprocess_data
from sklearn.ensemble import RandomForestRegressor

# Initialize the RealEstateFetcher class
real_estate_fetcher = RealEstateFetcher()

# Fetch new data and save it to the file (this will handle checking for new ads and saving)
new_data = real_estate_fetcher.fetch_and_save_data()

predict_price = new_data[new_data['Is New'] == True]


# Preporocess the data
predict_price = preprocess(predict_price)


X = predict_price[['Size_m2', 'Latitude', 'Longitude', 'Flat Type']] 
y = predict_price['Price (CZK)']

# Load model 
model = joblib.load('linear_regression_model.pkl')
