from nextcord import Interaction, slash_command
from nextcord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @slash_command(name="owner", description="Owner only commands!")
    async def owner_only_base(self, interaction: Interaction):
        await interaction.send(f"How did you get here? Seriously, contact "
                               f"{self.bot.owner.mention} if you see this!")

    @slash_command(name="extension", description="Controls extension-related actions.")
    async def base_extension_cmd(self, interaction: Interaction):
        await interaction.send(f"How did you get here? Seriously, contact "
                               f"{self.bot.owner.mention} if you see this!")

    @base_extension_cmd.subcommand(name="load", description="Loads an extension from the disk.")
    async def extension_load(self, interaction: Interaction, name: str):
        if not await self.bot.is_owner(interaction.user):
            return await interaction.send("You aren't the bot owner!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            self.bot.load_extension(name=name)
            await self.bot.slash_resync_command()
        except Exception as e:
            return await interaction.send(f"Failed to load extension with error: {e}")
        await interaction.send("Loaded extension.")

    @base_extension_cmd.subcommand(name="unload", description="Unloads an extension from the bot.")
    async def extension_unload(self, interaction: Interaction, name: str):
        if not await self.bot.is_owner(interaction.user):
            return await interaction.send("You aren't the bot owner!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            self.bot.unload_extension(name=name)
            await self.bot.slash_resync_command()
        except Exception as e:
            return await interaction.send(f"Failed to unload extension with error: {e}")
        await interaction.send("Unloaded extension.")

    @base_extension_cmd.subcommand(name="reload", description="Reloads an extension from the bot, from disk.")
    async def extension_reload(self, interaction: Interaction, name: str):
        if not await self.bot.is_owner(interaction.user):
            return await interaction.send("You aren't the bot owner!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            self.bot.reload_extension(name=name)
            await self.bot.slash_resync_command()
        except Exception as e:
            return await interaction.send(f"Failed to reload extension with error: {e}")
        await interaction.send("Reloaded extension.")


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))