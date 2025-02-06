# Python-project---Svikova-Bittnar
This project analyzes real estate prices in Prague, focusing on the purchase of flats. The primary data source is Sreality.cz, from which we collect information on flat prices, locations, and sizes.

The dataset is dynamic, meaning that each time the code is executed, it automatically fetches the latest data from the website and highlights new flat listings. These newly added listings are then analyzed using a Random Forest model. Initially, the model is trained on a base dataset, but it is continually retrained as new data is collected, allowing it to improve over time.

Users can specify parameters for the flats they are interested in, such as size or location. The application compares the predicted price with the actual listing price and recommends flats that are priced lower than the model's predicted price, indicating they may be good opportunities for purchase.
