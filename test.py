from Functions.Preprocess import preprocess_data
from sklearn.ensemble import RandomForestRegressor

new_data = pd.DataFrame('real_estate_prague_test.csv')

predict_price = new_data[new_data['Is New'] == True]

# Check if the new dataset is empty
if predict_price.empty:
    print("No new data to predict.")
else:
    # Preporocess the data
    predict_price = preprocess(predict_price)
    
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
    X_retrain = new_data[['Size_m2', 'Latitude', 'Longitude', 'Flat Type']]
    y_retrain = predict_price['Price (CZK)']

    X_train, X_test, y_train, y_test = train_test_split(X_retrain, y_retrain, test_size = 0.2, random_state = 42)
    
    new_model = RandomForestRegressor(n_estimators = 1000,
                                      random_state = 42,
                                      max_depth = 10,
                                      min_samples_split = 5
                                     )
    new_model.train(X_train, y_train)

    print(price_drops)
