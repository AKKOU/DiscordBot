from discord.ext import commands
import datetime
from colorama import Fore, Style

class VoiceLog(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if before.channel is None and after.channel is not None:
            print(Fore.CYAN + f"[{datetime.datetime.now()}] [{member.guild}] {member.name}: 加入了語音 {after.channel.name}" + Style.RESET_ALL)
        elif before.channel is not None and after.channel is None:
            print(Fore.LIGHTRED_EX + f"[{datetime.datetime.now()}] [{member.guild}] {member.name}: 退出了語音 {before.channel.name}" + Style.RESET_ALL)

async def setup(bot:commands.Bot):
    await bot.add_cog(VoiceLog(bot))