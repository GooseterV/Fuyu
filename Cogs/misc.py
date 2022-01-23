import itertools
import random
import time
from datetime import datetime

import discord
from discord.channel import VocalGuildChannel
from discord.ext import commands
from googletrans import Translator
from pytz import timezone

tz = timezone('US/Eastern')
translator = Translator()
class MiscCog(commands.Cog, name="Miscellaneous Commands"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
		
	@commands.command(name = "ping",
					usage="",
					description = "Display the bot's ping.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def ping(self, ctx):
		before = time.monotonic()
		message = await ctx.send("🏓 Pong !")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
	
	@commands.command(name = "info",
					usage="",
					description = "Displays info about the bot.",
					aliases=["information"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def info(self, ctx):
		footers = ["Powered by discord.py", "nobody even reads these", "Created by Goose#4825", "Fuyu Bot 2021", "fuyu is just winter in japanese", "冬のボット2021", "Fuyu v0.1", "冬バージョン0.1"]
		random.shuffle(footers)
		before = time.monotonic()
		currenttime = datetime.now(tz)
		embed = discord.Embed(title="Information", color=1356771, timestamp=currenttime)
		embed.set_author(name=self.bot.user.name, icon_url="https://cdn.discordapp.com/avatars/878388115625115668/db239028190888b382675126aef5a416.webp?size=96")
		embed.set_image(url="https://cdn.discordapp.com/attachments/847500838825754649/899379695525703720/fuyu_banner_resized.png")
		embed.set_footer(text=random.choice(footers))
		embed.add_field(name="Latency", value=f"0 ms", inline=True)
		embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", inline=True)
		embed.add_field(name="Users", value=f"{sum([guild.member_count for guild in self.bot.guilds])}", inline=True)
		embed.add_field(name="Channels", value=f"{len(list(self.bot.get_all_channels()))}", inline=True)
		embed.add_field(name="Roles", value=f"{len([role for role in list(itertools.chain.from_iterable([guild.roles for guild in self.bot.guilds])) if role.name != '@everyone'])}", inline=True)
		embed.add_field(name="Emojis", value=f"{len(self.bot.emojis)}", inline=True)
		embed.add_field(name="Commands", value=f"{len(self.bot.commands)}", inline=True)
		msg = await ctx.send(embed=embed)
		ping = (time.monotonic() - before) * 1000
		embed.set_field_at(0, value=f"{int(ping)} ms", name="Latency", inline=True)
		await msg.edit(embed=embed)

	@commands.command(name = "translate",
					usage="<source-language> <destination-language> {content}",
					description = "Translates text into another language.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def translate(self, ctx, sourcelang, destlang, content):	
		result = translator.translate(text=content, src=sourcelang, dest=destlang)
		embed = discord.Embed(title=f"{ctx.author.name}'s Translator", description="", color = 1356771)
		embed.add_field(name="""Translated""", value=f"""```> {content}```
		({sourcelang})""", inline=False)
		embed.add_field(name="""To""", value=f"""```> {result.text}```
		({destlang})""", inline=False)
		embed.set_footer(text="Powered by Google Translate")
		await ctx.send(embed=embed)

	@commands.command(name = "echo",
					usage="{message} {channel}",
					description = "Echos a message into another channel")
	@commands.cooldown(1, 2, commands.BucketType.member)
	@commands.has_permissions(administrator=True)
	async def echo(self, ctx, channelid:int, *, message):
		channel = self.bot.get_channel(channelid)
		await channel.send(message)

def setup(bot:commands.Bot):
	bot.add_cog(MiscCog(bot))
