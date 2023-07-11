import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from wikipediaApi import random_page
import random
import logging

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configure bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Configure /nameme command
@tree.command(name = 'nameme', description = 'Get a random name')
async def nameme_command(interaction):
    if (interaction.channel is None):
        interaction.response.send_message('This command can only be used in a server!')
        return

    # Defer
    await interaction.response.defer()

    # Get random page from Wikipedia
    page = random_page()

    # Get user
    user = interaction.user
    success = True
    try:
        await user.edit(nick=page['title'])
    except:
        success = False

    # Send message
    if success:
        replyMessage = f'Your new name is "{page["title"]}"!'
    else:
        replyMessage = 'Sorry, I couldn\'t change your name, but here\'s a random Wikipedia article anyway!'

    replyEmbed = discord.Embed(
        title=page['title'],
        description=page["extract"],
        color=random.randint(0, 0xFFFFFF),
        url=page['link']
    )

    await interaction.followup.send(content=replyMessage, embed=replyEmbed)

@client.event
async def on_ready():
    # Synchronize commands with Discord
    print('Syncing commands with global scope')
    await tree.sync()

    print(f'{client.user} has connected to Discord!')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
client.run(DISCORD_TOKEN, log_handler=handler)
