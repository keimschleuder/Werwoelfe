from Token.Token import TOKEN as token
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="dir zu")
bot = commands.Bot(command_prefix = "!", activity=activity, intents = intents, status=discord.Status.online)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

bot.run(token)
