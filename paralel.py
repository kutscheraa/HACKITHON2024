import requests
import pandas as pd
from tqdm import tqdm
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

def fetch_data(url):
    """
    Fetches data from the given URL.

    Args:
        url (str): The URL from which to fetch the data.

    Returns:
        dict or None: The fetched data as a dictionary, or None if fetching failed.
    """
    try:
        if url == 'null':
            print("URL not available for this city.")
            return None
        else:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Failed to retrieve data from the URL: {url}, Status Code: {response.status_code}")
                return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def process_data(data):
    """
    Processes the fetched data and returns a DataFrame with selected columns.

    Args:
        data (dict): The fetched data.

    Returns:
        pandas.DataFrame or None: The processed data as a DataFrame, or None if there is no data.
    """
    if data:
        informace = data.get('informace', [])
        selected_data = []

        for item in informace:
            dokument_info = ''
            if item.get('dokument'):
                dokument = item.get('dokument')[0]
                dokument_info = f"{dokument.get('název', {}).get('cs', '')} ({dokument.get('url', '')})"
                
            selected_data.append({
                'název': item.get('název', {}).get('cs', ''),
                'datum_vyvěšení': item.get('vyvěšení', {}).get('datum', ''),
                'dokument': dokument_info
            })

        df = pd.DataFrame(selected_data)
        return df
    else:
        print("No data to process.")
        return None

def fetch_and_process_data(city, url):
    """
    Fetches and processes data for a given city and URL.

    Args:
        city (str): The name of the city.
        url (str): The URL to fetch the data from.

    Returns:
        tuple: A tuple containing the city name and the processed DataFrame.
    """
    data = fetch_data(url)
    if data:
        df = process_data(data)
        if df is not None:
            return city, df
    return city, None

def fetch_and_process_dataframes(csv_file, max_workers=10):
    """
    Fetches and processes data from a CSV file and returns a dictionary of DataFrames with selected columns.

    Args:
        csv_file (str): The path to the CSV file.
        max_workers (int): The maximum number of threads to use for concurrent fetching.

    Returns:
        dict: A dictionary where keys are city names and values are DataFrames with corresponding data.
    """
    city_dataframes = {}

    # Read data from the CSV file
    df = pd.read_csv(csv_file)
    
    # Use ThreadPoolExecutor to fetch data concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_city = {executor.submit(fetch_and_process_data, row['mesto'], row['url']): row['mesto'] for _, row in df.iterrows()}
        
        for future in tqdm(as_completed(future_to_city), total=len(future_to_city), desc="Nacitam data z..."):
            city, city_df = future.result()
            if city_df is not None:
                city_dataframes[city] = city_df
    
    return city_dataframes

# Function call to fetch and process data from the CSV file
dataframes_dict = fetch_and_process_dataframes('mesta.csv', 16)

# Print the dictionary of DataFrames and datum_vyvěšení for debugging purposes
print("Dictionary of DataFrames:")
for city, df in dataframes_dict.items():
    print(f"City: {city}")
    print(df)
    # for _, row in df.iterrows():
    #     print(f"Datum vyvěšení: {row['datum_vyvěšení']}")
    print("\n")
