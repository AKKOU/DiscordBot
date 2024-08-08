import discord
import asyncio
import datetime
from discord.ext import commands
from discord import app_commands
from typing import Optional
from colorama import Fore, Style

class Main(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    #斜線指令
    @app_commands.command(name="hello",description="hello world")
    async def hello(self, interaction:discord.Interaction):
        guild = "私人" if interaction.guild==None else interaction.guild
        channel = "訊息" if interaction.guild==None else interaction.channel
        print(Fore.GREEN + f"[{datetime.datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 斜線指令(Hello World)" + Style.RESET_ALL)
        await interaction.response.send_message("Hello there!")

    @app_commands.command(name="say",description="Say it for me")
    async def say(self,interaction:discord.Interaction,text:str):
        guild = "私人" if interaction.guild==None else interaction.guild
        channel = "訊息" if interaction.guild==None else interaction.channel
        print(Fore.GREEN + f"[{datetime.datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 斜線指令(Say)" + Style.RESET_ALL)
        await interaction.response.send_message(text)

    #字串偵測
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        guild = "私人" if message.guild==None else message.guild
        channel = "訊息" if message.guild==None else message.channel
        if message.author.id!=1099679926518546516:
            if message.attachments:
                for attachment in message.attachments:
                    if(message.content):
                        print(Fore.YELLOW + f"[{datetime.datetime.now()}] [{guild}的{channel}] {message.author}: {message.content}" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"[{datetime.datetime.now()}] [{guild}的{channel}] {message.author}: ({attachment.content_type})" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"[{datetime.datetime.now()}] [{guild}的{channel}] {message.author}: {message.content}" + Style.RESET_ALL)

        if message.author == self.bot.user:
            return
        if self.bot.user in message.mentions:
            await message.channel.send("?")
        elif message.content == "早安":
            await message.channel.send("早安吃雞雞")
        elif message.content == "nick":
            tmp = await message.channel.send("小雞雞")
            await asyncio.sleep(2)
            await tmp.delete()
        elif "你娘" in message.content:
            await message.delete()
            await message.channel.send("嘴巴臭臭：(")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            guild = "私人" if message.guild==None else message.guild
            channel = "訊息" if message.guild==None else message.channel
            print(Fore.RED + f"[{datetime.datetime.now()}][{guild}的{channel}] {message.author}: {message.content}(已刪除)" + Style.RESET_ALL)

async def setup(bot:commands.Bot):
    await bot.add_cog(Main(bot))