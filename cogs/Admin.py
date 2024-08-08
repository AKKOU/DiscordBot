import json
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import discord.state
import requests
import random
from colorama import Fore, Style

intent = discord.Intents.all()
intent.message_content = True
bot = commands.Bot(command_prefix="$",intents=intent)

class Admin(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="checkuserid",description="查詢使用者功能(Admin Only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def checkuserid(self,interaction:discord.Interaction,user:discord.User):
        embed = discord.Embed(title=f"{user.name}'s Profile",color=0xd561ff)
        embed.add_field(name="使用者標籤",value=user.global_name)
        embed.add_field(name="使用者名稱",value=user.name)
        embed.add_field(name="使用者ID",value=user.id)
        embed.add_field(name="使用者加入日期",value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Admin(bot))

