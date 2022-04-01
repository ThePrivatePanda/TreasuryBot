import unicodedata

from nextcord.ext import commands
from nextcord import File
from io import StringIO

class Etc(commands.Cog):
    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """
        Shows you information about a number of characters.
        Only up to 25 characters at a time.
        """

        def to_string(c):
            digit = f"{ord(c):x}"
            name = unicodedata.name(c, "Name not found.")
            return f"`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <https://www.fileformat.info/info/unicode/char/{digit}>"

        msg = "\n".join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.reply(file=File(StringIO(msg), filename="charinfo.txt"))

        await ctx.send(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Etc())
