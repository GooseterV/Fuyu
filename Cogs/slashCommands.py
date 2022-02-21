import colorsys
import datetime
import json
import os
import random
import sys
import time
from datetime import datetime

import aiohttp
import discord
import pyspectrum
from colormath.color_objects import LuvColor
from discord import AsyncWebhookAdapter, Webhook
from discord import guild
from discord.ext import commands
from discord.ext.commands.converter import _get_from_guilds
from discord.http import Route
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp
from pytz import timezone

import Cogs.colors as colorFuncs

EST = timezone('US/Eastern')

class Slash(commands.Cog, name="Slash Commands"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
	@cog_ext.cog_slash(name="color",
			description="Returns with the color of a member's top role.",
			options=[
			   create_option(
					name="member",
					description="The member to get the color of.",
					option_type=6,
					required=False,
			   )
			])
	async def _color(self, ctx: SlashContext, member: discord.Member):
		footers = ["Powered by discord.py", "nobody even reads these", "Created by Goose#4825", "Fuyu Bot 2021", "fuyu is just winter in japanese", "冬のボット2021", "Fuyu v0.1", "冬バージョン0.1"]
		random.shuffle(footers)
		colorEmbed = discord.Embed(
			title=f"{member.name}'s Top Color",
			timestamp=datetime.now(EST),
			color=member.color
		)
		hexColor = str(member.color).replace("#", "")
		rgbColor = colorFuncs.hex_to_rgb(hexColor)
		r, g, b = rgbColor[0], rgbColor[1], rgbColor[2]
		hlsColor = colorsys.rgb_to_hls(r/255, g/255, b/255)
		yiqColor = colorsys.rgb_to_yiq(r/255, g/255, b/255)
		hsvColor = colorsys.rgb_to_hsv(r/255, g/255, b/255)
		yccColor = colorFuncs.rgb_to_ycc(r, g, b)
		cmykColor = colorFuncs.rgb_to_cmyk(r, g, b)
		labColor = colorFuncs.rgb_to_lab(r, g, b)
		xyzColor = colorFuncs.rgb_to_xyz(r, g, b)
		luvColor = colorFuncs.rgb_to_luv(r, g, b)
		colorEmbed.add_field(name="RGB", value=f"{r}, {g}, {b}")
		colorEmbed.add_field(name="Hexadecimal", value=str(member.color))
		colorEmbed.add_field(name="Decimal", value=colorFuncs.hex_to_decimal(hexColor))
		colorEmbed.add_field(name="CMYK", value=f"{cmykColor[0]}%, {cmykColor[1]}%, {cmykColor[2]}%, {cmykColor[3]}%")
		colorEmbed.add_field(name="HSV", value=f"{round(hsvColor[0], 2)}°, {round(hsvColor[1], 2)}%, {round(hsvColor[2], 2)}%")
		colorEmbed.add_field(name="HLS", value=f"{round(hlsColor[0], 2)}°, {round(hlsColor[1], 2)}%, {round(hlsColor[2], 2)}%")
		colorEmbed.add_field(name="YIQ", value=f"{round(yiqColor[0], 2)}, {round(yiqColor[1], 2)}, {round(yiqColor[2], 2)}")
		colorEmbed.add_field(name="XYZ", value=f"{round(xyzColor[0]*100)}, {round(xyzColor[1]*100)}, {round(xyzColor[2]*100)}")
		colorEmbed.add_field(name="YCbCr", value=f"{yccColor[0]}, {yccColor[1]}, {yccColor[2]}")
		colorEmbed.add_field(name="L\*a\*b*", value=f"{round(labColor[0])}, {round(labColor[1])}, {round(labColor[2])}")
		colorEmbed.add_field(name="Luv", value=f"{round(luvColor[0])}, {round(luvColor[1])}, {round(luvColor[2])}")
		colorEmbed.set_image(url=f"https://singlecolorimage.com/get/{str(member.color).replace('#', '')}/450x250")
		colorEmbed.set_footer(text=random.choice(footers))
		await ctx.send(embed=colorEmbed)
	@cog_ext.cog_slash(name="viewcolor",
			description="Returns with an embed with the designated color.",
			options=[
			   create_option(
					name="color",
					description="A hexadecimal string to view colors of (#xxxxxx; 0-9 a-F)",
					option_type=3,
					required=True,
			   )
			])
	async def _viewcolor(self, ctx: SlashContext, color:str):
		footers = ["Powered by discord.py", "nobody even reads these", "Created by Goose#4825", "Fuyu Bot 2021", "fuyu is just winter in japanese", "冬のボット2021", "Fuyu v0.1", "冬バージョン0.1"]
		random.shuffle(footers)
		colorEmbed = discord.Embed(
			title=f"{color}",
			timestamp=datetime.now(EST),
			color=int(color.replace("#", ""), 16)
		)
		hexColor = str(color).replace("#", "")
		rgbColor = colorFuncs.hex_to_rgb(hexColor)
		r, g, b = rgbColor[0], rgbColor[1], rgbColor[2]
		hlsColor = colorsys.rgb_to_hls(r/255, g/255, b/255)
		yiqColor = colorsys.rgb_to_yiq(r/255, g/255, b/255)
		hsvColor = colorsys.rgb_to_hsv(r/255, g/255, b/255)
		yccColor = colorFuncs.rgb_to_ycc(r, g, b)
		cmykColor = colorFuncs.rgb_to_cmyk(r, g, b)
		labColor = colorFuncs.rgb_to_lab(r, g, b)
		xyzColor = colorFuncs.rgb_to_xyz(r, g, b)
		luvColor = colorFuncs.rgb_to_luv(r, g, b)
		colorEmbed.add_field(name="RGB", value=f"{r}, {g}, {b}")
		colorEmbed.add_field(name="Hexadecimal", value=str(color))
		colorEmbed.add_field(name="Decimal", value=colorFuncs.hex_to_decimal(hexColor))
		colorEmbed.add_field(name="CMYK", value=f"{cmykColor[0]}%, {cmykColor[1]}%, {cmykColor[2]}%, {cmykColor[3]}%")
		colorEmbed.add_field(name="HSV", value=f"{round(hsvColor[0], 2)}°, {round(hsvColor[1], 2)}%, {round(hsvColor[2], 2)}%")
		colorEmbed.add_field(name="HLS", value=f"{round(hlsColor[0], 2)}°, {round(hlsColor[1], 2)}%, {round(hlsColor[2], 2)}%")
		colorEmbed.add_field(name="YIQ", value=f"{round(yiqColor[0], 2)}, {round(yiqColor[1], 2)}, {round(yiqColor[2], 2)}")
		colorEmbed.add_field(name="XYZ", value=f"{round(xyzColor[0]*100)}, {round(xyzColor[1]*100)}, {round(xyzColor[2]*100)}")
		colorEmbed.add_field(name="YCbCr", value=f"{yccColor[0]}, {yccColor[1]}, {yccColor[2]}")
		colorEmbed.add_field(name="L\*a\*b*", value=f"{round(labColor[0])}, {round(labColor[1])}, {round(labColor[2])}")
		colorEmbed.add_field(name="Luv", value=f"{round(luvColor[0])}, {round(luvColor[1])}, {round(luvColor[2])}")
		colorEmbed.set_image(url=f"https://singlecolorimage.com/get/{hexColor}/450x250")
		colorEmbed.set_footer(text=random.choice(footers))
		await ctx.send(embed=colorEmbed)
	@cog_ext.cog_slash(
		name="activites",
		description="Select an activity to play in your voice channel",
		#guild_ids=[847500838825754646],
		options=[
			create_option(
				name="activity",
				description="the activity to start",
				option_type=3,
				required=False,
				choices=[
					create_choice(
						name="Betrayal.io",
						value="betrayal"
					),
					create_choice(
						name="YouTube",
						value="youtube"
					),
					create_choice(
						name="Poker",
						value="poker"
					),
					create_choice(
						name="Fishington.io",
						value="fishington"
					),
					create_choice(
						name="Chess in the Park",
						value="chess"
					),
					create_choice(
						name="Doodle Crew",
						value="doodle"
					),
					create_choice(
						name="Word Snacks",
						value="word"
					),
					create_choice(
						name="Letter Tile",
						value="letter"
					),
					create_choice(
						name="Spell Cast",
						value="spell"
					),
					create_choice(
						name="Checkers in the Park",
						value="checkers"
					),
					create_choice(
						name="Sketch Heads.",
						value="sketch"
					)
				]
			)
		],
	)
	async def _start_activity(self, ctx: SlashContext, activity):
		activities = {
			"youtube": 755600276941176913,
			"betrayal": 773336526917861400,
			"fishington": 814288819477020702,
			"poker": 755827207812677713,
			"chess": 832012586023256104,
			"doodle":878067389634314250,
			"word":879863976006127627,
			"letter":879863686565621790,
			"spell":852509694341283871,
			"checkers":832013003968348200,
			"sketch":902271654783242291
		}
		voice = ctx.author.voice
		if not voice:
			return await ctx.send(
				content="You have to be in a voice channel to use this command."
			)
		r = Route(
			"POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id
		)
		payload = {
			"max_age": 60,
			"target_type": 2,
			"target_application_id": activities[activity],
		}

		try:
			code = (await self.bot.http.request(r, json=payload))["code"]
		except discord.Forbidden:
			return await ctx.send(
				content="I Need the `Create Invite` permission.", type=7
			)
		await ctx.send(
			embed=discord.Embed(
				description=f"[{activity.capitalize()} Activity Invite](https://discord.gg/{code})\nLink expires in 1 minute",
				color=3447003
			)
		)
def setup(bot:commands.Bot):
	bot.add_cog(Slash(bot))
