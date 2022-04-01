from code import interact
from discord import User
from nextcord import Embed
from nextcord import Interaction, SlashOption
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

class SOTD(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.sotd_submissions_channel = self.bot.get_channel(952207189244780544)
        self.sotd_announcement_channel = self.bot.get_channel(952193764234002503)
        self.sotd_manager_role = self.bot.treasury.get_role(957264032061091842)
        self.yesyes_emote = self.bot.get_emoji(805437127554367549)
        self.nono_emote = self.bot.get_emoji(829726535203684382)

    @nextcord.slash_command(name="song", description="Submit a song of the day suggestion", guild_ids=[727276010600530011])
    async def song_(
        self,
        interaction: Interaction,
        song: str = SlashOption(description="Song Suggestion", required=True),
        message: str = SlashOption(description="Message", required=False, default="No Message")
        ):

        await self.sotd_submissions_channel.send(embed=Embed(colour=0x00ffea).add_field(name="Song:", value=song, inline=False).add_field(name="Message:", value=message, inline=False).set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url).set_footer(text="Treasury", icon_url=self.bot.user.avatar.url).set_thumbnail(url=self.bot.treasury.icon.url))
        await interaction.send("Alright done.", ephemeral=True)

    @nextcord.slash_command(name="sotd", description="Annoucne a song of the day", guild_ids=[727276010600530011])
    async def sotd_(
        self,
        interaction: Interaction,
        song: str = SlashOption(description="Name of the song", required=True),
        suggester: User = SlashOption(description="Mention the person who suggested it"),
        message: str = SlashOption(description="The message of the suggester", required=True),
        song_url: str = SlashOption(description="Youtube link of the song", required=True),
    ):
        if self.sotd_manager_role not in interaction.user.roles:
            return await interaction.send("You ain't allowed to do that!", ephemeral=False)

        song_thumbnail = "https://cdn.discordapp.com/icons/727276010600530011/d1c44f8386621e69800f9b50139593a8.png?size=1024"
        song_author = "me"
        message = await self.sotd_announcement_channel.send(embed=Embed(description=f"**Message:**\n{message}", colour=0x00ffea).set_author(name=suggester.display_name, icon_url=suggester.display_avatar.url).set_thumbnail(url=song_thumbnail).add_field(name="Song Name:", value=f"[{song}]({song_url})").add_field(name="Song Author", value=song_author).set_footer(text="Treasury", icon_url=self.bot.user.avatar.url))
        await message.add_reaction(self.yesyes_emote)
        await message.add_reaction(self.nono_emote)
        await interaction.send("Done.", ephemeral=True)


def setup(bot):
    bot.add_cog(SOTD(bot))
