import os
import discord
from discord.ext import commands
from discordTogether import DiscordTogether

client = commands.Bot(command_prefix="yt!")
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
    embed=discord.Embed(color=0xd80e0e)
    embed.set_author(name="Youtube Together", icon_url="https://cdn.discordapp.com/avatars/859365742457389106/8f7e3878218059b90db2868f194413fd.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/859365742457389106/8f7e3878218059b90db2868f194413fd.png")
    embed.add_field(name="Watch Youtube", value=f"[Click Here]({link})", inline=False)
    embed.set_footer(text="Only Works in PC for now :( ")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx ,error ):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You need to be in your selected voice channel first")


@client.command()
async def help(ctx):
    await ctx.send("""
Use yt!youtube in your selected voice channel (Only Works on PC for Now)
Use yt!invite for the invite link""")

@client.command()
async def invite(ctx):
    embed=discord.Embed(color=0xd80e0e)
    embed.set_author(name="Youtube Together", icon_url="https://cdn.discordapp.com/avatars/859365742457389106/8f7e3878218059b90db2868f194413fd.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/859365742457389106/8f7e3878218059b90db2868f194413fd.png")
    embed.add_field(name="Invite The Bot ", value="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=859365742457389106&permissions=2182138176&scope=bot%20applications.commands)  |  [Support Server](https://discord.gg/gVFxdXdjnd)", inline=False)
    embed.set_footer(text="-Bot Devs")
    await ctx.send(embed=embed)



@client.event
async def on_guild_join(guild):

    name = str(guild.name)
    description = str(guild.description)

    owner = str(guild.owner)
    id = str(guild.id)
    region = str(guild.region)
    memberCount = str(guild.member_count)

    icon = str(guild.icon_url)

    embed = discord.Embed(
        title=" Joined a server",
        description=description,
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server Name", value=name, inline=False)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    log_channel = client.get_channel(832944803338911765)
    await log_channel.send(embed=embed)
    await client.change_presence(
    activity=discord.Game(f" .help in {len(client.guilds)} servers"))



@client.event
async def on_guild_remove(guild):

    name = str(guild.name)
    description = str(guild.description)

    owner = str(guild.owner)
    id = str(guild.id)
    region = str(guild.region)
    memberCount = str(guild.member_count)

    icon = str(guild.icon_url)

    embed = discord.Embed(
        title=" Left a Server ",
        description=description,
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server Name", value=name, inline=False)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    log_channel = client.get_channel(832944803338911765)
    await log_channel.send(embed=embed)
    await client.change_presence(
    activity=discord.Game(f" .help in {len(client.guilds)} servers"))

client.run(f"{os.environ['TOKEN']}")

