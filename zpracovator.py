import re
import pandas as pd
from collections import Counter
from paralel import fetch_and_process_dataframes

# Function to extract words from text and count their frequencies
def extract_and_count_words(text):
    # Use regular expression to find words (ignoring punctuation and non-word characters)
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out words with fewer than three letters
    words = [word for word in words if len(word) >= 3]
    # Count the frequencies of words
    return Counter(words)

# Function call to fetch and process data from the CSV file with additional info
dataframes_dict = fetch_and_process_dataframes('mesta.csv', 20)

# Initialize a dictionary to store the most frequent keyword per city
most_used_keyword_per_city = {}
# Initialize a dictionary to store the frequency of updates per city
updates_frequency_per_city = {}

# Iterate over the dictionary of DataFrames
for city, df in dataframes_dict.items():
    # Extract and count words for each announcement in the city
    word_counts = Counter()
    for _, row in df.iterrows():
        word_counts.update(extract_and_count_words(row['název']))
    # Calculate the most frequent keyword for the city
    most_used_keyword_per_city[city] = word_counts.most_common(1)[0][0] if word_counts else None
    # Calculate the frequency of updates (number of posts)
    updates_frequency_per_city[city] = len(df)

# Convert the dictionaries to DataFrames
most_used_keyword_df = pd.DataFrame(most_used_keyword_per_city.items(), columns=['City', 'Most Used Keyword'])
updates_frequency_df = pd.DataFrame(updates_frequency_per_city.items(), columns=['City', 'Updates Frequency'])

# Merge the DataFrames on the 'City' column
combined_df = pd.merge(most_used_keyword_df, updates_frequency_df, on='City')

# Sort the DataFrame by 'Updates Frequency' column in descending order
combined_df = combined_df.sort_values(by='Updates Frequency', ascending=False)

# Print the combined DataFrame
print("Combined DataFrame:")
print(combined_df)
