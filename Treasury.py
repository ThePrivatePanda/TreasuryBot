import aiohttp
import aiosqlite
import json
from nextcord import Intents
from BotBase import BotBaseBot
from typing import List
import config_handler
from aiosqlite.core import Connection


bot: BotBaseBot = BotBaseBot(command_prefix="!!", intents=Intents.all())

cogs: List[str] = [
    "jishaku",

    "cogs.Afk",
    "cogs.Appeal",
    "cogs.Bonk",
    # "cogs.BumpPing",
    "cogs.CustomFlagger",
    "cogs.Demote",
    "cogs.Docs",
    "cogs.drop",
    "cogs.Errors",
    "cogs.Etc",
    "cogs.Events",
    "cogs.Giveaways",
    # "cogs.Lockdown",
    # "cogs.LockItUp",
    "cogs.MessageLB",
    # "cogs.Owner",
    "cogs.SelfRoles",
    "cogs.ServerGuardian",
    "cogs.SOTD",
    # "cogs.StaffWork",
    "cogs.Todo",
    "cogs.Trades",
    ]

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")

async def startup():
    bot.load_extension("cogs.Owner")
    print("Starting up...")
    # bot vars
    bot.MAX_WINNERS = bot.config.config["max_winners"]
    bot.GIVEAWAY_HOST_ID = bot.config.config["giveaway_manager"]
    bot.EVENT_HOST_ID = bot.config.config["event_manager"]
    bot.MM_ROLE_ID = bot.config.config["trusted_middleman"]
    bot.STAFF_ID = bot.config.config["staff_role"]
    bot.MOD_ID = bot.config.config["mod_role"]

    bot.appeal_guild_invite = bot.config.config["appeal_guild_invite"]
    bot.treasury_invite = bot.config.config["treasury_invite"]

    bot.persistent_views_added =  False
    print("Set bot variables...")

    await bot.wait_until_ready()
    bot.giveaway_log_channel = await bot.getch_channel(bot.config.config["gaw_log"])
    bot.treasury = await bot.getch_guild(727276010600530011)
    bot.owner = await bot.getch_user(bot.owner_id)
    bot.ghost_ping_channel = await bot.getch_channel(bot.config.config["ghost_ping_channel"])
    bot.quarantine_info_channel = await bot.getch_channel(bot.config.config["quarantine_info_channel"])
    bot.quarantine_role = bot.treasury.get_role(bot.config.config["quarantine_role"])
    bot.announcements_channel = await bot.getch_channel(bot.config.config["server_lb"])
    bot.dank_announcements = await bot.getch_channel(bot.config.config["dank_lb"])
    bot.karuta_announcements = await bot.getch_channel(bot.config.config["karuta_lb"])
    bot.owo_announcements = await bot.getch_channel(bot.config.config["owo_lb"])
    bot.owo_bot_announcements = await bot.getch_channel(bot.config.config["owo_bot_lb"])
    bot.session = aiohttp.ClientSession()
    print("Set more bot variables...")

    # db stuff
    bot.db = await aiosqlite.connect("dbs/db.sqlite3")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS afk (user_id bigint UNIQUE PRIMARY KEY, msg text, time real)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS reminders (ind bigint, user_id bigint, message text, time bigint)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS quarantine (user_id bigint UNIQUE PRIMARY KEY, time bigint)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS lb_active_daily (user_id bigint, category text, messages int, cd real)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS lb_active_weekly (user_id bigint, category text, messages int)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS lb_active_monthly (user_id bigint, category text, messages int)")
    await bot.db.commit()
    print("Setup database connection and tables...")

    # cogs
    for extension in cogs:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension {extension}")
        except Exception as e:
            exc = f"{type(e).__name__,}: {e}"
            print(f"Failed to load extension {extension}\n{exc}")
    print("Loaded all cogs...")
    bot.add_startup_application_commands()
    await bot.rollout_application_commands()
    await bot.treasury.rollout_application_commands()
    print("Synced all slash commands...")

bot.config = config_handler.Config()
bot.todo = config_handler.TodoHandler()
bot.loop.create_task(startup())
bot.run(bot.config.config["token"])
