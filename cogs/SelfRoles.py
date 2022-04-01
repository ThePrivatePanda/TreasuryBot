import nextcord

from nextcord.ext import commands

async def edit_roles(interaction, values, rem_all=False):
    changes = []
    add_roles = []
    remove_roles = []
    if rem_all is False:
        for role_id in values:
            role = interaction.guild.get_role(int(role_id))
            if role in interaction.user.roles:
                remove_roles.append(role)
                changes.append(f"<:TDT_crossw:947123976323366963> {role.name}")
            elif role not in interaction.user.roles:
                add_roles.append(role)
                changes.append(f"<:TDT_tick:946820484685783100> {role.name}")
    else:
        for role_id in rem_all:
            role = interaction.guild.get_role(int(role_id))
            if role in interaction.user.roles:
                remove_roles.append(role)
        changes.append("ALL roles of this dropdown were removed.")

    await interaction.user.add_roles(*add_roles)
    await interaction.user.remove_roles(*remove_roles)

    await interaction.followup.send(embed=nextcord.Embed(
        title="Success!",
        description="The following changes were done:\n" + "\n".join(changes),
        colour=0x00ffea
        )
        .set_thumbnail(url=interaction.guild.icon.url)
        .set_footer(text="TreasuryBot", icon_url=interaction.guild.me.display_avatar.url),
        ephemeral=True
        )


class AccessDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Dank Memer Player', description='Gain access to dank memer channels', value='853389527304110082'),
            nextcord.SelectOption(label='Karuta Player', description='Gain access to karuta channels', value='906158516090306620'),
            nextcord.SelectOption(label='OwO Player', description='Gain access to OwO channels', value='853674063783526400'),
            nextcord.SelectOption(label='RPG Player', description='Gain access to RPG channels', value='822925411183886336'),
            nextcord.SelectOption(label='Poketwo Player', description='Gain access to poketwo channels', value='823262683373240420'),
            nextcord.SelectOption(label='Mudae Player', description='Gain access to mudae channels', value='824708462818361375'),
            nextcord.SelectOption(label='Other Bots User', description='Gain access to all-bots channels', value='811891673604161546'),
        ]

        super().__init__(placeholder='Select upto 7 access roles...', min_values=0, max_values=7, options=self.my_options_, custom_id="access_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class PingDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Announcement ping', description='Get pinged on an announcement', value='804162649016500234'),
            nextcord.SelectOption(label='Chat revive ping', description='Help us keep the server active?', value='810188479954157628'),
            nextcord.SelectOption(label='Nitro giveaway ping', description='Get pinged when a nitro giveaway takes place!', value='834894650749616159'),
            nextcord.SelectOption(label='Partners ping', description='Check out our new partners!', value='747841749887615046'),
            nextcord.SelectOption(label='No Partnership Ping', description='DONT get pinged when a partnership happens.', value='799687210366140466'),
        ]

        super().__init__(placeholder='Select upto 4 ping roles...', min_values=0, max_values=4, options=self.my_options_, custom_id="ping_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        print(self.values)
        if len(self.values) > 0:
            values = [int(i) for i in self.values]
            if 747841749887615046 in values and 799687210366140466 in values:
                return await interaction.followup.send("Don't try to break me.", ephemeral=True)
            await edit_roles(interaction, values)
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class ColourDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Blue', description='Make your name appear blue in chat!', value='730811726886469692'),
            nextcord.SelectOption(label='Green', description='Make your name appear green in chat!', value='730813071454371911'),
            nextcord.SelectOption(label='Red', description='Make your name appeal red in chat!', value='730812444804644875'),
            nextcord.SelectOption(label='Yellow', description='Make your name appear yellow in chat!', value='730811229672701982'),
            nextcord.SelectOption(label='Purple', description='Make your name appear purple in chat!', value='730812697247088721'),
        ]

        super().__init__(placeholder='Select your colour role!', min_values=0, max_values=5, options=self.my_options_, custom_id="colour_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class AgeDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='18+', description='damn big man', value='809613202752667698'),
            nextcord.SelectOption(label='13-17', description='ayo', value='809612627948208149'),
            nextcord.SelectOption(label='-13', description='are you sure about that?', value="0"),
        ]

        super().__init__(placeholder='Select an age role!', min_values=0, max_values=1, options=self.my_options_, custom_id="colour_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            if self.values[0] == "0":
                return await interaction.followup.send("Are you sure about that?", ephemeral=True)
            await edit_roles(interaction, [int(self.values[0])])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])



class DankRolesDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Giveaway ping', description='Get pinged when a dank giveaway happens!', value='730814805308473424'),
            nextcord.SelectOption(label='Heist Ping', description='Get pinged when an in-server heist is about to take place!', value='738807828877279293'),
            nextcord.SelectOption(label='Event ping', description='Get pinged when an in-server event takes place!', value="758725180578201642"),
            nextcord.SelectOption(label='No Partnership Ping', description='do NOT get pinged for partnerships :', value="799687210366140466"),
            nextcord.SelectOption(label='Outside Heist Ping', description='Get pinged when a heist happens in a partered server!', value="806638313716711425"),
        ]

        super().__init__(placeholder='Select some Dank roles!', min_values=0, max_values=5, options=self.my_options_, custom_id="dank_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])



class KarutaRolesDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Karuta Giveaway ping', description='Get pinged when a karuta giveaway happens!', value='855769479026966538'),
            nextcord.SelectOption(label='Server Drop Ping', description='Get pinged when a server drop happens!', value='929330689868963850'),
            nextcord.SelectOption(label='Event ping', description='Get pinged when an in-server karuta event takes place!', value="758725180578201642"),
        ]

        super().__init__(placeholder='Select some Karuta roles!', min_values=0, max_values=3, options=self.my_options_, custom_id="karuta_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class RpgRolesDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='RPG Giveaway ping', description='Get pinged when a RPG giveaway happens!', value='730814805308473424'),
        ]

        super().__init__(placeholder='Select some RPG roles!', min_values=0, max_values=1, options=self.my_options_, custom_id="rpg_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class PoketwoRolesDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='Giveaway ping', description='Get pinged when a poketwo giveaway happens!', value='855769479026966538'),
            nextcord.SelectOption(label='Poketwo Tournmanets', description='Get pinged when a poketwo tournament happens!', value='854394470161842186'),
            nextcord.SelectOption(label='Incense', description='Incense!', value="915295516789735507"),
        ]

        super().__init__(placeholder='Select some Poketwo roles!', min_values=0, max_values=3, options=self.my_options_, custom_id="poketwo_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])


class OwoRolesDropdown(nextcord.ui.Select):
    def __init__(self):
        self.my_options_ = [
            nextcord.SelectOption(label='OwO Gaw & Events', value='865260438102999061'),
            nextcord.SelectOption(label='OwO Distorted Ping', value='863488059412840468'),
            nextcord.SelectOption(label='OwO Shop Ping', value="863488609515339786"),
        ]

        super().__init__(placeholder='Select some OwO roles!', min_values=0, max_values=3, options=self.my_options_, custom_id="owo_roles")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=True)
        if len(self.values) > 0:
            await edit_roles(interaction, [int(i) for i in self.values])
        else:
            await edit_roles(interaction, True, [i.value for i in self.my_options_])





class AccessDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(AccessDropdown())

class PingDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(PingDropdown())

class ColourDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(ColourDropdown())

class AgeDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(AgeDropdown())


class DankRolesDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(DankRolesDropdown())


class KarutaRolesDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(KarutaRolesDropdown())


class RpgRolesDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(RpgRolesDropdown())


class PoketwoRolesDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(PoketwoRolesDropdown())


class OwoRolesDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(OwoRolesDropdown())





class SelfRoles(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.bot.loop.create_task(self.create_views())

    async def create_views(self):
        if not self.bot.persistent_views_added:
            self.bot.add_view(AccessDropdownView())
            self.bot.add_view(PingDropdownView())
            self.bot.add_view(ColourDropdownView())
            self.bot.add_view(AgeDropdownView())
            self.bot.add_view(DankRolesDropdownView())
            self.bot.add_view(KarutaRolesDropdownView())
            self.bot.add_view(RpgRolesDropdownView())
            self.bot.add_view(PoketwoRolesDropdownView())
            self.bot.add_view(OwoRolesDropdownView())
            self.bot.persistent_views_added = True

    @commands.command()
    @commands.is_owner()
    async def alldropdowns(self, ctx):
        commands = self.get_commands()
        commands.remove(ctx.command)
        for command in commands:
            await ctx.invoke(command)

    @commands.command()
    @commands.is_owner()
    async def botroles(self, ctx):
        """Sends a message with our dropdown containing access roles view"""
        view = AccessDropdownView()
        embed = nextcord.Embed(title="Bot Access Roles", description="""
Select some roles to get access to bot channels!

<:TDT_PepeHappy:768943608850022440> ﹒ <@&853389527304110082>
<:TDT_Love:795644995545333790> ﹒ <@&906158516090306620>
<:TDT_owo:822907036375056395> ﹒ <@&853674063783526400>
<:TDT_rpgepiccoin:822940392017100850> ﹒ <@&822925411183886336>
<:TDT_pika_sip:926573490289647666> ﹒ <@&823262683373240420>
<:TDT_wownice:796663661539622912> ﹒ <@&824708462818361375>
<:TDT_NyaFlowers:799666115662970900> ﹒ <@&811891673604161546>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def pingroles(self, ctx):
        """Sends a message with our dropdown containing ping roles view"""
        view = PingDropdownView()
        embed = nextcord.Embed(title="Ping Roles", description="""
Select some roles to get pinged on certain events!

<:TDT_1:947085821675200563> ﹒ <@&804162649016500234>
<:TDT_2:947085688564776980> ﹒ <@&810188479954157628>
<:TDT_3:947085551658467368> ﹒ <@&834894650749616159>
<:TDT_4:947085399887589376> ﹒ <@&747841749887615046>
<:TDT_5:947085199915765792> ﹒ <@&799687210366140466>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def colourroles(self, ctx):
        """Sends a message with our dropdown containing colour roles view"""
        view = ColourDropdownView()
        embed = nextcord.Embed(title="Colour Roles", description="""
Select a role to make your name appear coloured in the chat!

<:TDT_1:947085821675200563> ﹒ <@&730811726886469692>
<:TDT_2:947085688564776980> ﹒ <@&730813071454371911>
<:TDT_3:947085551658467368> ﹒ <@&730812444804644875>
<:TDT_4:947085399887589376> ﹒ <@&730811229672701982>
<:TDT_5:947085199915765792> ﹒ <@&730812697247088721>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def ageroles(self, ctx):

        """Sends a message with our dropdown containing age roles view"""
        view = AgeDropdownView()
        embed = nextcord.Embed(title="Age Roles", description="""
Select a role to let people know about you!

<:TDT_1:947085821675200563> ﹒ <@&809613202752667698>
<:TDT_2:947085688564776980> ﹒ <@&809612627948208149>
<:TDT_3:947085551658467368> ﹒ Below 13, Are you sure about that?
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def dankroles(self, ctx):
        """Sends a message with our dropdown containing dank roles view"""
        view = DankRolesDropdownView()
        embed = nextcord.Embed(title="Dank Roles", description="""
If you have claimed these roles in other channels do not react
<a:TDT_giveaway:805879267883876352> ﹒ <@&730814805308473424>
<a:TDT_joinheist:805808790833856512> ﹒ <@&738807828877279293>
<:TDT_celebrate:828603083684446238> ﹒ <@&758725180578201642>
<:TDT_PepePing:768943608510152715> ﹒ <@&799687210366140466>
<a:TDT_pepehacker:806675236434214932> ﹒ <@&806638313716711425>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def karutaroles(self, ctx):
        """Sends a message with our dropdown containing kqrutq roles view"""
        view = KarutaRolesDropdownView()
        embed = nextcord.Embed(title="Karuta Roles", description="""
If you have claimed these roles in other channels do not react
<a:TDT_giveaway:805879267883876352> ﹒ <@&855769479026966538>
<a:TDT_shrug:836013887966937088> ﹒ <@&929330689868963850>
<a:TDT_Meong_Cute:851260392797110322> ﹒ <@&758725180578201642>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def rpgroles(self, ctx):
        """Sends a message with our dropdown containing rpg roles view"""
        view = RpgRolesDropdownView()
        embed = nextcord.Embed(title="RPG Roles", description="""
If you have claimed these roles in other channels do not react
<a:TDT_giveaway:805879267883876352> ﹒ <@&730814805308473424>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def poketworoles(self, ctx):
        """Sends a message with our dropdown containing poketwo roles view"""
        view = PoketwoRolesDropdownView()
        embed = nextcord.Embed(title="Poketwo Roles", description="""
If you have claimed these roles in other channels do not react
<:TDT_rich:795642645107048488> ﹒ <@&730814805308473424>
<:TDT_pika_sip:926573490289647666> ﹒ <@&854394470161842186>
<:TDT_wow:795644802917335062> ﹒ <@&915295516789735507>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()


    @commands.command()
    @commands.is_owner()
    async def oworoles(self, ctx):
        """Sends a message with our dropdown containing owo roles view"""
        view = OwoRolesDropdownView()
        embed = nextcord.Embed(title="OwO Roles", description="""
If you have claimed these roles in other channels do not react
<:TDT_Love:795644995545333790> ﹒ <@&865260438102999061>
<a:TDT_joinheist:805808790833856512> ﹒ <@&863488059412840468>
<:TDT_cutelol:863489437291380767> ﹒ <@&863488609515339786>
""", colour=0x00ffea).set_thumbnail(url=ctx.guild.icon.url).set_footer(text="TreasuryBot", icon_url=ctx.guild.me.display_avatar.url)
        await ctx.send(embed=embed, view=view)
        # await ctx.message.delete()



def setup(bot):
    bot.add_cog(SelfRoles(bot))
