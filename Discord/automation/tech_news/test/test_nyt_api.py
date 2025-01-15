import requests
import os

# Ability to use environment variables
from dotenv import load_dotenv
load_dotenv()


# Replace with your actual NYTimes API key
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")

# Function to fetch latest news
def fetch_latest_news():
    url = f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={NYTIMES_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        articles = data.get("results", [])
        
        print("Connection successful! Latest articles:")
        for i, article in enumerate(articles[:5], start=1):  # Show top 5 articles
            print(f"{i}. {article.get('title', 'No Title')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
fetch_latest_news()
