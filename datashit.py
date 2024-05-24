import requests
import pandas as pd

def fetch_data(url):
    """
    Fetches data from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict or None: The fetched data as a dictionary, or None if failed.
    """
    try:
        if url == 'null':
            print("URL not available for this city.")
            return None
        else:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to retrieve data from the URL:", url)
                return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def process_data(data):
    """
    Processes the fetched data and returns it as a pandas DataFrame.

    Args:
        data (dict): The fetched data.

    Returns:
        pandas.DataFrame or None: The processed data as a DataFrame, or None if no data to process.
    """
    if data:
        informace = data.get('informace', [])
        df = pd.DataFrame(informace)
        return df
    else:
        print("No data to process.")
        return None

def fetch_data_from_dataframe(df):
    """
    Fetches and processes data from a pandas DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing URLs.

    Returns:
        pandas.DataFrame or None: The DataFrame with processed data added, or None if failed.
    """
    try:
        for index, row in df.iterrows():
            url = row['url']
            data = fetch_data(url)
            if data:
                df.loc[index, 'data'] = process_data(data)
        return df
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def fetch_and_process_data(url_or_df):
    """
    Fetches and processes data from a URL or a pandas DataFrame.

    Args:
        url_or_df (str or pandas.DataFrame): The URL string or DataFrame containing URLs.

    Returns:
        pandas.DataFrame or None: The DataFrame with processed data added, or None if failed.
    """
    if isinstance(url_or_df, str):
        data = fetch_data(url_or_df)
        if data:
            return process_data(data)
    elif isinstance(url_or_df, pd.DataFrame):
        return fetch_data_from_dataframe(url_or_df)
    else:
        print("Invalid input type. Please provide a URL string or a DataFrame.")
        return None

# Example usage
if __name__ == "__main__":
    # Example with URL string
    example_url = 'https://www.benesov-city.cz/opendata-uredni-deska'
    processed_data_url = fetch_and_process_data(example_url)
    print("Processed data from URL:")
    print(processed_data_url)
    print()

    # Example with DataFrame
    example_df = pd.DataFrame({'mesto': ['Benešov'], 'url': [example_url]})
    processed_data_df = fetch_and_process_data(example_df)
    print("Processed data from DataFrame:")
    print(processed_data_df)

