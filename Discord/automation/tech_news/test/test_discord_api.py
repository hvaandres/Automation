import discord
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()  # Use default intents
intents.messages = True  # Ensure message-related intents are enabled

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Run the client
client.run(DISCORD_TOKEN)
