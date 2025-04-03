import json
import re
from collections import Counter
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import numpy as np
import nltk
nltk.download('stopwords')

# Load the collected data from the JSON file
with open('ksu1000.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract emails and count their frequencies
emails = [email for item in data for email in item['emails']]
email_counts = Counter(emails)

# Print email statistics
print("Email Statistics:")
print(f"Total unique email addresses: {len(email_counts)}")
print("Top ten most frequent email addresses:")
for email, count in email_counts.most_common(10):
    print(f"\t({email}, {count})")

# Remove stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
filtered_words = [word for item in data for word in item['body'].split() if word.lower() not in stop_words and word not in punctuation]

# Count word frequencies (before removing stopwords and punctuation)
word_counts_before = Counter(filtered_words)

# Sort word counts by frequency
sorted_word_counts_before = sorted(word_counts_before.items(), key=lambda x: x[1], reverse=True)

# Create a list of ranks and counts for the log-log plot
ranks_before = np.arange(1, len(sorted_word_counts_before) + 1)
counts_before = [item[1] for item in sorted_word_counts_before]

# Plot and save the word frequency ranking (before removing stopwords and punctuation)
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.plot(ranks_before, counts_before, marker='.', linestyle='None')
plt.title('Word Frequency Ranking (Before Removing Stopwords and Punctuation)')
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.savefig('word_frequency_ranking_before.jpg', dpi=300)

# Remove stopwords and punctuation and count word frequencies again
filtered_words = [word for word in filtered_words if len(word) > 1]  # Remove single-character words

# Count word frequencies (after removing stopwords and punctuation)
word_counts_after = Counter(filtered_words)

# Sort word counts by frequency
sorted_word_counts_after = sorted(word_counts_after.items(), key=lambda x: x[1], reverse=True)

# Create a list of ranks and counts for the log-log plot
ranks_after = np.arange(1, len(sorted_word_counts_after) + 1)
counts_after = [item[1] for item in sorted_word_counts_after]

# Plot and save the word frequency ranking (after removing stopwords and punctuation)
plt.subplot(122)
plt.plot(ranks_after, counts_after, marker='.', linestyle='None')
plt.title('Word Frequency Ranking (After Removing Stopwords and Punctuation)')
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.savefig('word_frequency_ranking_after.jpg', dpi=300)

plt.tight_layout()
plt.show()

# Print statistics
print("Word Frequency Rankings (Before and After Removing Stopwords and Punctuation):")
print(f"{'Rank':<7}{'Term':<20}{'Freq (Before)':<15}{'Freq (After)':<15}")
print("-" * 57)
for i in range(30):
    term_before, freq_before = sorted_word_counts_before[i]
    term_after, freq_after = sorted_word_counts_after[i]
    print(f"{i+1:<7}{term_before:<20}{freq_before:<15}{freq_after:<15}")
