import joblib
import pandas as pd

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

    # Retraining the random forest
    X_train = predict_price[['Size_m2', 'Latitude', 'Longitude', 'Flat Type']]
    y_train = predict_price['Price (CZK)']

    new_model = RandomForestRegressor(n_estimators = 1000,
                                      random_state = 42,
                                      max_depth = 10,
                                      min_samples_split = 5
                                     )
    new_model.fit(X_train, y_train)

    joblib.dump(new_model, 'random_forest_model_compressed.pkl', compress=3)

    print(price_drops)

    print(f'You have {price_drops.shape[0]} new flat advertisements with predicted market value above listing price. For details see the table above.')
