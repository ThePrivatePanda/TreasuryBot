from aiosqlite import Cursor
from nextcord.channel import TextChannel
from nextcord.ext import commands
from nextcord import Message
from typing import Any, List
import time
from BotBase import BotBaseBot

class AFK(commands.Cog):
    def __init__(self, bot: BotBaseBot):
        self.bot: BotBaseBot = bot


    async def get_afk_users(self) -> List[int]:
        return [
            i[0]
            for i in await (await self.bot.db.execute("SELECT user_id FROM afk")).fetchall()
        ]

    async def get_afk_message(self, id: int) -> tuple[str, float]:
        data_raw: Cursor = await self.bot.db.execute(f"SELECT msg, time FROM afk WHERE user_id = ?", (id,))
        data = await data_raw.fetchone()
        return data

    async def write_afk(self, id: int, message: str, time: float) -> None:
        await self.bot.db.execute(
            "INSERT OR REPLACE into afk (user_id, msg, time) VALUES(?, ?, ?)", (id, message, time, )
        )
        await self.bot.db.commit()

    async def remove_afk(self, id: int) -> None:
        await self.bot.db.execute("DELETE FROM afk WHERE user_id = ?", (id, ))
        await self.bot.db.commit()

    async def go_afk(self, ctx: commands.Context, message: str, time: float):
        if id in await self.get_afk_users():
            await self.remove_afk(ctx.author.id)
        await self.write_afk(ctx.author.id, message, time)

    @commands.group(invoke_without_command=True)
    async def afk(self, ctx: commands.Context[commands.Bot], *, msg: str ="getting a life"):

        if not any(i in (731665988059136021, 863021165370540043) for i in [i.id for i in ctx.author.roles]) and not ctx.author.id == 736147895039819797:
            await ctx.reply("You are not allowed to use this command.")
            return
        if "[AFK]" in ctx.message.author.display_name:
            await ctx.message.author.edit(nick=ctx.message.author.display_name.replace("[AFK]", ""))
        await self.go_afk(ctx, msg, time.time())

        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        await ctx.reply(f"You are now afk with reason: {msg}")


    @afk.command(name="ignore")
    async def afk_ignore(self, ctx: commands.Context, channel: TextChannel) -> None:
        if ctx.author.id not in (736147895039819797, 752299909755043900) or not ctx.author.guild_permissions.manage_guild:
            return
        old_config = self.bot.config.get("afk_ignored_channels")
        if channel.id in old_config:
            return await ctx.reply("That channel is already afk ignored.")

        old_config.append(channel.id)
        self.bot.config.update("afk_ignored_channels", old_config)

        await ctx.reply(f"Mentions in {channel.mention} will no longer trigger afk.")

    @afk.command(name="unignore", aliases=["removeignore", "ignore_remove", "listen"])
    async def afk_ignore_rem_(self, ctx, channel: TextChannel) -> None:
        if ctx.author.id not in (736147895039819797, 752299909755043900) or not ctx.author.guild_permissions.manage_guild: # only allow me and ninja to edit
            return

        old_config = self.bot.config.get("afk_ignored_channels")
        if channel.id not in old_config:
            return await ctx.reply("That channel is already not ignored for afk.")

        old_config.remove(channel.id)
        self.bot.config.update("afk_ignored_channels", old_config)

        await ctx.reply(f"Mentions in {channel.mention} will no longer trigger afk.")


    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.bot:
            return
        if msg.channel.id in self.bot.config.get("afk_ignored_channels"):
            return

        afk_users = await self.get_afk_users()

        """
        Two things can happen.
            - author if afk.
                - if 
                - inherit if they pinged someone.
            - author is not afk, check if ping
            - channel mention
        """

        if msg.content.startswith("!!afk ignore") and msg.channel_mentions[0] == msg.channel:
            return

        if msg.author.id in afk_users:
            if "[AFK]" in msg.author.display_name:
                await msg.author.edit(nick=msg.author.display_name.replace("[AFK]", ""))

            await self.remove_afk(msg.author.id)
            await msg.reply("Welcome back from afk!")

        if not msg.mentions:
            return

        temp_message = ""
        for user in msg.mentions:
            if user.id in afk_users:
                afk_reason, afk_since = await self.get_afk_message(user.id)
                temp_message = f"{user.name} is afk with reason: {afk_reason} since <t:{int(afk_since)}:F>"

        if temp_message == "":
            return
        if len(temp_message) > 2000:
            return await msg.reply("Seriously, mention so many AFK users in a message next time and I'll mute you.")

        await msg.reply(temp_message)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AFK(bot))
