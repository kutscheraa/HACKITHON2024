import requests
import urllib3
import pandas as pd

# Pro Linux distribuce
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
    Processes the fetched data and returns a DataFrame.

    Args:
        data (dict): The fetched data.

    Returns:
        pandas.DataFrame or None: The processed data as a DataFrame, or None if there is no data.
    """
    if data:
        informace = data['informace']
        
        df = pd.DataFrame(informace)
        return df
    else:
        print("No data to process.")
        return None

def fetch_and_process_dataframes(csv_file):
    """
    Fetches and processes data from URLs provided in a CSV file and returns a dictionary of DataFrames.

    Args:
        csv_file (str): The path to the CSV file containing 'mesto' and 'url' columns.

    Returns:
        dict: A dictionary where keys are city names and values are DataFrames with corresponding data.
    """
    city_dataframes = {}

    try:
        # Read data from the CSV file
        df = pd.read_csv(csv_file)
        
        # Iterate over rows in the CSV file
        for index, row in df.iterrows():
            city = row['mesto']
            url = row['url']
            
            # Fetch data from URL
            data = fetch_data(url)

            print('\x1b[2K', end= '\r')
            print(f'\rZískávám data města {city} z {url}', end='')

            if data:
                # Process data and add it to the dictionary
                df = process_data(data)
                if df is not None:
                    city_dataframes[city] = df
    except Exception as e:
        print("An error occurred:", str(e))

    return city_dataframes

# Example usage:
if __name__ == "__main__":
    csv_file_path = 'mesta.csv'
    dataframes_dict = fetch_and_process_dataframes(csv_file_path)
    print(dataframes_dict)
