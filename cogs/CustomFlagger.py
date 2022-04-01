from nextcord.ext import commands


class CustomFlagger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def on_message_custom_flagger(self, msg):
        if "--delete" in msg.content and ("pre-ignore" not in msg.content or "preignore" not in msg.content):
            await msg.delete()

def setup(bot):
    bot.add_cog(CustomFlagger(bot))