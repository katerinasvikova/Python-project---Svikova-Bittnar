import pandas as pd  
import re

df = pd.read_csv('real_estate_prague.csv')

def preprocess_data(data):
        
    # Extract the size of the flat from the 'Name' column
    data['Size_m2'] = data['Name'].apply(lambda x: int(re.findall(r'(\d+)\s*m²', x)[0]) if re.findall(r'(\d+)\s*m²', x) else None)

    # Remove zero-price flats
    def remove_zero_price_flat(data):
        if (data['Price (CZK)'] == 0).any():
            data = data[data['Price (CZK)'] != 0]
            print("Zero-price flats have been removed.")
        else:
            print("No zero-price flats found.")
        data = data.reset_index(drop=True)
        
        return data

    data = remove_zero_price_flat(data)
    
    # Split the 'Location' into District and Municipal Part
    data['Prague_district'] = data['Location'].str.extract(r'Praha\s*(\d+)')
    #data['Municipal_part'] = data['Location'].str.extract(r' - (.*)') - we dont need this in our analysis
    
    # Create a new column 'Sale_or_Rent'
    data['Sale_or_Rent'] = data['Name'].apply(lambda x: 'Sale' if 'Prodej' in x else 'Rent')
    
    # Extract flat type (e.g., '1+kk', '2+1')
    #data['Flat'] = data['Name'].str.extract(r'(\d+\+kk|\d+\+1)') - we dont need this in our analysis
    #data['Flat'].fillna('6+1 or more', inplace=True)

    data = data.drop('Name', axis=1)
    data = data.drop('Location', axis=1)

    # Check for missing values and handle zero prices
    def check_missing_values(data):
        # Check for missing values in all columns
        for column in data.columns:
            missing_values = data[column].isna().sum()
            if missing_values > 0:
                print(f"Column '{column}' has {missing_values} missing values.")
    
    check_missing_values(data)
    
    return data

# Preprocessing of our data
df = preprocess_data(df)

#dropping missing values
df = df.dropna()

print(df.head())



