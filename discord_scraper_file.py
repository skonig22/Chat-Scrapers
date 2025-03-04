import discord
import os
from dotenv import load_dotenv

# Load enviroment variables
load_dotenv()

token = os.getenv('BOT_TOKEN') 
file_path = "./chat_log.txt"

# Set up Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = f"{message.author}: {message.content}\n"

    with open(file_path, "a") as file:
        file.write(msg)
        print("Wrote msg to file")

client.run(token)
