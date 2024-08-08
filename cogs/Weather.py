import discord
import requests
import io
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional
from colorama import Fore, Style

class Weather(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    @app_commands.command(name="weather",description="為您查詢天氣")
    @app_commands.describe(city = "特定城市",option="只查詢特定內容")
    @app_commands.choices(
        city = [
            Choice(name="基隆市",value="%E5%9F%BA%E9%9A%86%E5%B8%82"),
            Choice(name="臺北市",value="%E8%87%BA%E5%8C%97%E5%B8%82"),
            Choice(name="新北市",value="%E6%96%B0%E5%8C%97%E5%B8%82"),
            Choice(name="桃園市",value="%E6%A1%83%E5%9C%92%E5%B8%82"),
            Choice(name="新竹縣",value="%E6%96%B0%E7%AB%B9%E7%B8%A3"),
            Choice(name="新竹市",value="%E6%96%B0%E7%AB%B9%E5%B8%82"),
            Choice(name="宜蘭縣",value="%E5%AE%9C%E8%98%AD%E7%B8%A3"),
            Choice(name="臺中市",value="%E8%87%BA%E4%B8%AD%E5%B8%82"),
            Choice(name="苗栗縣",value="%E8%8B%97%E6%A0%97%E7%B8%A3"),
            Choice(name="彰化縣",value="%E5%BD%B0%E5%8C%96%E7%B8%A3"),
            Choice(name="嘉義市",value="%E5%98%89%E7%BE%A9%E5%B8%82"),
            Choice(name="嘉義縣",value="%E5%98%89%E7%BE%A9%E7%B8%A3"),
            Choice(name="南投縣",value="%E5%8D%97%E6%8A%95%E7%B8%A3"),
            Choice(name="雲林縣",value="%E9%9B%B2%E6%9E%97%E7%B8%A3"),
            Choice(name="臺南市",value="%E8%87%BA%E5%8D%97%E5%B8%82"),
            Choice(name="高雄市",value="%E9%AB%98%E9%9B%84%E5%B8%82"),
            Choice(name="屏東縣",value="%E5%B1%8F%E6%9D%B1%E7%B8%A3"),
            Choice(name="澎湖縣",value="%E6%BE%8E%E6%B9%96%E7%B8%A3"),
            Choice(name="花蓮縣",value="%E8%8A%B1%E8%93%AE%E7%B8%A3"),
            Choice(name="臺東縣",value="%E8%87%BA%E6%9D%B1%E7%B8%A3"),
            Choice(name="金門縣",value="%E9%87%91%E9%96%80%E7%B8%A3"),
            Choice(name="連江縣",value="%E9%80%A3%E6%B1%9F%E7%B8%A3"),
        ],
        option = [
            Choice(name="詳細降雨機率",value=0),
            Choice(name="詳細溫度",value=1),
        ]
    )
    async def weather(self,interaction:discord.Interaction,city:Choice[str],option:Optional[int]):
        try:
            
            response = requests.get(f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-CA635BA6-683C-4D51-B340-9F26D1C2D279&locationName={city.value}")
            guild = "私人" if interaction.guild==None else interaction.guild
            channel = "訊息" if interaction.guild==None else interaction.channel
            file = None
            data = response.json()
            if option is None:
                embed = discord.Embed(title=f"{city.name} - {data['records']['datasetDescription']}",description="資料由中央氣象署提供",color=0x73bbff)
                for d in data['records']['location']:
                    # 天氣狀況
                    for element in d['weatherElement'][0]['time']:
                        starttime = datetime.strptime(element['startTime'], "%Y-%m-%d %H:%M:%S")
                        endtime = datetime.strptime(element['endTime'], "%Y-%m-%d %H:%M:%S")
                        embed.add_field(name=element['parameter']['parameterName'],value=f"``{starttime.strftime('%d日 %I %p')} 至\n{endtime.strftime('%d日 %I %p')}``")
                    # 降雨機率
                    percent = 0
                    mint =0
                    maxt =0
                    cnt =0
                    for element in d['weatherElement'][1]['time']:
                        cnt += 1
                        percent += int(element['parameter']['parameterName'])
                    percent = percent/cnt
                    cnt =0
                    # 最低溫
                    for element in d['weatherElement'][2]['time']:
                        cnt += 1
                        mint += int(element['parameter']['parameterName'])
                    mint = mint/cnt
                    cnt =0
                    # 最高溫
                    for element in d['weatherElement'][4]['time']:
                        cnt += 1
                        maxt += int(element['parameter']['parameterName'])
                    maxt = maxt/cnt
                    embed.add_field(name="降雨機率",value=f"{round(percent,2)}%")
                    embed.add_field(name="最低溫度",value=f"{round(mint,2)}°C")
                    embed.add_field(name="最高溫度",value=f"{round(maxt,2)}°C")
                print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 天氣指令(全部顯示)" + Style.RESET_ALL)
            
            elif option==0:
                embed = discord.Embed(title=f"{city.name} - 詳細降雨機率",description="資料由中央氣象署提供",color=0x73bbff)
                for d in data['records']['location']:

                    percent_array = []
                    time_array = []
                    # 降雨機率
                    for element in d['weatherElement'][1]['time']:

                        starttime = datetime.strptime(element['startTime'], "%Y-%m-%d %H:%M:%S")
                        endtime = datetime.strptime(element['endTime'], "%Y-%m-%d %H:%M:%S")
                        percent = element['parameter']['parameterName']
                        # 曲線圖資料陣列
                        percent_array.append(int(percent))
                        time_array.append(starttime.strftime('%d日 %I %p'))
                        # 文字embed
                        embed.add_field(name=f"降雨機率:{percent}%",value=f"``{starttime.strftime('%d日 %I %p')} 至\n{endtime.strftime('%d日 %I %p')}``")
                #曲線圖設定
                plt.style.use('fivethirtyeight')
                plt.rcParams['font.sans-serif']=['Microsoft YaHei']
                plt.figure(figsize=(12,4))
                plt.xlabel('時間')
                plt.ylabel('降雨機率')
                plt.title(f"{city.name} - 詳細降雨機率")
                plt.ylim(0,100)
                #塞資料
                plt.plot(time_array,percent_array)
                #曲線圖存檔
                buf = io.BytesIO()
                plt.savefig(buf,format='png')
                buf.seek(0)
                file = discord.File(buf,filename='plotimage.png')
                embed.set_image(url='attachment://plotimage.png')
                print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 天氣指令(詳細降雨)" + Style.RESET_ALL)
            else:
                embed = discord.Embed(title=f"{city.name} - 詳細氣溫",description="資料由中央氣象署提供",color=0x73bbff)
                for d in data['records']['location']:
                # 最低溫
                    time_array = []
                    mint_array = []
                    maxt_array = []
                    for element in d['weatherElement'][2]['time']:
                        starttime = datetime.strptime(element['startTime'], "%Y-%m-%d %H:%M:%S")
                        endtime = datetime.strptime(element['endTime'], "%Y-%m-%d %H:%M:%S")
                        mint = element['parameter']['parameterName']
                        time_array.append(starttime.strftime('%d日 %I %p'))
                        mint_array.append(int(mint))
                        embed.add_field(name=f"最低溫度:{mint}°C",value=f"``{starttime.strftime('%d日 %I %p')} 至\n{endtime.strftime('%d日 %I %p')}``")  
                    # 最高溫
                    for element in d['weatherElement'][4]['time']:
                        starttime = datetime.strptime(element['startTime'], "%Y-%m-%d %H:%M:%S")
                        endtime = datetime.strptime(element['endTime'], "%Y-%m-%d %H:%M:%S")
                        maxt = element['parameter']['parameterName']
                        maxt_array.append(int(maxt))
                        embed.add_field(name=f"最高溫度:{maxt}°C",value=f"``{starttime.strftime('%d日 %I %p')} 至\n{endtime.strftime('%d日 %I %p')}``")
                    #曲線圖設定
                    plt.style.use('fivethirtyeight')
                    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
                    plt.figure(figsize=(12,4))
                    plt.xlabel('時間')
                    plt.ylabel('最高溫-最低溫')
                    plt.title(f"{city.name} - 詳細氣溫")
                    plt.ylim(0,40)
                    #塞資料
                    plt.plot(time_array,mint_array)
                    plt.plot(time_array,maxt_array)
                    #曲線圖存檔
                    buf = io.BytesIO()
                    plt.savefig(buf,format='png')
                    buf.seek(0)
                    file = discord.File(buf,filename='plotimage.png')
                    embed.set_image(url='attachment://plotimage.png')
                print(Fore.GREEN + f"[{datetime.now()}][{guild}的{channel}] {interaction.user.name} ({interaction.user.id}) --> 天氣指令(詳細氣溫)" + Style.RESET_ALL)
            
            embed.set_footer(text=f"查詢時間: {datetime.now().strftime('%b %d, %Y')}")
            if(file is not None):
                await interaction.response.send_message(embed=embed,file=file)
            else:
                await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)

async def setup(bot:commands.Bot):
    await bot.add_cog(Weather(bot))