import requests
import os
import pandas as pd

class RealEstateFetcher:
    def __init__(self, output_filename='real_estate_prague.csv'):
        """Initialize the RealEstateFetcher class."""
        self.output_filename = output_filename
        self.flat_types = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16]  # Define flat types
        self.estate_records = []  # List to store all records
    
    def fetch_estates_data(self, category_main_cb, category_sub_cb):
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

    def fetch_and_exctract_data(self):
        """Fetch data for both 'buy' and 'rent' for each flat type and preprocess."""
        # Load previous dataset (if exists) to check for new advertisements
        if os.path.exists(self.output_filename):
            prev_df = pd.read_csv(self.output_filename)
            prev_df['Is New'] = False
        else:
            prev_df = pd.DataFrame()  # Empty DataFrame if it's the first fetch

        # Fetch data for both 'buy' and 'rent' for each flat type
        for flat_type in self.flat_types:
            # Fetch estates for sale (category_main_cb=1)
            estates_buy = self.fetch_estates_data(category_main_cb=1, category_sub_cb=flat_type)
            for estate in estates_buy:
                estate_record = {
                    'ID': estate['hash_id'],
                    'Name': estate['name'],
                    'Price (CZK)': estate['price_czk']['value_raw'],
                    'Location': estate['locality'],
                    'Latitude': estate['gps']['lat'],
                    'Longitude': estate['gps']['lon'],
                    'Flat Type': flat_type,
                    'Is New': True  # Mark all fetched estates as new initially
                }
                self.estate_records.append(estate_record)

            # Fetch estates for rent (category_main_cb=2)
            estates_rent = self.fetch_estates_data(category_main_cb=2, category_sub_cb=flat_type)
            for estate in estates_rent:
                estate_record = {
                    'ID': estate['hash_id'],
                    'Name': estate['name'],
                    'Price (CZK)': estate['price_czk']['value_raw'],
                    'Location': estate['locality'],
                    'Latitude': estate['gps']['lat'],
                    'Longitude': estate['gps']['lon'],
                    'Flat Type': flat_type,
                    'Is New': True
                }
                self.estate_records.append(estate_record)

        # Create a DataFrame for new estates
        new_df = pd.DataFrame(self.estate_records)

        # If it's not the first fetch, compare new data with previous data
        if not prev_df.empty:
            # Find common ads (ads that exist in both new_df and prev_df)
            common_ads = prev_df[prev_df['ID'].isin(new_df['ID'])]

            # Find new ads (ads that are in new_df but not in prev_df)
            new_ads = new_df[~new_df['ID'].isin(prev_df['ID'])]

        # Concatenate the new data with the previous data
        combined_df = pd.concat([common_ads, new_ads], ignore_index=True)

        # Remove duplicates in combined data
        combined_df = combined_df.drop_duplicates(subset=['ID'], keep='first')
        
        # Save the combined DataFrame back to the file
        combined_df.to_csv(self.output_filename, index=False, encoding='utf-8')
        print(f"Data saved to {self.output_filename}")

        return combined_df
