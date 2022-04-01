from nextcord.ext import commands
from nextcord import Member, Role

class Demote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.cache: dict = {}

    @commands.command(name="demote", aliases=["demoot"])
    async def demoot_(self, ctx: commands.Context, user: Member, pos: Role = None) -> None:
        if user.id == 736147895039819797:
            return await ctx.reply("Do that one more time and I'll demote you.")
        if ctx.author.top_role <= user.top_role and ctx.author.id != 736147895039819797:
            return await ctx.reply("Your not allowed to do that.")

        rr: list = []
        self.cache[user.id] = []

        for role in user.roles:
            if role > self.bot.treasury.get_role(784819437626720326):
                if pos:
                    if role <= pos:
                        continue
                self.cache[user.id].append(role.id)
                rr.append(role)

        await user.remove_roles(*rr)
        await ctx.reply(f"{user.mention} has been demoted. 2bad4them")

    @commands.command(name="undemote", aliases=["promote", "undemoote", "promoot"])
    async def undemoot_(self, ctx: commands.Context, user: Member, role: Role = None) -> None:
        if ctx.author.top_role <= user.top_role and ctx.author.id != 736147895039819797:
            return await ctx.reply("Your not allowed to do that.")

        if user.id in self.cache.keys():
            await user.add_roles(*[ctx.guild.get_role(r) for r in self.cache[user.id]])
            del self.cache[user.id]
            return await ctx.reply(f"{user.mention} has been promoted. v v good4them")

        if not role:
            return await ctx.reply("Unable to promote since not in cache and no arg given either.")

        rr: list[Role] = []
        for r in role:
            rr.append(ctx.guild.get_role(r))

        await user.add_roles(*rr)
        await ctx.reply(f"Promoted {user.mention} till {user.top_role.name}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Demote(bot))