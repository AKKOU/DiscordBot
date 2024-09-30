from colorama import Fore, Style
import discord
import discord.state
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime
import hashlib

class Hashcoder(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="hasher",description="為您編碼Hash格式的文字 (直接丟進來即可)")
    @app_commands.describe(hash_type = "雜湊類型")
    @app_commands.choices(
        hash_type = [
            Choice(name="SHA1",value="sha1"),
            Choice(name="SHA256",value="sha256"),
            Choice(name="MD5",value="md5")
        ]
    )
    async def hasher(self,interaction:discord.Interaction,hash_type:Choice[str],text:str):
    
        guild = "私人" if interaction.guild==None else interaction.guild
        channel = "訊息" if interaction.guild==None else interaction.channel
        
        if hash_type.value == "sha1":
            return_value = hashlib.sha1(text.encode('utf-8')).hexdigest()
        elif hash_type.value == "sha256":
            return_value = hashlib.sha256(text.encode('utf-8')).hexdigest()
        else:
            return_value = hashlib.md5(text.encode('utf-8')).hexdigest()

        print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> Hash ({hash_type.name})" + Style.RESET_ALL)
        await interaction.response.send_message(f"您的雜湊結果:{return_value}",ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Hashcoder(bot))