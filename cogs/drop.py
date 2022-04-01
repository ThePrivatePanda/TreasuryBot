from itertools import dropwhile
from nextcord.ext import commands
from nextcord import Embed


class Drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_role = self.bot.treasury.get_role(740723390675026000)
    
    @commands.command(name="drop")
    async def drop(self, ctx, *, prize):
        if self.staff_role not in ctx.author.roles:
            return await ctx.reply("You ain't allowed to do that.")
        prize = prize.replace("--delete", "")
        try:
            await ctx.message.delete()
        except:
            pass

        m = await ctx.send(embed=Embed(colour=0x00ffea, title=f"Drop by `{ctx.author.display_name}`", description=f"React with ✈️ first to claim ||{prize}||"))
        await m.add_reaction("✈️")
        def check(reaction, user):
            return str(reaction.emoji) == "✈️" and user.id != self.bot.user.id

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        await m.edit(embed=Embed(colour=0x00ffea, title=f"Drop by `{ctx.author.display_name}`", description=f"The drop for {prize} by {ctx.author.mention} has been claimed by {user.mention}"))

def setup(bot):
    bot.add_cog(Drop(bot))