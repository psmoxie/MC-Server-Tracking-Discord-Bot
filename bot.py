import os
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


def get_minecraft_status(ip: str):
    url = f"https://api.mcsrvstat.us/3/{ip}"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return None
        return res.json()
    except requests.RequestException:
        return None


@bot.command()
async def smpstatus(ctx):
    ip = "174.115.206.194"
    data = get_minecraft_status(ip)

    if not data:
        await ctx.send("Couldn't reach the server status API.")
        return

    online = data.get("online", False)

    if online:
        embed = discord.Embed(
            title="🟢 Server Online",
            description=f"IP: {ip}\nhttps://mcsrvstat.us/server/{ip}",
            color=0x2ecc71
        )
    else:
        embed = discord.Embed(
            title="🔴 Server Offline",
            description=f"IP: {ip}\nhttps://mcsrvstat.us/server/{ip}",
            color=0xe74c3c
        )

    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    await ctx.send("hello")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} server(s)")


bot.run(TOKEN)