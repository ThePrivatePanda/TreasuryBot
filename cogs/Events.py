from nextcord import SlashOption
import nextcord
from nextcord.ext import commands

class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.grey)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()

class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="event", description="Events! Fun!", guild_ids = [727276010600530011])
    async def event(self, interaction):
        pass
    
    @event.subcommand(name="donate", description="Donate for an event!")
    async def event_donate(
        self,
        interaction: nextcord.Interaction,
        prize: str = SlashOption(description="The prir of the event!", required=True),
        event: str = SlashOption(description="Which event to host?", choices={
            "Mafia": "mafia",
            "Rumble Royale": "rumble",
            "Dank Memer Heist": "heist",
            "Mudae Green Tea": "greentea",
            "Mudae Red Tea": "redtea",
            "Mudae Black Tea": "blacktea",
        },
        required=True),
        requirement: str = SlashOption(description="What is the requirement to join the event?", required=False),
    ):
        if interaction.channel.id != 901362488262656030:
            return await interaction.send("This command can only be used in <#901362488262656030>", ephemeral=True)

        join_req = requirement or "None"

        view = Confirm()
        myembed = nextcord.Embed(
            title="Giveaway Donation",
            description=f"Prize: {prize}\nEvent: {event}\nRequirement: {join_req}\n",
    colour=0x00ffea
            )
        await interaction.send(embed=myembed, view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            await interaction.send('Timed out...', ephemeral=True)
        elif view.value:
            await interaction.channel.send(
                content=f"<@&810573438594187294> ,\nLookie here, An event donation by {interaction.user.mention}!",
                embed=myembed
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(text=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            )
        else:
            await interaction.send(f'Alright cancelled {interaction.user.mention}, re-run the command to donate!', ephemeral=True)



    @commands.command(name="howevent", aliases=["howev", "how2ev", "d2ev"], description="How to donate for a event")
    async def howev_(self, ctx):
        if ctx.channel.id != 901362488262656030:
            return await ctx.reply("This command can only be used in <#901362488262656030>")
        if ctx.author.top_role < ctx.guild.get_role(740723390675026000):
            return await ctx.reply("You don't have permission to use this command.")
        myembed = nextcord.Embed(
            title="How to donate for an event",
            description="Want to donate for an event?\nJust type `/event donate` and choose the slash command which pops up from <@944302078065524746>!\nThe options given will guide you through the process.\n", colour=0x00ffea)

        myembed.add_field(
                name="⦿ A few rules...",
                value="""
- Respect the giveaway manager at your service
- Minimum payout per person is **500k**
- Minimum donation amount for a heist is 5mil
- You must cover all necessary taxes if applicable
- No troll/unreasonable requirements such as asking people to be pinged
**- Any kind of promotion through your message is strictly prohibited**
                """
            )
        myembed.set_thumbnail(url=ctx.guild.icon.url)
        myembed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=myembed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Events(bot))
