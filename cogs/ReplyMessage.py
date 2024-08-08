import json
import discord
from discord.ext import commands
import asyncio
import datetime
from discord.ext import commands
from discord import app_commands
import requests
import random

class ReplyMessage(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        json_data = requests.get("https://akkou.github.io/download/update/dcbot_response/dcbot_main.json")
        json_nssh = requests.get("https://akkou.github.io/download/update/dcbot_response/dcbot_nssh.json")
        json_daan = requests.get("https://akkou.github.io/download/update/dcbot_response/dcbot_daan.json")
        data = json.loads(json_data.text)
        nssh = json.loads(json_nssh.text)
        daan = json.loads(json_daan.text)

        data = {k.lower(): v for k,v in data.items()}
        nssh = {k.lower(): v for k,v in nssh.items()}
        daan = {k.lower(): v for k,v in daan.items()}
        
        if message.author == self.bot.user:
                return
        msg = message.content.lower()
        #nssh only
        if(message.guild.id==601296688879108109 and msg in nssh):
            lst = str(nssh[msg]).split(',')
            await message.channel.send(lst[random.randrange(0,len(lst))])
        #daan only
        elif(message.guild.id==1016954822148231168 and msg in daan):
            lst = str(daan[msg]).split(',')
            await message.channel.send(lst[random.randrange(0,len(lst))])
        #normal message response
        elif(msg in data): 
            lst = str(data[msg]).split(',')
            await message.channel.send(lst[random.randrange(0,len(lst))])
        

async def setup(bot:commands.Bot):
    await bot.add_cog(ReplyMessage(bot))