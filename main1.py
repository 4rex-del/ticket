import discord
import os
from discord.ext import commands
from discord import utils

from myserver import server_on

channelid = "1412433107574849577"  # ไอดี log
channelCategory = "1411575398780764251"  # ไอดีหมวดหมู่
adminid = "1400471054295502849"  # ไอดีแอดมิน
owner_id = "1400471054295502849"  # ไอดีเจ้าของดิส

### ( เวลารันบอทเสร็จใช้คําสั่ง !setup )

def now():
    now1 = datetime.datetime.now(tz)
    month_name = now1.month
    thai_year = now1.year
    time_str = now1.strftime('%H:%M:%S')
    return "%d/%s/%d %s" % (now1.day, month_name, thai_year, time_str)


class Message(discord.ui.Modal, title='Feedback'):
    def __init__(self):
        super().__init__(title='Ticket', timeout=None, custom_id='ticket_model_001')

    message = discord.ui.TextInput(
        label='ติดต่อแอดมิน',
        style=discord.TextStyle.long,
        placeholder='เขียนเรื่องที่ต้องการติดต่อ',
    )

    async def on_submit(self, interaction: discord.Interaction):
        message = self.message.value
        member = interaction.user
        category = discord.utils.get(member.guild.categories, id=int(channelCategory))
        ticket = utils.get(
            interaction.guild.text_channels,
            name=f"{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}"
        )

        if ticket is not None:
            embed = discord.Embed(
                title="แจ้งเตือน",
                description=f"คุณมี Ticket เปิดอยู่แล้วที่ {ticket.mention}!",
                color=0xfa0d0d
            )
            embed.set_footer(text=now())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    read_message_history=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),
            }
            channel = await interaction.guild.create_text_channel(
                f"{interaction.user.name}-{interaction.user.discriminator}",
                overwrites=overwrites,
                category=category
            )
            embed1 = discord.Embed(
                title="ดำเนินหารสำเร็จ",
                description=f"สร้างห้องสำเร็จ {channel.mention}",
                color=0x1BE51B
            )
            await interaction.response.send_message(embed=embed1, ephemeral=True)

            embed2 = discord.Embed(
                title="สร้างตั๋ว",
                description=f"{interaction.user.mention} แอดมิน <@{adminid}>\n```ติดต่อเรื่อง {message}```\nโปรดรอแอดมินมาตอบครับ",
                color=0xdddddd
            )
            embed2.set_image(
                url="https://cdn.discordapp.com/attachments/1166453203764789410/1176917209554092133/7cfef8409d92517cc9ab6a2ecf8730de.gif"
            )
            await channel.send(embed=embed2, view=Close_ticket())

            userid = interaction.user.id
            embed1 = discord.Embed(
                title="เปิด Ticket",
                description=f"เปิด Ticket โดย <@{userid}> ห้อง {channel.mention}",
                color=0x1BE51B
            )
            embed1.set_footer(text=now())
            channel1 = discord.utils.get(member.guild.channels, id=int(channelid))
            await channel1.send(embed=embed1)


class Create_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="<a:789801494396141628:1173957600241520653>",
        label="สร้างตั๋ว",
        style=discord.ButtonStyle.green,
        custom_id="ticket_button_001"
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Message())


class Close_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="<:Cross:1174025840040882277>",
        label="ปิด Ticket",
        style=discord.ButtonStyle.red,
        custom_id="ticket_button_002"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        perms = interaction.channel.overwrites_for(member)
        perms.view_channel = False
        await interaction.channel.set_permissions(member, overwrite=perms)

        await interaction.response.send_message(view=Confirm_close_ticket())

        userid = interaction.user.id
        embed = discord.Embed(
            title="ปิด Ticket",
            description=f"ปิด Ticket โดย <@{userid}> ห้อง {interaction.channel.mention}",
            color=0xfa0d0d
        )
        embed.set_footer(text=now())
        channel = discord.utils.get(member.guild.channels, id=int(channelid))
        await channel.send(embed=embed)


class Confirm_close_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="<:Bunny9:1175845773812957355>",
        label="ลบ Ticket",
        style=discord.ButtonStyle.red,
        custom_id="ticket_button_003"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()
        userid = interaction.user.id
        embed = discord.Embed(
            title="ลบ Ticket",
            description=f"ลบ Ticket โดย <@{userid}>",
            color=0xfa0d0d
        )
        embed.set_footer(text=now())
        channel = discord.utils.get(interaction.guild.channels, id=int(channelid))
        await channel.send(embed=embed)


class MyBot(commands.Bot):

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix='!',
            help_command=None,
            case_insensitive=True,
            intents=intents,
        )
        self.owner_id = int(owner_id)

    async def on_ready(self) -> None:
        streaming = discord.Streaming(
            name="พร้อมใช้งาน💜",
            url="https://www.youtube.com/"
        )
        await self.change_presence(activity=streaming)
        await self.tree.sync()
        print(f"✅ บอทออนไลน์แล้ว: {self.user}")

    async def setup_hook(self) -> None:
        self.add_view(Create_ticket())


bot = MyBot()


@bot.command()
@commands.is_owner()
async def setup(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(
        title="สอบถาม / ซื้อของ",
        description="\n\nสำหรับ สอบถาม แจ้งปัญหา ซื้อของ\nเราจะปิด ticket ภายใน 30นาที หากไม่มีการตอบกลับจากลูกค้า\nกดเล่นแบนทันที",
        color=0xdddddd
    )
    embed.set_image(
        url='https://media.discordapp.net/attachments/1411575487096164522/1411580378254147704/1276_20250831121606.png?ex=68b7cf2c&is=68b67dac&hm=ab251f6f3595d5fa4a87cae451c75dc3b2ab94c152d312398bf8620fba9f8d48&=&format=webp&quality=lossless&width=850&height=480'
    )
    embed.set_footer(text="BOT SEVER  © discord.gg/")
    await ctx.send(embed=embed, view=Create_ticket())

server_on()


bot.run(os.getenv('TOKEN'))
