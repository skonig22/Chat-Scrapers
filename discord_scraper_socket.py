import discord
import os
import socket
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Network variables
HOST = '0.0.0.0'
PORT = 8080

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True 

discord_client = discord.Client(intents=intents)

# Global client socket
connected_client = None

def start_socket_server():
    # Blocking function to start the socket server and wait for a client
    global connected_client
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing port

    try:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Socket server listening on {HOST}:{PORT}...")

        # Accept a single client connection and store it
        connected_client, addr = server.accept()
        print(f"Client connected from {addr}")

    except OSError as e:
        print(f"Error: {e}. Is the port in use?")
        return

async def send_to_client(message):
    
    global connected_client
    if connected_client:
        try:
            connected_client.sendall(message.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            print("Client disconnected. Waiting for a new connection...")
            connected_client = None  # Reset the client socket

@discord_client.event
async def on_ready():
    print(f"Logged in as {discord_client.user}")

@discord_client.event
async def on_message(message):
    # Handles messages received from Discord
    if message.author == discord_client.user:
        return  # Ignore bot's own messages

    msg = f"{message.author}: {message.content}\n"
    print("Received Discord message:", msg)

    # Send message to the connected client
    await send_to_client(msg)

async def main():
    # First run the socket server until client accepted, then start the Discord bot
    loop = asyncio.get_running_loop()

    # Run the blocking socket server in a separate thread
    await loop.run_in_executor(None, start_socket_server)

    # Start the Discord bot
    await discord_client.start(TOKEN)

# Run the bot
asyncio.run(main())
