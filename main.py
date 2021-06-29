import os
import discord
from discord.ext import commands
from discordTogether import DiscordTogether

client = commands.Bot(command_prefix=".")
togetherControl = DiscordTogether(client)
client.remove_command('help')
@client.event
async def on_ready():
    print(f"Bot logged into {client.user}.")
    print("Ready")
    await client.change_presence(
        activity=discord.Game(f" .help in {len(client.guilds)} servers"))

@client.command()
async def youtube(ctx):
    link = await togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click The Link! \n{link}")

@client.event
async def on_command_error(ctx ,error ):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You need to be in your selected voice channel first")


@client.command()
async def help(ctx):
    await ctx.send("Use .youtube in your selected voice channel (Only Works on PC for Now")

@client.command()
async def invite(ctx):
    await ctx.send("[Click Here to Invite the bot!](https://discord.com/api/oauth2/authorize?client_id=859365742457389106&permissions=2182138176&scope=bot%20applications.commands)")




client.run(f"{os.environ['TOKEN']}")

