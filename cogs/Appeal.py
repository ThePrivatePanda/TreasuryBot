from asyncio import TimeoutError
from re import match
from typing import Optional

from nextcord.ext import commands
from nextcord import (
    Button,
    ButtonStyle,
    ChannelType,
    Colour,
    Embed,
    Forbidden,
    HTTPException,
    Interaction,
    Member,
    MessageType,
    Thread,
    ThreadMember,
    Message,
    ui,
    User,
)

APPEAL_CHANNEL_ID: int = 944207520233316423
APPEAL_LOGS_CHANNEL_ID: int = 944304103624937472
STAFF_ROLE_ID: int = 944205802103795722
GUILD_ID: int = 944201132765483099
NAME_TOPIC_REGEX: str = r"(^.*?) \((.*?[0-9]{4})\)$"
CUSTOM_ID_PREFIX: str = "ta:"
WAIT_FOR_TIMEOUT: int = 6*60
timeout_message: str = "You are currently timed out, please wait until it ends before trying again"

async def get_thread_author(channel: Thread) -> Member:
    history = channel.history(oldest_first = True, limit = 1)
    history_flat = await history.flatten()
    user: User = history_flat[0].mentions[0]
    return user


async def close_appeal_thread(method: str, thread_channel: Thread, thread_author: User) -> None:
    """
    Closes a appeal thread. Is called from either the close button or the
    !!close command.
    """

    # no need to do any of this if the thread is already closed.
    if (thread_channel.locked or thread_channel.archived):
        return

    if not thread_channel.last_message or not thread_channel.last_message_id:
        _last_msg: Optional[Message] = (await thread_channel.history(limit = 1).flatten())[0]
    else:
        _last_msg: Message = thread_channel.get_partial_message(thread_channel.last_message_id)

    thread_jump_url: str = _last_msg.jump_url

    embed_reply: Embed = Embed(title="This thread has now been closed",
                        description="This case has been closed. Please do not open a new one continuing this thread without due proof.",
                        colour=Colour.dark_theme())

    await thread_channel.send(embed=embed_reply)  # Send the closing message to the appeal thread
    await thread_channel.edit(locked = True, archived = True)  # Lock thread
    await thread_channel.guild.get_channel(APPEAL_LOGS_CHANNEL_ID).send(embed=Embed(
        title="Thread Closed",
        description=f"Thread by {thread_author.mention} has been closed by {method}\nAccess by clicking [here]({thread_jump_url})")
        .set_thumbnail(url=thread_channel.guild.icon.url)
        .set_author(name=thread_author.name, icon_url=thread_author.display_avatar.url))  # Send closing message to logs channel,

    # Make some slight changes to the previous thread-closer embed
    # to send to the user via DM.
    embed_reply.title = "Your appeal thread in the Treasury appeal server has been closed."
    embed_reply.description += f"\n\nYou can use [**this link**]({thread_jump_url}) to access the archived thread for future reference"
    if thread_channel.guild.icon:
        embed_reply.set_thumbnail(url=thread_channel.guild.icon.url)
    try:
        await thread_author.send(embed=embed_reply)
    except (HTTPException, Forbidden):
        pass

class AppealButton(ui.Button["AppealView"]):
    def __init__(self, *, style: ButtonStyle, custom_id: str) -> None:
        super().__init__(label = f"Appeal", style = style, custom_id = f"{CUSTOM_ID_PREFIX}{custom_id}")

    async def create_appeal_thread(self, interaction: Interaction) -> Thread:
        thread: Thread = await interaction.channel.create_thread(
            name = f"{interaction.user}",
            type = ChannelType.public_thread,
        )

        thread_jump_url: str = f"https://discord.com/channels/{interaction.guild.id}/{thread.id}/"

        await interaction.guild.get_channel(APPEAL_LOGS_CHANNEL_ID).send(embed=Embed(
            title="Thread Opened",
            description=f"Thread opened by: {interaction.user.mention}\nClick [here]({thread_jump_url}) to access it.")
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url))  # Send closing message to logs channel,

        em: Embed = Embed(
            title = "Appeal thread",
            colour = Colour.blurple(),
            description = "Please state the reason for your ban.\nNext, explain why you were banned, i.e. your side of the story.\nInclude relevant proof as well as *why* we should appeal you."
        )
        em.set_footer(text = "You can close this thread with the button or !!close command.")

        close_button_view = ThreadCloseView()

        msg: Message = await thread.send(
            content = interaction.user.mention,
            embed = em,
            view = close_button_view
        )

        # it's a persistent view, we only need the button.
        close_button_view.stop()
        await msg.pin(reason = "First message in appeal thread with the close button.")
        return thread

    async def __launch_wait_for_message(self, thread: Thread, interaction: Interaction) -> None:
        assert self.view is not None

        def is_allowed(message: Message) -> bool:
            return message.author.id == interaction.user.id and message.channel.id == thread.id and not thread.archived  # type: ignore

        try:
            await self.view.bot.wait_for("message", timeout=WAIT_FOR_TIMEOUT, check=is_allowed)
        except TimeoutError:
            return await close_appeal_thread("TIMEOUT", thread, interaction.user)
        else:
            return await thread.send(f"<@&{STAFF_ROLE_ID}>", delete_after=5)

    async def callback(self, interaction: Interaction) -> None:
        confirm_view = ConfirmView()

        def disable_all_buttons():
            for _item in confirm_view.children:
                _item.disabled = True

        confirm_content: str = f"Are you really sure you want to make an appeal thread?"

        await interaction.send(content = confirm_content, ephemeral = True, view = confirm_view)
        await confirm_view.wait()

        if confirm_view.value is False or confirm_view.value is None:
            disable_all_buttons()
            content: str = "Ok, cancelled." if confirm_view.value is False else f"~~{confirm_content}~~ I guess not..."
            await interaction.edit_original_message(content = content, view = confirm_view)
        else:
            disable_all_buttons()
            await interaction.edit_original_message(content = "Created!", view = confirm_view)
            created_thread: Thread = await self.create_appeal_thread(interaction)
            await self.__launch_wait_for_message(created_thread, interaction)


class AppealView(ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout = None)
        self.bot: commands.Bot = bot

        self.add_item(AppealButton(style = ButtonStyle.blurple, custom_id = "appeal"))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.timeout is not None:
            await interaction.send(timeout_message, ephemeral=True)
            return False

        return await super().interaction_check(interaction)

class ConfirmButton(ui.Button["ConfirmView"]):
    def __init__(self, label: str, style: ButtonStyle, *, custom_id: str) -> None:
        super().__init__(label = label, style = style, custom_id = f"{CUSTOM_ID_PREFIX}{custom_id}")

    async def callback(self, interaction: Interaction) -> None:
        self.view.value = True if self.custom_id == f"{CUSTOM_ID_PREFIX}confirm_button" else False
        self.view.stop()


class ConfirmView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = 10.0)
        self.value = None
        self.add_item(ConfirmButton("Yes", ButtonStyle.green, custom_id = "confirm_button"))
        self.add_item(ConfirmButton("No", ButtonStyle.red, custom_id = "decline_button"))


class ThreadCloseView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @ui.button(label = "Close", style = ButtonStyle.red, custom_id = f"{CUSTOM_ID_PREFIX}thread_close")  # type: ignore
    async def thread_close_button(self, button: Button, interaction: Interaction) -> bool:
        button.disabled = True
        await interaction.response.edit_message(view = self)
        thread_author: User = await get_thread_author(interaction.channel)  # type: ignore
        await close_appeal_thread("BUTTON", interaction.channel, thread_author)

    async def interaction_check(self, interaction: Interaction) -> bool:

        # because we aren't assigning the persistent view to a message_id.
        if not isinstance(interaction.channel, Thread) or interaction.channel.parent_id != APPEAL_CHANNEL_ID:
            return False

        if (interaction.channel.archived or interaction.channel.locked):  # type: ignore
            return False

        if isinstance(interaction.user, Member) and interaction.user.timeout is not None:
            await interaction.send(timeout_message, ephemeral=True)
            return False

        thread_author = await get_thread_author(interaction.channel)  # type: ignore
        if interaction.user.id == thread_author.id or interaction.user.get_role(STAFF_ROLE_ID):  # type: ignore
            return True
        else:
            await interaction.send("You are not allowed to close this thread.", ephemeral=True)
            return False

class AppealCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.loop.create_task(self.create_views())

    async def create_views(self) -> None:
        if getattr(self.bot, "appeal_view_set", False) is False:
            self.bot.appeal_view_set = True
            self.bot.add_view(AppealView(self.bot))
            self.bot.add_view(ThreadCloseView())

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.channel.id == APPEAL_CHANNEL_ID and message.type is MessageType.thread_created:
            await message.delete(delay = 5)
        if isinstance(message.channel, Thread) and \
                message.channel.parent_id == APPEAL_CHANNEL_ID and \
                message.type is MessageType.pins_add:
            await message.delete(delay = 10)

    @commands.Cog.listener()
    async def on_thread_member_remove(self, member: ThreadMember) -> None:
        thread: Thread = member.thread
        if thread.parent_id != APPEAL_CHANNEL_ID or thread.archived:
            return

        thread_author = await get_thread_author(thread)
        if member.id != thread_author.id:
            return

        await close_appeal_thread("EVENT", thread, thread_author)

    @commands.command(name="invite", aliases=["appeal"])
    async def invite(self, ctx: commands.Context, destination=None) -> None:
        if destination == "appeal":
            return await ctx.send(self.bot.appeal_guild_invite)
        elif destination in ("main", "home", "treasury"):
            return await ctx.send(self.bot.treasury_invite)
        else:
            return await ctx.send(f"Appeal server invite: {self.bot.appeal_guilde_invite}\nMain server invite: {self.bot.treasury_invite}")

    @commands.command()
    @commands.is_owner()
    async def appeal_menu(self, ctx: commands.Context) -> None:
        await ctx.send(embed=Embed(description="""
This Server is for The Treasury APPEALS only.

Below this message, you will find a button to open an appeal ticket. When the channel is created, please answer the following questions.

**1) Provide your Discord ID.**
Click [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) if you need help finding your ID.

**2) Include the reason for your ban.**
This can be found from the DM you received from If you are unable to find the same, please state you do not know the reason

**3) Give your side of the story of the incident.**
This is your chance to give us your side of the story.

**4) Provide relevant proof.**
Proof is everything. Include all the proof you can.

**5) What can you do in the future to avoid the situation that caused your ban?**
Please be thoughtful in your explanation.

After this, please absolutely **DO NOT ping** any staff member.
Repeated offence will result in **moderation action**, as well as the chances of your appeal diminishing.
""", color=Colour.yellow()).set_author(name="Appeal Guide").set_thumbnail(url=ctx.guild.icon.url).set_footer(text=f"Treasury Appeals", icon_url=self.bot.user.display_avatar.url))

        await ctx.send(
            content = "**:white_check_mark: If you've read the guidelines above, click a button to create an appeal thread!**",
            view = AppealView(self.bot)
        )

    @commands.command()
    async def close(self, ctx: commands.Context) -> None:
        if not isinstance(ctx.channel, Thread) or ctx.channel.parent_id != APPEAL_CHANNEL_ID:
            return

        first_thread_message: Message = (await ctx.channel.history(limit=1, oldest_first=True).flatten())[0]
        thread_author = first_thread_message.mentions[0]
        if not (ctx.author.id == thread_author.id or ctx.author.get_role(STAFF_ROLE_ID)):
            return await ctx.send("You are not allowed to change the topic of this thread.")

        thread_author: User = await get_thread_author(ctx.channel)
        await close_appeal_thread("COMMAND", ctx.channel, thread_author)

    @commands.command()
    @commands.has_role(STAFF_ROLE_ID)
    async def topic(self, ctx: commands.Context, *, topic: str) -> None:
        if not (isinstance(ctx.channel, Thread) and ctx.channel.parent.id == APPEAL_CHANNEL_ID):  # type: ignore
            return await ctx.send("This command can only be used in appeal threads!")

        author = match(NAME_TOPIC_REGEX, ctx.channel.name).group(2)  # type: ignore
        await ctx.channel.edit(name=f"{topic} ({author})")

    @commands.Cog.listener("on_thread_member_join")
    async def on_thread_member_join(self, member: Member) -> None:
        first_thread_message: Message = (await member.thread.history(limit=1, oldest_first=True).flatten())[0]
        thread_author: User = first_thread_message.mentions[0]

        if not (member.id == thread_author.id or member.thread.guild.get_member(member.id).get_role(STAFF_ROLE_ID)):
            if member.thread.channel.id == APPEAL_CHANNEL_ID:
                await member.thread.remove_user(member)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(AppealCog(bot))
