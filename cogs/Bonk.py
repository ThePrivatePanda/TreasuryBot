from nextcord import User
from nextcord.ext import commands
from humanfriendly import parse_timespan
import datetime


class Bonk(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    async def remind(self, user: int, message: str) -> None:
        await self.bot.db.execute("DELETE FROM reminders WHERE user_id = ? and message = ?", (user, message))
        user: User = await self.bot.getch_user(user)
        await user.send(f"Reminder for `{message}`")

    @commands.group(invoke_without_command=True, name="bonk", aliases=["remindme", "remind"])
    async def _bonk(self, ctx: commands.Context, duration: str, *, message: str=None) -> None:
        message: str = f"{ctx.message.jump_url}\n{message}" or ctx.message.jump_url
        try:
            duration: int = parse_timespan(duration)
            reminder_time = datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=duration))
        except:
            return await ctx.reply("Invalid time.")

        rems = await self.bot.db.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY ind", (ctx.author.id, ))
        rems = await rems.fetchall()
        if len(rems) == 0:
            index = 1
        else:
            index = rems[0][0]+1

        try:
            await self.bot.db.execute("INSERT INTO reminders (ind, user_id, message, time) VALUES (?, ?, ?, ?)", (index, ctx.author.id, message, reminder_time, ))
            await self.bot.db.commit()
        except:
            return await ctx.reply("Wasn't able to add reminder to the database.")

        self.bot.loop.call_later(duration, lambda: self.bot.loop.create_task(self.remind(ctx.author.id, message)))
        await ctx.send(f"I'll remind you about `{message}` on <t:{int(reminder_time)}:F>")

    @commands.command(name="bonks", aliases=["reminders", "all", "list"])
    async def _bonks(self, ctx: commands.Context) -> None:
        reminders = await self.bot.db.execute("SELECT * FROM reminders WHERE user_id = ?", (ctx.author.id, ))
        reminders = await reminders.fetchall()

        if len(reminders) == 0:
            return await ctx.reply("You have no reminders.")
        rems = ""
        for i in range(len(reminders)):
            rems += f"`{reminders[i][0]}.` <t:{int(reminders[i][3])}:F> {reminders[i][2]}\n"
        await ctx.send(f"{ctx.author.mention}'s reminders:\n{rems}")

    @_bonk.command(name="remove", aliases=["delete", "remonvereminder", "remove_reminder"])
    async def _remove_reminder(self, ctx: commands.Context, index: int):
        rems = await self.bot.db.execute("SELECT ind FROM reminders WHERE user_id = ?", (ctx.author.id, ))
        rems = await rems.fetchall()
        if index not in [i[0] for i in rems]:
            return await ctx.reply("You don't have that many reminders!")

        await self.bot.db.execute("DELETE FROM reminders WHERE user_id = ? AND ind = ?", (ctx.author.id, index, ))
        await self.bot.db.commit()

        await ctx.reply("Removed reminder.")

    @commands.Cog.listener("on_ready")
    async def _bonk_on_ready(self) -> None:
        reminders = await self.bot.db.execute("SELECT * FROM reminders")
        reminders = await reminders.fetchall()

        for reminder in reminders:
            seconds = (datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(reminder[2])).total_seconds()
            self.bot.loop.call_later(seconds, self.remind(reminders[0], reminders[1]))


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Bonk(bot))