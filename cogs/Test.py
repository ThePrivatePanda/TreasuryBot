from nextcord.ext import commands, tasks


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()
    
    @tasks.loop(seconds=1)
    async def my_task(self):
        print("f")
    
    def cog_unload(self):
        self.my_task.stop()

def setup(bot):
    bot.add_cog(Test(bot))