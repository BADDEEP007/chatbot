import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


# Convert to DataFrame
df = pd.read_csv('data/1_movies_per_genre/Action.csv')

# Function to fetch review text from an IMDb review page
def fetch_review(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all review texts on the page
        reviews = soup.find_all('div', class_='text show-more__control')
        
        # Join all reviews into a single string
        review_texts = "\n".join([review.get_text() for review in reviews])
        
        return review_texts if review_texts else "No reviews found"
    
    except Exception as e:
        print(f"Error fetching {link}: {e}")
        return None
    
movie_reviews = {}

# # Iterate over each movie in the DataFrame
# for index, row in df.iterrows():
#     movie_name = row['name']
#     review_url = row['review_url']
    
#     # Fetch the review for each movie
#     review_text = fetch_review(review_url)
    
#     # Add to the dictionary with movie name as the key
#     movie_reviews[movie_name] = review_text

# Write the dictionary to a JSON file
with open('reviews.txt', 'w') as f:
    json.dump(df['review_url'].apply(fetch_review) ,f, indent=4)

print("Reviews successfully scraped and saved to movie_reviews.json.")


