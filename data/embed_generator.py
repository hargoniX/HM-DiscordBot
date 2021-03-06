import json
import os
import discord
from settings import Directories, ServerIds
from utils import UserError
import time


class HelpError(UserError):
    pass


class Embedgenerator:

    def __init__(self, file):
        os.chdir(Directories.DATA_DIR)
        self.file = rf'{os.getcwd()}/{file}.json'

        if not os.path.isfile(self.file):
            raise HelpError("Hilfe fehlgeschlagen.\n"
                            "!help für mehr Informationen")

    def read(self):

        # noinspection PyBroadException
        try:
            with open(self.file, "r", encoding="utf-8")as f:
                payload = json.loads(f.read())
        except Exception as e:
            print(e)
            payload = None
        finally:
            os.chdir(Directories.ROOT_DIR)
            # noinspection PyUnboundLocalVariable
            return payload

    def generate(self):

        # noinspection PyShadowingNames
        jroot = self.read()

        if jroot:
            embed = discord.Embed(title=jroot["embeds"][0]["title"],
                                  colour=discord.Colour(0x12d4ca),
                                  description=jroot["embeds"][0]["description"])

            for x in jroot["embeds"][0]["fields"]:
                try:
                    inline = x["inline"]
                except KeyError:
                    inline = False
                embed.add_field(name=x["name"],
                                value=x["value"],
                                inline=inline)
            return embed

        else:
            embed = discord.Embed(title="Error",
                                  colour=discord.Colour(0x12d4ca),
                                  description="Diese Hilfe scheint es noch nicht zu geben.")
            return embed


class BugReport:

    # noinspection PyShadowingNames
    def __init__(self, bot, ctx, e):
        self.bot = bot
        self.ctx = ctx
        self.channel = bot.get_channel(id=ServerIds.DEBUG_CHAT)
        self.embed = discord.Embed(colour=discord.Colour(0x12d4ca),
                                   description="")

        self.embed.set_author(name="Bug Report")
        self.embed.set_footer(text=f"Erstellt am {time.strftime('%d.%m.%Y %H:%M:%S')}")

        self.embed.add_field(name="Error:",
                             value=e,
                             inline=False)

    def user_details(self):
        self.embed.add_field(name="Author",
                             value=f"Name: `{self.ctx.author.name}`\n"
                                   f"ID: `{self.ctx.author.id}`",
                             inline=False)

        self.embed.add_field(name="Command:",
                             value=f"`{self.ctx.message.content}`",
                             inline=False)

        try:
            roles = ""
            for x in self.ctx.author.roles:
                roles += f"{x.name}\n"

            self.embed.add_field(name="Roles:",
                                 value=roles,
                                 inline=False)
        except AttributeError:
            pass

        if self.ctx.guild:
            guild_id = self.ctx.guild.id
            channel_id = self.ctx.channel.id
            message_id = self.ctx.message.id
            value = f"https://discordapp.com/channels/{guild_id}/{channel_id}/{message_id}"

        else:
            value = "Privatnachricht"
        self.embed.add_field(name="Link to message",
                             value=value,
                             inline=False)

    async def reply(self):
        await self.ctx.send("Nicht klassifizierter Fehler. Ein Report wurde erstellt.")
        await self.channel.send(embed=self.embed)
