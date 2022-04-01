from nextcord import Interaction, slash_command, SlashOption
from nextcord.ext import commands
from humanfriendly import parse_timespan
import asyncio


class Lockdown(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def lockdown(self, ctx: commands.Context, lockrole: bool = False):
        """
        Lockdown a server
        If you pass true, your @everyone role will also be denied permissions from within the role menu
        """
        guild = ctx.guild
        config_check = await self.config.guild(guild).channels()
        if not config_check:
            await ctx.send(
                "You need to set this up by running `{}lockdownset`, first and stepping through those configuration subcommands".format(
                    ctx.prefix
                )
            )
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        lock_check = await self.config.guild(ctx.guild).locked()
        if lock_check is True:
            return await ctx.send("You're already locked")

        await ctx.send(f"Proceed with locking down {guild.name}?\n`[yes|no]`")
        try:
            confirm_lock = await ctx.bot.wait_for("message", check=check, timeout=30)
            if confirm_lock.content.lower() != "yes":
                return await ctx.send(
                    "Good thing I was made for my time to be wasted - canceling lockdown..."
                )
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to reply!")

        await ctx.trigger_typing()
        nondefault_lock = await self.config.guild(guild).nondefault()
        if nondefault_lock is True:
            await self.secondary_lockdown(ctx, guild)

        # proceed to default lockdown
        await self.reign_lockdown(ctx, guild)

        if lockrole:
            perms = ctx.guild.get_role(ctx.guild.id).permissions
            perms.send_messages = False
            if not ctx.me.guild_permissions.manage_roles:
                await ctx.send(
                    "I'm missing the ability to manage roles so we will skip making changes to roles in the server settings"
                )
            try:
                await ctx.guild.default_role.edit(
                    permissions=perms, reason=f"Role Lockdown requested by {ctx.author.name}"
                )
                await self.config.guild(ctx.guild).lock_role.set(True)
            except Exception as e:
                await ctx.send(
                    f"Getting an error when attempting to edit role permissions in server settings:\n{e}\nSkipping..."
                )

        # finalize
        try:
            await ctx.send(
                "Server locked down. Revert this by running `{}unlockdown`".format(ctx.prefix)
            )
        except Exception as er:
            self.log.info(
                f"Couldn't secure overrides in Guild {ctx.guild.name} ({ctx.guild.id}): Locked as requested."
            )
            await self.loggerhook(
                guild,
                error=f"Unable to send messages on lockdown to your channels due to the following error\n```diff\n+ ERROR:\n- {er}\n```",
            )

        await self.config.guild(guild).locked.set(True)  # write it to configs


    @slash_command(name="Lockdown")
    async def ImsCog_(
        self,
        interaction: Interaction,
        category: str = SlashOption(description="Category to lock.", required=True, choices={
            "karuta": [823167859739066428, 941760360401231912, 941758148375642142],
            "dank": [727608271686598657, 934388991636176936],
            "epic rpg": [822930320298737764],
            "poketwo": [823260280099831869],
            "owo": [824393825140998214],
            "others": [806128856658477066, 750279051092164639]

        }),
    ) -> None:
        if interaction.author.top_role <= self.bot.treasury.get_role(self.bot.MOD_ID):
            return await interaction.send("You are not allowed to do that.", ephemeral=True)

        pass