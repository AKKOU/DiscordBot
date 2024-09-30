from colorama import Fore, Style
import discord
import discord.state
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime
import base64
import hashlib

def isBase64(s:str):
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode('UTF-8')
    except Exception:
        return False

class Base64coder(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="base64",description="為您編碼/解碼Base64格式的文字 (直接丟進來即可)")
    async def base64(self,interaction:discord.Interaction,text:str):

        guild = "私人" if interaction.guild==None else interaction.guild
        channel = "訊息" if interaction.guild==None else interaction.channel
        
        if(isBase64(text)):
            #COMMAND LOG    
            print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> Base64 (Decode)" + Style.RESET_ALL)
            await interaction.response.send_message(f"您的解碼結果: `{base64.b64decode(text).decode('UTF-8')}`")
        else:
            #COMMAND LOG
            print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> Base64 (Encode)" + Style.RESET_ALL)
            await interaction.response.send_message(f"您的編碼結果: `{base64.b64encode(text.encode('UTF-8')).decode('UTF-8')}`")

async def setup(bot:commands.Bot):
    await bot.add_cog(Base64coder(bot))