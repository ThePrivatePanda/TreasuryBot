from email import message
from nextcord.ext import commands, tasks

class BumpPing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.myloop.start()

    def restart_loop(self):
        self.myloop.restart()

    @tasks.loop(seconds=10)
    async def myloop(self):
        await self.bot.get_channel().send(f"Nab")
        msg = await self.bot.wait_for("message", check=lambda m: m.author.id == 736147895039819797 and m.channel.id == 945302377110597696 and "ok" in m.content, timeout=60)
        await msg.channel.send("omk")


    @tasks.loop(hours=2)
    async def bump_ping(self):
        await self.bot.get_channel(737745521372037221).send(f"<@&927065312321478687> It's been 2 hours since the last successful bump, could someone run `!d bump`?")

        msg = await self.bot.wait_for("message", check=lambda m: m.author.id == 302050872383242240 and m.channel.id == 737745521372037221 and "Bump done! :thumbsup:" in m.embeds[0].description, timeout=60)
        bumper = int("".join([i for i in msg.embeds[0].description.split(" ")[0] if i.isdigit()]))

        await msg.channel.send(f"<@{bumper}> thank you for bumping! Make sure to leave a review at https://disboard.org/server/727276010600530011.")
        await self.bump_ping.restart()

def setup(bot):
    bot.add_cog(BumpPing(bot))