import requests
import pandas as pd

# Function to fetch estate data for a given category (1 = buy, 2 = rent) and flat type (category_sub_cb)
def fetch_estates_data(category_main_cb, category_sub_cb):
    """Fetch estate data from Sreality API for a specific transaction type and flat type."""
    url = "https://www.sreality.cz/api/cs/v2/estates"
    estates = []  
    page = 1      

    while True:
        params = {
            "category_sub_cb": category_sub_cb,  # Specific flat type
            "locality_region_id": 10,            # Praha (region ID for Prague)
            "category_main_cb": category_main_cb,  # 1 = Buy, 2 = Rent
            "per_page": 20,                      
            "page": page                         
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()  
            current_estates = data['_embedded']['estates']
            if not current_estates:
                break  
            
            estates.extend(current_estates)
            page += 1  
        else:
            print(f"Error fetching data: {response.status_code}")
            break

    return estates

# Define flat types (category_sub_cb) and create an empty list to store all records
flat_types = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16]  
estate_records = []

# Fetch data for both 'buy' and 'rent' for each flat type
for flat_type in flat_types:
    # Fetch estates for sale (category_main_cb=1)
    estates_buy = fetch_estates_data(category_main_cb=1, category_sub_cb=flat_type)
    for estate in estates_buy:
        estate_record = {
            'ID': estate['hash_id'],
            'Name': estate['name'],
            'Price (CZK)': estate['price_czk']['value_raw'],
            'Location': estate['locality'],
            'Latitude': estate['gps']['lat'],
            'Longitude': estate['gps']['lon'],
            'Flat Type': flat_type
        }
        estate_records.append(estate_record)
    
    # Fetch estates for rent (category_main_cb=2)
    estates_rent = fetch_estates_data(category_main_cb=2, category_sub_cb=flat_type)
    for estate in estates_rent:
        estate_record = {
            'ID': estate['hash_id'],
            'Name': estate['name'],
            'Price (CZK)': estate['price_czk']['value_raw'],
            'Location': estate['locality'],
            'Latitude': estate['gps']['lat'],
            'Longitude': estate['gps']['lon'],
            'Flat Type': flat_type
        }
        estate_records.append(estate_record)

# Create a DataFrame 
df = pd.DataFrame(estate_records)

# Save the DataFrame to a CSV file
output_filename = 'real_estate_prague.csv'
df.to_csv(output_filename, index=False, encoding='utf-8')
print(f"Data saved to {output_filename}")

# Print the first few rows
print(df.head())


