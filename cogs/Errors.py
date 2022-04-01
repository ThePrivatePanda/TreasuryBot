import traceback
from nextcord.ext import commands
import asyncio
from nextcord.ext.commands import errors
import nextcord

class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Cog = bot

    @commands.Cog.listener("on_command_error")
    async def on_command_error_dm(self, ctx, error):
        if isinstance(error, errors.CommandNotFound):
            return
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        elif isinstance(error, errors.TooManyArguments):
            await ctx.send("You are giving too many arguments!")
            return
        elif isinstance(error, errors.BadArgument):
            await ctx.send(
                "The library ran into an error attempting to parse your argument."
            )
            return
        elif isinstance(error, errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument.")

        elif isinstance(error, nextcord.NotFound) and "Unknown interaction" in str(error):
            return

        else:
            await ctx.send(
                f"This command raised an exception: `{type(error)}:{str(error)}`"
            )

        deliminator = "\n"
        if not self.bot.owner:
            self.bot.owner = await self.bot.getch_user(self.bot.owner_id)
        await self.bot.owner.send(
            f"{type(error).__name__}: {ctx.message.jump_url} while using command {ctx.invoked_with}\n```py\n{deliminator.join(traceback.format_exception(type(error), error, error.__traceback__))}```"
        )


def setup(bot: commands.Bot):
    bot.add_cog(Errors(bot))
