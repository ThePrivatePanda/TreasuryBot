from code import interact
from distutils.log import fatal
import re
from discord import AutoShardedClient
import nextcord
from nextcord.ext import commands, tasks
import time
import datetime
import json
import pytz


class MessageLb(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.lb_day: int = self.bot.config.get("lb_day")
        self.reset_lb_.start()
        self.update_stats.start()
        self.emotes = {
            1: "<:TDT_1:947085821675200563>",
            2: "<:TDT_2:947085688564776980>",
            3: "<:TDT_3:947085551658467368>",
            4: "<:TDT_4:947085399887589376>",
            5: "<:TDT_5:947085199915765792>",
            6: "<:TDT_6:947473601307738163>",
            7: "<:TDT_7:947473729426972682>",
            8: "<:TDT_8:947473830266404864>",
            9: "<:TDT_9:947473950374514690>",
        }

    def cog_unload(self):
        self.reset_lb_.stop()
        self.update_stats.stop()
        self.bot.unload_extension(name="cogs.MessageLb")

    def cog_load(self):
        self.reset_lb_.start()
        self.update_stats.start()
        self.bot.load_extension(name="cogs.MessageLb")

    def cog_reload(self):
        self.unload()
        self.load()


    @commands.Cog.listener("on_message")
    async def on_message_lb(self, message: nextcord.Message) -> None:
        if not message.guild or message.guild.id != 727276010600530011 or message.author.bot or not message.channel.category:
            return

        # checks to see if it meets the specifications
        category = None
        if message.content.strip() == "owo": # owo bot
            category = "owo"
        elif "owo" in message.content:
            category = "owobot"
        elif "🐸" in message.channel.name or "🤖" in message.channel.name: # dank memer channels / all bot channels
            category = "dank"
        elif message.channel.category_id == 823167859739066428: # karuta category
            category = "karuta"
        else:
            category = "overall"

        previous = await self.bot.db.execute("SELECT cd FROM lb_active_daily WHERE user_id = ? and category = ?", (message.author.id, category, ))
        cd = await previous.fetchone()

        if cd is None:
            await self.bot.db.execute("INSERT INTO lb_active_daily VALUES(?, ?, ?, ?)", (message.author.id, category, 1, time.time()))
            await self.bot.db.execute("INSERT INTO lb_active_weekly VALUES(?, ?, ?)", (message.author.id, category, 1))
            await self.bot.db.execute("INSERT INTO lb_active_monthly VALUES(?, ?, ?)", (message.author.id, category, 1))
        else:
            if category == "owo":
                two_or_ten = 10
            else:
                two_or_ten = 2
            if cd[0] > time.time()-two_or_ten:
                return
            await self.bot.db.execute("UPDATE lb_active_daily SET messages = messages + 1, cd = ? WHERE user_id = ? and category = ?", (time.time(), message.author.id, category, ))
            await self.bot.db.execute("UPDATE lb_active_weekly SET messages = messages + 1 WHERE user_id = ? and category = ?", (message.author.id, category, ))
            await self.bot.db.execute("UPDATE lb_active_monthly SET messages = messages + 1 WHERE user_id = ? and category = ?", (message.author.id, category, ))
        await self.bot.db.commit()


    async def get_top_10(self, timespan, category):
        top_10 = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_{timespan} WHERE category = ? ORDER BY messages DESC", (category, ))
        top_10 = await top_10.fetchall()
        return (sorted({i[0]: i[1] for i in top_10}.items(), key=lambda x: x[1], reverse=True))[:9]


    def beautify(self, data):
        my_string = ""
        for i in range(len(data)):
            my_string += f"{self.emotes[i+1]} `{data[i][1]}`  ﹒ <@{data[i][0]}>\n"
        return my_string

    async def announce(self, timespan):
        top_10_owo = await self.get_top_10(timespan, "owo")
        top_10_owo_bot = await self.get_top_10(timespan, "owobot")
        top_10_dank = await self.get_top_10(timespan, "dank")
        top_10_karuta = await self.get_top_10(timespan, "karuta")

        data = await self.bot.db.execute(f"SELECT * FROM lb_active_{timespan}")
        data = await data.fetchall()
        category_sort = {"dank": 0, "karuta": 0, "owo": 0, "overall": 0, "owobot": 0}
        top_users = {}

        for entry in data:
            category_sort[entry[1]] += entry[2]

            if entry[0] not in top_users.keys():
                top_users[entry[0]] = entry[2]
            else:
                top_users[entry[0]] += entry[2]

        top_users = (sorted(top_users.items(), key=lambda x: x[1], reverse= True))[:9]


        embed=nextcord.Embed(
            title=f"{timespan.title()} Message Leaderboard", colour=0x00ffea).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text=self.bot.treasury.me.display_name, icon_url=self.bot.treasury.me.display_avatar.url)


        embed.add_field(name=f"{timespan.title()} `Dank` Count", value=f"<:TDT_cyanreply:947475547280257035>{category_sort['dank']:,}")
        embed.add_field(name=f"{timespan.title()} `Karuta` Count", value=f"<:TDT_cyanreply:947475547280257035>{category_sort['karuta']:,}")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name=f"{timespan.title()} `OwO` Count", value=f"<:TDT_cyanreply:947475547280257035>{category_sort['owo']:,}")
        embed.add_field(name=f"{timespan.title()} `Owo Bot` Count", value=f"<:TDT_cyanreply:947475547280257035>{category_sort['owobot']:,}")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name=f"Top {timespan.title()} Users", value=self.beautify(top_users))
        embed.set_footer(icon_url=self.bot.user.display_avatar.url, text=f"Overall {timespan} count: {category_sort['overall']}")
        await self.bot.announcements_channel.send(embed=embed)


        await self.bot.dank_announcements.send(embed=nextcord.Embed(
            title=f"{timespan.title()} `Dank` Leaderboard",
            description=self.beautify(top_10_dank), colour=0x00ffea).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text=f'Dank count {timespan}: {category_sort["dank"]:,}', icon_url="https://cdn.discordapp.com/avatars/270904126974590976/d60c6bd5971f06776ba96497117f7f58.png")
        )

        await self.bot.karuta_announcements.send(embed=nextcord.Embed(
            title=f"{timespan.title()} `Karuta` Leaderboard",
            description=self.beautify(top_10_karuta), colour=0x00ffea).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text=f'Karuta count {timespan}: {category_sort["karuta"]:,}', icon_url="https://cdn.discordapp.com/avatars/646937666251915264/0e54d87446f106d1fd58385295ae9deb.png")
        )

        await self.bot.owo_announcements.send(embed=nextcord.Embed(
            title=f"{timespan.title()} `OwO` Leaderboard",
            description=self.beautify(top_10_owo), colour=0x00ffea).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text=f'OwO count {timespan}: {category_sort["owo"]:,}', icon_url="https://cdn.discordapp.com/avatars/408785106942164992/0b42be9386cf6fbe96861429a9774a89.png")
        )

        await self.bot.owo_bot_announcements.send(embed=nextcord.Embed(
            title=f"{timespan.title()} `OwO Bot` Leaderboard",
            description=self.beautify(top_10_owo_bot), colour=0x00ffea).set_thumbnail(url=self.bot.treasury.icon.url).set_footer(text=f'OwO count {timespan}: {category_sort["owo"]:,}', icon_url="https://cdn.discordapp.com/avatars/408785106942164992/0b42be9386cf6fbe96861429a9774a89.png")
        )

    @tasks.loop(time=datetime.time(0, 0, 0, 0, datetime.timezone.utc))
    async def reset_lb_(self):
        self.lb_day += 1
        self.bot.config.update("lb_day", self.lb_day)

        await self.bot.db.execute("DELETE FROM lb_active_daily;")

        if self.lb_day % 7 == 0:
            await self.bot.db.execute("DELETE FROM lb_active_weekly;")
        if self.lb_day % 30 == 0:
            self.lb_day = 0
            await self.bot.db.execute("DELETE FROM lb_active_monthly;")

        await self.bot.db.commit()

    @tasks.loop(minutes=10)
    async def update_stats(self):
        try:
            await self.bot.announcements_channel.purge(limit=100)
            await self.bot.dank_announcements.purge(limit=100)
            await self.bot.karuta_announcements.purge(limit=100)
            await self.bot.owo_announcements.purge(limit=100)
            await self.bot.owo_bot_announcements.purge(limit=100)
            await self.announce("monthly")
            await self.announce("weekly")
            await self.announce("daily")
        except:
            pass

    @nextcord.slash_command(name="msgs", description="Get your message stats in this server!", guild_ids=[727276010600530011])
    async def msgs_(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            description="The category for which to fetch statistics. Defaults to all.",
            choices={
                "Dank": "dank",
                "Karuta": "karuta",
                "OwO": "owo",
                "OwO Bot": "owo bot",
                "All": "all"
                },
            required=True,
        ),
        tiemspan: str = nextcord.SlashOption(
            name="timespan",
            description="The timespan for which to fetch stats. Defaults to all time periods. Calculated since midnight GMT",
            choices={
                "Daily": "daily",
                "Weekly": "weekly",
                "Monthly": "monthly",
                "All Time": "all"
                },
            required=True,
        ),
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user of whose statistics to fetch. Defaults to you!",
            required=False
        ),
    ):
        user = user or interaction.user

        today = datetime.date.today()
        midnight = datetime.datetime.combine(today, datetime.datetime.max.time()) + datetime.timedelta(hours=5, minutes=30)
        description = f"Resets at midnight: <t:{int(midnight.timestamp())}:R>"

        if category != "all":
            if tiemspan != "all":
                data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_{tiemspan} WHERE category = ? ORDER BY messages", (category, ))
                data = await data.fetchall()
                user_messages = [i[1] for i in [(a, b) for a, b in data] if i[0] == user.id]
                if not user_messages:
                    await interaction.send("Active when? I did not find any stats for you.")
                    return
                user_messages = user_messages[0]
                user_rank = data.index((user.id, user_messages))

                return await interaction.send(f"You have {user_messages} messages for timespan: `{tiemspan.title()}` and category: `{category.title()}` and your category rank is: **{user_rank}**.")
            else:
                daily_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_daily WHERE category = ? ORDER BY messages", (category, ))
                weekly_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_weekly WHERE category = ? ORDER BY messages", (category, ))
                monthly_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_monthly WHERE category = ? ORDER BY messages", (category, ))

                daily_data = await daily_data.fetchall()
                weekly_data = await weekly_data.fetchall()
                monthly_data = await monthly_data.fetchall()

                user_messages_daily = [i[1] for i in [(a, b) for a, b in daily_data] if i[0] == user.id]
                user_messages_weekly = [i[1] for i in [(a, b) for a, b in weekly_data] if i[0] == user.id]
                user_messages_monthly = [i[1] for i in [(a, b) for a, b in monthly_data] if i[0] == user.id]

                embed = nextcord.Embed(colour=0x00ffea, description=description).set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url).set_thumbnail(url=interaction.guild.icon.url).set_footer(text="Treasury", icon_url=interaction.guild.me.display_avatar.url)

                if user_messages_daily:
                    user_messages_daily = user_messages_daily[0]
                    user_rank_daily = daily_data.index((user.id, user_messages_daily))
                    embed.add_field(name=f"Daily Stats", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_daily}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_daily}**")
                if user_messages_weekly:
                    user_messages_weekly = user_messages_weekly[0]
                    user_rank_weekly = weekly_data.index((user.id, user_messages_weekly))
                    embed.add_field(name=f"Weekly Stats", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_weekly}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_weekly}**")
                if user_messages_monthly:
                    user_messages_monthly = user_messages_monthly[0]
                    user_rank_monthly = monthly_data.index((user.id, user_messages_monthly))
                    embed.add_field(name=f"Monthly Stats", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_monthly}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_monthly}**")

                if len(embed.fields) > 0:
                    await interaction.send(embed=embed)
                else:
                    await interaction.send("Active when? I did not find any stats for you.")
                return
        else:
            if tiemspan == "all":
                embed = nextcord.Embed(colour=0x00ffea, description=description).set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url).set_thumbnail(url=interaction.guild.icon.url).set_footer(text="Treasury", icon_url=interaction.guild.me.display_avatar.url)
                for category_ in ("karuta", "danks", "owo", "owobot"):
                    daily_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_daily WHERE category = ? ORDER BY messages", (category_, ))
                    weekly_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_weekly WHERE category = ? ORDER BY messages", (category_, ))
                    monthly_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_monthly WHERE category = ? ORDER BY messages", (category_, ))

                    daily_data = await daily_data.fetchall()
                    weekly_data = await weekly_data.fetchall()
                    monthly_data = await monthly_data.fetchall()

                    user_messages_daily = [i[1] for i in [(a, b) for a, b in daily_data] if i[0] == user.id]
                    user_messages_weekly = [i[1] for i in [(a, b) for a, b in weekly_data] if i[0] == user.id]
                    user_messages_monthly = [i[1] for i in [(a, b) for a, b in monthly_data] if i[0] == user.id]


                    if user_messages_daily:
                        user_messages_daily = user_messages_daily[0]
                        user_rank_daily = daily_data.index((user.id, user_messages_daily))
                        embed.add_field(name=f"Daily {category_.title()} Stats:", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_daily}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_daily}**")
                    if user_messages_weekly:
                        user_messages_weekly = user_messages_weekly[0]
                        user_rank_weekly = weekly_data.index((user.id, user_messages_weekly))
                        embed.add_field(name=f"Weekly {category_.title()} Stats:", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_weekly}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_weekly}**")
                    if user_messages_monthly:
                        user_messages_monthly = user_messages_monthly[0]
                        user_rank_monthly = monthly_data.index((user.id, user_messages_monthly))
                        embed.add_field(name=f"Monthly {category_.title()} Stats:", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_monthly}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_monthly}**")

                if len(embed.fields) > 0:
                    await interaction.send(embed=embed)
                else:
                    await interaction.send("Active when? I did not find any stats for you.")
                    return
            else:
                embed = nextcord.Embed(colour=0x00ffea, description=description).set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url).set_thumbnail(url=interaction.guild.icon.url).set_footer(text="Treasury", icon_url=interaction.guild.me.display_avatar.url)
                for category_ in ("karuta", "danks", "owo", "owobot"):
                    daily_data = await self.bot.db.execute(f"SELECT user_id, messages FROM lb_active_daily WHERE category = ? ORDER BY messages", (category_, ))
                    daily_data = await daily_data.fetchall()
                    user_messages_daily = [i[1] for i in [(a, b) for a, b in daily_data] if i[0] == user.id]
                    if user_messages_daily:
                        user_messages_daily = user_messages_daily[0]
                        user_rank_daily = daily_data.index((user.id, user_messages_daily))
                        embed.add_field(name=f"Daily {category_.title()} Stats:", value=f"<:TDT_cyanreply:947475547280257035> Messages: **{user_messages_daily}**\n<:TDT_cyanreply:947475547280257035> Rank:  **{user_rank_daily}**")
                if len(embed.fields) > 0:
                    await interaction.send(embed=embed)
                else:
                    await interaction.send("Active when? I did not find any stats for you.")
                    return


def setup(bot):
    bot.add_cog(MessageLb(bot))
