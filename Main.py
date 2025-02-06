import joblib
from Functions.Fetch import RealEstateFetcher
from Functions.Preprocess import preprocess_data
from sklearn.ensemble import RandomForestRegressor

# Initialize the RealEstateFetcher class
real_estate_fetcher = RealEstateFetcher()

# Fetch new data and save it to the file (this will handle checking for new ads and saving)
new_data = real_estate_fetcher.fetch_and_exctract_data()

predict_price = new_data[new_data['Is New'] == True]

# Check if the new dataset is empty
if predict_price.empty:
    print("No new data to predict.")
else:
    # Preporocess the data
    predict_price = preprocess_data(predict_price)
    
    X = predict_price[['Size_m2', 'Latitude', 'Longitude', 'Flat Type']] 
    y = predict_price['Price (CZK)']
    
    # Load model 
    model = joblib.load('random_forest_model_compressed.pkl')

    predictions = model.predict(X)

    # Add predictions to the dataset
    predict_price['Predicted Price'] = predictions

    # Filter only observations where the predicted price is lower than the actual price
    price_drops = predict_price[predict_price['Predicted Price'] < predict_price['Price (CZK)']]

    # Return only those observations
    import ace_tools as tools  # Use ace_tools to display DataFrame
    tools.display_dataframe_to_user(name="Predicted Price Drops", dataframe=price_drops)
