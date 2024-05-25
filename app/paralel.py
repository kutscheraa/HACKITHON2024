import requests
import pandas as pd
from tqdm import tqdm
from collections import Counter
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

def fetch_data(url):
    try:
        if not url or url == 'null':
            return None
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

def process_data(data):
    if not data:
        return None
    
    informace = data.get('informace', [])
    selected_data = []

    for item in informace:
        if not item.get('dokument'):
            continue
        dokument = item['dokument'][0]
        dokument_info = f"{dokument.get('název', {}).get('cs', '')}"
        pdf_link = dokument.get('url', '')

        if pdf_link:
            selected_data.append({
                'název': item.get('název', {}).get('cs', ''),
                'datum_vyvěšení': item.get('vyvěšení', {}).get('datum', ''),
                'dokument': dokument_info,
                'pdf_link': pdf_link
            })

    return pd.DataFrame(selected_data) if selected_data else None

def fetch_and_process_data(city, url):
    data = fetch_data(url)
    df = process_data(data)
    return city, df

def fetch_and_process_dataframes(csv_file, max_workers=20):
    city_dataframes = {}

    df = pd.read_csv(csv_file)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_city = {
            executor.submit(fetch_and_process_data, row['mesto'], row['url']): row['mesto']
            for _, row in df.iterrows() if row['url'] and row['url'] != 'null'
        }
        
        for future in tqdm(as_completed(future_to_city), total=len(future_to_city), desc="Nacitam data z..."):
            city, city_df = future.result()
            if city_df is not None:
                city_dataframes[city] = city_df
    
    return city_dataframes

def df_stats(dataframes_dict):
    results_df = pd.DataFrame(columns=['City', 'Average Monthly Frequency', 'Most Used Word'])

    # Iterate over the city DataFrames
    for city, df in dataframes_dict.items():
        # Convert 'datum_vyvěšení' column to datetime type
        df['datum_vyvěšení'] = pd.to_datetime(df['datum_vyvěšení'])
        
        # Extract the 'název' column and convert to lowercase
        names = df['název'].str.lower()
        
        # Calculate the average monthly frequency
        avg_monthly_freq = len(names) / len(df['datum_vyvěšení'].dt.to_period('M').unique())
        
        # Find the most used word (longer than 3 characters)
        word_counts = Counter(word for name in names for word in name.split() if len(word) > 3)
        most_used_word = word_counts.most_common(1)[0][0]
        
        # Add the results to the new DataFrame
        results_df = pd.concat([results_df, pd.DataFrame.from_records([{'City': city, 'Average Monthly Frequency': avg_monthly_freq, 'Most Used Word': most_used_word}])], ignore_index=True)

    return results_df

# Function call to fetch and process data from the CSV file
dataframes_dict = fetch_and_process_dataframes('mesta.csv', 20)

# Print the dictionary of DataFrames and datum_vyvěšení for debugging purposes
print("Dictionary of DataFrames:")
for city, df in dataframes_dict.items():
    print(f"City: {city}")
    print(df)
    print("\n")
