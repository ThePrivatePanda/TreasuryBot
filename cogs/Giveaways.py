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

class GiveawayDono(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="giveaway", description="Giveaways! Fun!", guild_ids = [727276010600530011])
    async def giveaway(self, interaction):
        pass

    @giveaway.subcommand(name="donate", description="Donate to the server for a giveaway.")
    async def dono_(
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


    @commands.command(name="howgaw", aliases=["howtodonate", "howdonate"], description="How to donate for a giveaway")
    async def howgaw_(self, ctx):
        if ctx.channel.id != 855434764419858454:
            return await ctx.reply("This command can only be used in <#855434764419858454>")
        if ctx.author.top_role < ctx.guild.get_role(740723390675026000):
            return await ctx.reply("You don't have permission to use this command.")
        myembed = nextcord.Embed(
            title="How to donate for a giveaway",
            description="Want to donate for a giveaway?\nJust type `/giveaway donate` and choose the slash command which pops up from <@944302078065524746>!\nThe options given will guide you through the process.\n", colour=0x00ffea)

        myembed.add_field(
                name="⦿ A few rules...",
                value="""
- Respect the giveaway manager at your service
- Minimum payout per person is **500k**
- You must cover all necessary taxes if applicable
- No troll/unreasonable requirements such as asking people to be pinged
**- Any kind of promotion through your message is strictly prohibited**
                """
            )
        myembed.set_thumbnail(url=ctx.guild.icon.url)
        myembed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=myembed)
        await ctx.message.delete()


    # @giveaway.subcommand(name="stats", description="Show stats of giveaway managers")
    # async def giveaway_stats(
    #     self,
    #     interaction: nextcord.Interaction,
    #     user: nextcord.Member = SlashOption(description="Mention the user to show their stats", required=False, default="all"),
    #     ephemeral_var: bool = SlashOption(description="Type `True` if the output should NOT be visible to everyone", required=False)
    #     ):
    #     if not ephemeral_var:
    #         ephemeral_var = False
    #     else:
    #         ephemeral_var = ephemeral_var

    #     await interaction.response.defer(ephemeral=True, with_message=True)
    #     if interaction.user.top_role < interaction.guild.get_role(740723390675026000):
    #         return await interaction.send("You don't have permission to use this command.", ephemeral=True)
    #     if user == "all":
    #         data = await self.bot.db.execute("SELECT * FROM gawman_stats")
    #         data = await data.fetchall()
    #     else:
    #         data = await self.bot.db.execute("SELECT * FROM gawman_stats WHERE userid = ?", (user.id, ))
    #         data = await data.fetchone()
    #     if not data:
    #         return await interaction.followup.send("User not found.", ephemeral=True)
    
    #     myembed = nextcord.Embed(
    #         title="Giveaway Manager Statistics",
    #         colour=0x00ffea
    #         ).set_thumbnail(
    #             url=interaction.guild.icon.url
    #         ).set_footer(
    #             text=interaction.guild.name,
    #             icon_url=interaction.guild.me.display_avatar.url
    #         )
        
    #     if user == "all":
    #         stats_dict = {a: b for a, b in data}
    #         stats_dict = dict(sorted(stats_dict.items()))

    #         desc = ""
    #         for i in range(len(stats_dict)):
    #             desc += f"\n{i+1}. {tuple(stats_dict.items())[i][1]} giveaways have been hosted by <@{tuple(stats_dict.items())[i][0]}>"
    #         myembed.add_field(
    #             name="Total Statistics",
    #             value=f"Total giveaways hosted: {desc}",
    #         )
    #     else:
    #         myembed.add_field(
    #             name=f"{user.name}'s Statistics",
    #             value=f"{user.name} has hosted {data[1]} giveaways so far",
    #         )

    #     await interaction.followup.send(embed=myembed, ephemeral=ephemeral_var)

    @commands.Cog.listener("on_message")
    async def on_message_(self, message):
        if message.channel.id != 853380368916021299: # staff bots channel id
            return
        if message.author.id != 634866217764651009: # noumenon user id
            return
        if "GIVEAWAY" not in message.content:
            return

        embed: nextcord.Embed = message.embeds[0]
        prize = embed.title
        host = embed.description.split('Hosted by: ')[1].split('\n')[0]
        duration = embed.description.split("Time: ")[1].split("(")[0].replace("*", "")
        donor = None
        req = None
        gaw_message = None
        endtime = embed.description.split("Time: ")[1].split("(")[1].split(" ")[1].split(")")[0]

        for i in embed.fields:
            if "Donor:" in i.name:
                donor = i.value
            elif "Requirements:" in i.name:
                req = i.value
        def check(m):
            return m.author.id == 634866217764651009 and len(m.embeds) == 1 and "Giveaway" in m.embeds[0].title and "730814805308473424" in m.content
        new_message = await self.bot.wait_for("message", timeout=20, check=check)

        try:
            gaw_message = new_message.embeds[0].description.split("**Message:** ")[1]
        except:
            gaw_message = None

        await self.bot.giveaway_log_channel.send(embed=nextcord.Embed(
            title="Giveaway started",
            description=f"Prize: {prize}\nHost: {host}\nDonor: {donor}\nRequirements: {req}\nDuration: {duration}\nEnd time: {endtime}\nMessage: {gaw_message}\n\nClick [here]({message.jump_url}) to jump to the giveaway message",
            colour=nextcord.Colour.blue()
            ).set_footer(icon_url=message.guild.icon.url, text="Treasury Bot")
        )
        hostid = int("".join([str(i) for i in host if i.isdigit()]))
        # previous = await self.bot.db.execute("SELECT gaws_hosted FROM gawman_stats WHERE userid = ?", (hostid, ))
        # previous = await previous.fetchone()
        # if previous:
            # gaws_hosted = previous[0]+1
        # else:
            # gaws_hosted = 1
        # await self.bot.db.execute("UPDATE gawman_stats VALUES (?, ?)", (hostid, gaws_hosted, ))
        # await self.bot.db.commit()

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit_(self, before, message):
        if message.channel.id != 853380368916021299: # staff bots channel id
            return
        if message.author.id != 634866217764651009: # noumenon user id
            return
        if "GIVEAWAY ENDED" not in message.content:
            return

        embed: nextcord.Embed = message.embeds[0]
        prize = embed.title
        host = embed.description.split('Hosted by: ')[1].split('\n')[0]
        donor = None
        req = None
        for i in embed.fields:
            if "Donor:" in i.name:
                donor = i.value
            elif "Requirements:" in i.name:
                req = i.value

        embed = message.embeds[0]
        winner = embed.description.split("Winner: ")[1].split("\n")[0]
        await self.bot.giveaway_log_channel.send(embed=nextcord.Embed(
            title="Giveaway Ended",
            description=f"Prize: {prize}\nHost: {host}\nDonor: {donor}\nRequirements: {req}\nWinners: {winner}\n\nClick [here]({message.jump_url}) to jump to the giveaway message",
            colour=nextcord.Colour.green()
            ).set_footer(icon_url=message.guild.icon.url, text="Treasury Bot")
        )

def setup(bot):
    bot.add_cog(GiveawayDono(bot))
