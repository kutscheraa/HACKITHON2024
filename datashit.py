import requests
import pandas as pd
from tqdm import tqdm
import urllib3

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
                print("Failed to retrieve data from the URL:", url)
                return None
    except Exception as e:
        print("An error occurred:", str(e))
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
        selected_data = [{'název': item.get('název', {}).get('cs', ''),
                          'datum_vyvěšení': item.get('datum_vyvěšení', '')}
                         for item in informace]
        df = pd.DataFrame(selected_data)
        return df
    else:
        print("No data to process.")
        return None

def fetch_and_process_dataframes(csv_file):
    """
    Fetches and processes data from a CSV file and returns a dictionary of DataFrames with selected columns.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        dict: A dictionary where keys are city names and values are DataFrames with corresponding data.
    """
    city_dataframes = {}

    # Read data from the CSV file
    df = pd.read_csv(csv_file)
    
    # Iterate over rows in the CSV file with a progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Nacitam data z..."):
        city = row['mesto']
        url = row['url']
        
        # Fetch and process data from URL
        data = fetch_data(url)
        if data:
            df = process_data(data)
            if df is not None:
                city_dataframes[city] = df
    
    return city_dataframes

# Function call to fetch and process data from the CSV file
dataframes_dict = fetch_and_process_dataframes('mesta.csv')

# Print the dictionary of DataFrames
print("Dictionary of DataFrames:")
for city, df in dataframes_dict.items():
    print(f"City: {city}")
    print(df)
    print("\n")
