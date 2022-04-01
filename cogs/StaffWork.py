from nextcord import Interaction, SlashOption
import nextcord
from nextcord.ext import commands
from humanfriendly import parse_timespan

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

class StaffWork(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="staff", description="Some stuff for the staff", guild_ids = [727276010600530011])
    async def staff(self, interaction):
        pass
    
    @staff.subcommand(name="work", description="Manage jobs")
    async def staff_work(self, interaction):
        pass

    @staff_work.subcommand(name="add", description="Announce a job")
    async def staff_work_add(
        self,
        interaction: Interaction,
        time: str = SlashOption(description="Runtime of giveaway.", required=True),
        winners: int = SlashOption(description="Number of winners", required=True),
        prize: str = SlashOption(description="Prize", required=True),
        not_claimed_action: str = SlashOption(description="What will happen if prize is not claimed?", required=True, choices={"Donate to special": "special", "Reroll Winner": "reroll", "Giveaway manager to keep": "keep"}),
        join_req: str = SlashOption(description="Requirement to join the giveaway", required=False),
        message: str = SlashOption(description="Message", required=False),
        ):

        if interaction.channel.id != 855434764419858454:
            return await interaction.send("This command can only be used in <#855434764419858454>", ephemeral=True)

        if winners < 1:
            return await interaction.send("Giveaways must have at least 1 winner.", ephemeral=True)

        if winners > self.bot.MAX_WINNERS:
            return await interaction.send("You can't have more than 30 winners", ephemeral=True)

        time_parsed = time
        try:
            time_parsed = int(parse_timespan(time))
            time_parsed = time_parsed/60
        except:
            pass

        try:
            time_parsed = int(time_parsed)
        except:
            pass

        if time_parsed == 0 or time_parsed == "0":
            time = time
        else:
            time = time_parsed

        try:
            time = int(time)
        except:
            pass


        message = message or "No message given."
        join_req = join_req or "None"

        if isinstance(time, int):
            timemsg =  f"Time: {time} minutes ({time/60:.2f} hours)"
        else:
            timemsg = f"Time: {time} minutes"
        view = Confirm()
        myembed = nextcord.Embed(
            title="Giveaway Donation",
            description=f"Prize: {prize}\n{timemsg}\nWinners: {winners}\nMessage: {message}\nRequirement: {join_req}\nAction if not claimed: {not_claimed_action}",
    colour=0x00ffea
            )
        await interaction.send(embed=myembed, view=view, ephemeral=True)

        await view.wait()
        if view.value is None:
            await interaction.send('Timed out...', ephemeral=True)
        elif view.value:
            await interaction.channel.send(
                content=f"<@&784783374392229898> <@&790327075939549194> <@&817122742754213949>,\nLookie here, A giveaway donation by {interaction.user.mention}!",
                embed=myembed
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(text=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            )
        else:
            await interaction.send(f'Alright cancelled {interaction.user.mention}, re-run the command to donate!', ephemeral=False)

def setup(bot):
    bot.add_cog(StaffWork(bot))
