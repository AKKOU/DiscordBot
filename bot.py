import discord
import asyncio
from discord.ext import commands
import discord.state
import os
from dotenv import load_dotenv
from colorama import Fore, Style

intent = discord.Intents.all()
intent.message_content = True
bot = commands.Bot(command_prefix="$",intents=intent)

load_dotenv()

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"載入 {len(slash)} 個斜線指令")
    game = discord.Game('把腳放頭上賺$100中')
    await bot.change_presence(status=discord.Status.online,activity=game)
    print(Fore.GREEN + f"機器人啟動成功，目前登入用戶身分:{bot.user}" + Style.RESET_ALL)
    print("---------------------------------------------------------\n")

@bot.command()
async def load(ctx,extension):
    try:
        if ctx.author.id == 426362947015540746:
            await bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Loaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error:{e}")
@bot.command()
async def unload(ctx,extension):
    try:
        if ctx.author.id == 426362947015540746:
            await bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Unloaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error:{e}")
@bot.command()
async def reload(ctx,extension):
    try:
        if ctx.author.id == 426362947015540746:
            await bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"Reloaded {extension} done.")
    except Exception as e:
        await ctx.send(f"Error:{e}")    

async def load_extension():
    # for file in os.listdir("/home/ubuntu/akou/discordbot/cogs"): #linux
    for file in os.listdir("Z:\DiscordBot\cogs"): #windows
        if(file.endswith(".py")):
            print(f"載入檔案:{file}..")
            await bot.load_extension(f"cogs.{file[:-3]}")
async def main():
    async with bot:
        await load_extension()
        await bot.start(os.environ['TOKEN'])

if __name__ == "__main__":
    asyncio.run(main())