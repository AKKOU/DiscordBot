import discord
import asyncio
import datetime
from discord.ext import commands
from discord import app_commands
from typing import Optional
import twstock
from twstock.realtime import get
import pandas
from colorama import Fore, Style

class Stock(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    #輸入指令
    @app_commands.command(name="stock",description="抓取當前股票資訊")
    async def stock(self,interaction:discord.Interaction,num:str):
        try:
            #初始化
            stock = get(num)
            stock_price = twstock.Stock(num)
            colorlist = [0x00ff00,0xff0000,0xffff00]
            #讀取資料
            sinfo = stock['info']
            price = stock['realtime']
            #是否上漲
            index = 0
            gap = stock_price.price[-1] - stock_price.price[-2]
            percent = stock_price.price[-1] / stock_price.price[-2]
            if(gap>0):
                index = 1
            elif(gap==0):
                index = 2
            else:
                index = 0

            if(percent>1):
                percent = round((percent-1)*100,2)
            else:
                percent = round((percent-1)*100,2)

            #建立框框
            embed = discord.Embed(title=f"{sinfo['name']}({sinfo['channel']})",description=sinfo['fullname'],color=colorlist[index])
            embed.add_field(name="成交價",value=price['latest_trade_price'])
            embed.add_field(name="最高價",value=price['high'])
            embed.add_field(name="最低價",value=price['low'])
            embed.add_field(name="開盤價",value=price['open'])
            embed.add_field(name="漲跌",value=gap)
            embed.add_field(name="漲幅",value=f"{percent}%")

            embed.set_footer(text=f"成交日期:{sinfo['time']}")

            guild = "私人" if interaction.guild==None else interaction.guild
            channel = "訊息" if interaction.guild==None else interaction.channel
            print(Fore.GREEN + f"[{datetime.datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 斜線指令(股票查詢)" + Style.RESET_ALL)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"出現錯誤:{e}"+Style.RESET_ALL)


async def setup(bot:commands.Bot):
    await bot.add_cog(Stock(bot))