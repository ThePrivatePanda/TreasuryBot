from nextcord import Embed
from nextcord.ext import commands

class Trades(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.auto_messages_ = {733372103738523748: 0, 853685813132394526: 0, 867088132050518037: 0, 934403708685516811: 0}
        self.embed: Embed = Embed(
            title="New trade-middleman rules",
            description="""
Use `pls trade <your offer>, [their offer] <@user>` for trades, and, `pls fight <@user> [bet]` for fights instead of a middleman.

If you wish to **REPORT A SCAM**, please use <#806509682386403328> and/or DM <@575252669443211264>.
Please do NOT ping the staff, the same may result in moderation actions.
""",
    colour=0x00ffea
    ).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text="TreasuryBot", icon_url=self.bot.user.display_avatar.url)

    @commands.Cog.listener("on_message")
    async def auto_trade_rule_(self, message) -> None:
        if message.channel.id not in (733372103738523748, 853685813132394526, 867088132050518037, 934403708685516811):
            return
        if self.auto_messages_[message.channel.id] != 250:
            self.auto_messages_[message.channel.id] += 1
            return
        self.auto_messages_[message.channel.id] = 0
        return await message.channel.send(embed=self.embed)

    @commands.command()
    async def mm(self, ctx) -> None:
        await ctx.send(embed=self.embed)

def setup(bot) -> None:
    bot.add_cog(Trades(bot))
