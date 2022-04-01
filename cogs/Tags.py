import re
from socket import CAN_BCM_TX_ANNOUNCE
from nextcord.ext import commands


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = []

    @commands.Cog.listener("on_message")
    async def on_message_tags(self, message):
        content = message.content.replace("--delete", "")
        if content not in self.tags:
            return
        if content == "!!gw":
            return await message.channel.send("<@&730814805308473424>") # giveaway ping
        if content == "":
            pass
        # todo