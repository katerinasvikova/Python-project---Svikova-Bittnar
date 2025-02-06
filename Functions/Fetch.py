import requests
import os
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
