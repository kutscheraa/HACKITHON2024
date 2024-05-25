import pandas as pd
from collections import Counter
from paralel import fetch_and_process_dataframes

# Assume dataframes_dict is available from the paralel.py code
dataframes_dict = fetch_and_process_dataframes('mesta.csv')
# Create a new DataFrame to store the results
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

# Print the results
print(results_df)