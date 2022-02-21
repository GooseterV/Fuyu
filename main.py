
import datetime
import json
import os
import sys
import time

import aiohttp
import discord
import pandas as pd
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp
from pytz import timezone
from sqlalchemy import create_engine

tz = timezone('US/Eastern')
load_dotenv()
# config file
with open("Config/configuration.json", "r") as config_file:
	config = json.loads(config_file.read())
	prefix = config["prefix"]
	owner_id = config["owner_id"]
	token = os.getenv("BOT_TOKEN")


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None




bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), owner_id=owner_id, case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, delete_from_unused_guilds=True)

menu = DefaultMenu(page_left=":fuyu_arrowL:907403532238479380", page_right=":fuyu_arrowR:907403531961651241", remove=":fuyu_x:907403532305563689")
ending_note = "{ctx.author}"
bot.help_command = PrettyHelp(menu=menu, color=1356771, ending_note=ending_note, show_index=True, no_category="Undefined")
# Load cogs
to_load = ["misc", "moderation", "onCommandError", "math", "fun", "stringTools", "slashCommands", "minecraft"]
for cog in to_load:
	bot.load_extension(f"Cogs.{cog}")

@bot.command()
async def restart(ctx):
	if ctx.author.id == 657993676257099788:
		async with aiohttp.ClientSession() as hooksession:
			status_hook = Webhook.from_url(url=os.getenv("STATUS_HOOK_URL"), adapter=AsyncWebhookAdapter(hooksession))
			currenttime = datetime.datetime.now(tz) 
			if currenttime.hour > 12:
				hr = f"{currenttime.hour - 12}"
				meridiem = "PM"
			elif currenttime.hour <= 12:
				hr = currenttime.hour
				meridiem = "AM"
			else: 
				hr = currenttime.hour
				meridiem = "AM"
			frmtedtime = f"{currenttime.month}-{currenttime.day}-{currenttime.year} {hr}:{str(currenttime.minute).zfill(2)}:{str(currenttime.second).zfill(2)} {meridiem} EST"
			st = f"🔹  🔹  🔹  🔹  🔹\nStatus Update: **Restarting <a:fuyu_loading:907403532922126337>**\nTimestamp - **{frmtedtime}**\n🔹  🔹  🔹  🔹  🔹\n\u200B"
			await status_hook.send(content=st)
			hook_message = await bot.get_channel(907400968256245770).fetch_message(bot.get_channel(907400968256245770).last_message_id)
			try:
				await hook_message.publish()
			except:
				pass
			os.execv(sys.executable, ['python'] + sys.argv)
	elif ctx.author.id != 657993676257099788:
		await ctx.send("You cannot run this command!")

@bot.command()
async def shutdown(ctx):
	if ctx.author.id == 657993676257099788:
		async with aiohttp.ClientSession() as hooksession:
			status_hook = Webhook.from_url(url=os.getenv("STATUS_HOOK_URL"), adapter=AsyncWebhookAdapter(hooksession))
			currenttime = datetime.datetime.now(tz) 
			if currenttime.hour > 12:
				hr = f"{currenttime.hour - 12}"
				meridiem = "PM"
			elif currenttime.hour <= 12:
				hr = currenttime.hour
				meridiem = "AM"
			else: 
				hr = currenttime.hour
				meridiem = "AM"
			frmtedtime = f"{currenttime.month}-{currenttime.day}-{currenttime.year} {hr}:{str(currenttime.minute).zfill(2)}:{str(currenttime.second).zfill(2)} {meridiem} EST"
			st = f"🔹  🔹  🔹  🔹  🔹\nStatus Update: **Shutting Down <:fuyu_sleepy:907403532292988989>**\nTimestamp - **{frmtedtime}**\n🔹  🔹  🔹  🔹  🔹\n​​\u200B"
			await status_hook.send(content=st)
			hook_message = await bot.get_channel(907400968256245770).fetch_message(bot.get_channel(907400968256245770).last_message_id)
			try:
				await hook_message.publish()
			except:
				pass
			exit()
	elif ctx.author.id != 657993676257099788:
		await ctx.send("You cannot run this command!")


@bot.event
async def on_ready():
	os.system("cls")
	print(f"Logged in as {bot.user}")
	print(f"Discord.py v{discord.__version__}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
	async with aiohttp.ClientSession() as hooksession:
		status_hook = Webhook.from_url(url=os.getenv("STATUS_HOOK_URL"), adapter=AsyncWebhookAdapter(hooksession))
		time.sleep(3)
		currenttime = datetime.datetime.now(tz) 
		if currenttime.hour > 12:
			hr = f"{currenttime.hour - 12}"
			meridiem = "PM"
		elif currenttime.hour <= 12:
			hr = currenttime.hour
			meridiem = "AM"
		else: 
			hr = currenttime.hour
			meridiem = "AM"
		frmtedtime = f"{currenttime.month}-{currenttime.day}-{currenttime.year} {hr}:{str(currenttime.minute).zfill(2)}:{str(currenttime.second).zfill(2)} {meridiem} EST"
		st = f"🔹  🔹  🔹  🔹  🔹\nStatus Update: **Online 🔵**\nTimestamp - **{frmtedtime}**\n🔹  🔹  🔹  🔹  🔹\n\u200B"
		await status_hook.send(content=st)
		hook_message = await bot.get_channel(907400968256245770).fetch_message(bot.get_channel(907400968256245770).last_message_id)
		try:
			await hook_message.publish()
		except:
			pass

bot.run(token)
