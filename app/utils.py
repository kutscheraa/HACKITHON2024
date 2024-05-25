import requests
import pandas as pd
from tqdm import tqdm
from collections import Counter
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

URLS_PATH = 'mesta.csv'
THREADS = 16

# Získávání dat z api
def fetch_data(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    print(f"Nastala chyba při volání GET requestu na URL: {url}")        

# Zpracování JSON souboru a vytvoření dataframu
def process_data(data):
    informace = data.get('informace', [])
    selected_data = []

    for item in informace:
        pdf_link = ""
        if not item.get('dokument'):
            dokument = ""
            dokument_info = ""
        else:
            dokument = item['dokument'][0]
            dokument_info = f"{dokument.get('název', {}).get('cs', '')}"
            pdf_link = dokument.get('url', '')

        selected_data.append({
            'název': item.get('název', {}).get('cs', ''),
            'datum_vyvěšení': item.get('vyvěšení', {}).get('datum', ''),
            'dokument': dokument_info,
            'pdf_link': pdf_link
        })

    return pd.DataFrame(selected_data) if selected_data else None

# Získání a zpracování dat
def fetch_and_process(city, url):
    data = fetch_data(url)
    df = process_data(data)
    return city, df

# Vytvoření slovníku kde klíč je město a hodnota je pandas dataframe
def create_dict(csv_file, threads=32):
    cities = {}
    df = pd.read_csv(csv_file)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_city = {
            executor.submit(fetch_and_process, row['mesto'], row['url']): row['mesto']
            for _, row in df.iterrows() if row['url'] and row['url'] != 'null'
        }
        
        for future in tqdm(as_completed(future_to_city), total=len(future_to_city), desc="Stahování dat"):
            city, city_df = future.result()
            if city_df is not None:
                cities[city] = city_df
    
    return cities

# Spočítání základních statistik dle zjištěných hodnot
def city_stats(dict):
    results_df = pd.DataFrame(columns=['City', 'Average Monthly Frequency', 'Most Used Word'])

    # Iterate over the city DataFrames
    for city, df in dict.items():
        df['datum_vyvěšení'] = pd.to_datetime(df['datum_vyvěšení'])
        names = df['název'].str.lower()
        
        # Průměrná měsíční frekvence
        avg_monthly_freq = len(names) / len(df['datum_vyvěšení'].dt.to_period('M').unique())
        
        # Nejpoužívanější slovo delší než 3 znaky
        word_counts = Counter(word for name in names for word in name.split() if len(word) > 3)
        most_used_word = word_counts.most_common(1)[0][0]
        
        # Přidání výsledků do pandas dataframu
        results_df = pd.concat([results_df, pd.DataFrame.from_records([{'City': city, 'Average Monthly Frequency': avg_monthly_freq, 'Most Used Word': most_used_word}])], ignore_index=True)
    return results_df


if __name__ == "__main__":
    dataframes_dict = create_dict(URLS_PATH, THREADS)
    print("Výsledek")
    for city, df in dataframes_dict.items():
        print(f"Město {city}")
        print(df.head(3))
        print("\n")
