import os
from dotenv import load_dotenv
import requests
import discord
from discord.ext import commands
from discord import Intents

# Load .env file
load_dotenv()

# Environment variables
NYTIMES_API_KEY = os.getenv('NYTIMES_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# Ensure the channel ID is valid
if DISCORD_CHANNEL_ID is None:
    raise ValueError("DISCORD_CHANNEL_ID is missing in the environment variables.")
else:
    DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID)

# Fetch latest tech news from NYTimes
def fetch_latest_news():
    url = f"https://api.nytimes.com/svc/topstories/v2/technology.json?api-key={NYTIMES_API_KEY}"  # Technology section
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("results", [])
        filtered_articles = filter_articles(articles)  # Filter based on specific topics
        return filtered_articles
    else:
        raise Exception("Failed to fetch news")

# Filter articles based on specific topics
def filter_articles(articles):
    keywords = ['vulnerabilities', 'cybersecurity', 'gadget', 'tech', 'UX', 'design', 'mobile devices updates', 'ios updates', 'android updates']
    filtered = []
    for article in articles:
        title = article.get('title', '').lower()
        abstract = article.get('abstract', '').lower()
        if any(keyword in title or keyword in abstract for keyword in keywords):
            filtered.append(article)
    return filtered[:5]  # Limit to top 5 relevant articles

# Send news to Discord
def format_message(articles):
    message = "**Latest Tech News:**\n"
    for article in articles:
        title = article.get('title', 'No Title')
        url = article.get('url', 'No URL')
        message += f"- [{title}]({url})\n"
    return message

# Enable the intents you need
intents = Intents.default()
intents.members = True  # Enable the "Server Members Intent"
intents.message_content = True  # Enable the "Message Content Intent"

# Create the bot with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    
    # Check if the bot is connected to any guilds (servers)
    if not bot.guilds:
        print("The bot is not connected to any servers.")
        return
    
    # Print the names of all servers the bot is in
    for guild in bot.guilds:
        print(f"Bot is in the server: {guild.name} (ID: {guild.id})")
        
    # Get the channel by ID
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        print(f"Could not find the channel with ID {DISCORD_CHANNEL_ID}.")
        return
    
    print(f"Found channel: {channel.name}")
    articles = fetch_latest_news()
    message = format_message(articles)
    await channel.send(message)
    print("Message sent successfully!")
    
    await bot.close()


# Run bot
bot.run(DISCORD_TOKEN)
