import math
import random
import time
from datetime import datetime

import discord
from discord.ext import commands
from pytz import timezone

tz = timezone('US/Eastern')


class FunCog(commands.Cog, name="Fun Commands"):
	"Fun things to play around with."
	def __init__(self, bot:commands.bot):
		self.bot = bot

	@commands.command(name = "waifurate",
					usage="<optional:mention>",
					description = "Finds what percent out of 100 you are waifu.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def waifurate(self, ctx, user: discord.Member = None):
		"😳 Finds your waifu rate out of 100."
		result = str(random.randint(1,100))
		if result == 69:
			emoji = ":ok_hand:"
		else:
			emoji = ":flushed:"
		if user:
			message100 = str(emoji) + " <@!" + str(user.id) + "> Is " + str(result) + "% waifu"
			embed100 = discord.Embed(title="Waifu-inator 2000", description=str(message100))
			embed100.set_author(name=user, icon_url=user.avatar)
			embed100.timestamp = ctx.message.created_at
			embed100.color = 1356771
			await ctx.send(embed=embed100)
		else:
			message10 = str(emoji) + " You are " + str(result) + "% waifu"
			embed101 = discord.Embed(title="Waifu-inator 2000", description=str(message10))
			embed101.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar)
			embed101.timestamp = ctx.message.created_at
			embed101.color = 1356771
			await ctx.send(embed=embed101)


	@commands.command(name = "gamerrate",
					usage="<optional:mention>",
					description = "Finds what percent out of 100 you are gamer.",
					aliases = [])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def gamerrate(self, ctx, user: discord.Member = None):
		"🎮 Finds how much of a gamer you are out of 100."
		result = str(random.randint(1,100))
		if user:
			message0 = ":video_game: <@!" + str(user.id) + "> Is " + str(result) + "% gamer"
			embed1 = discord.Embed(title="Gamer-inator 2000", description=str(message0))
			embed1.set_author(name=user, icon_url=user.avatar)
			embed1.timestamp = ctx.message.created_at
			embed1.color = 1356771
			await ctx.send(embed=embed1)
		else:
			message01 = ":video_game: " + "You are " + str(result) + "% gamer"
			embed = discord.Embed(title="Gamer-inator 2000", description=str(message01))
			embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar)
			embed.timestamp = ctx.message.created_at
			embed.color = 1356771
			await ctx.send(embed=embed)
			

	@commands.command(name = "idiotrate",
					usage="<optional:mention>",
					description = "Finds what percent out of 100 you are idiot.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def idiotrate(self, ctx, user: discord.Member = None):
		"Finds how stupid you are out of 100."
		result = str(random.randint(1,100))
		if user:
			message12 = "<:dummie:837842451505872946> <@!" + str(user.id) + "> Is " + str(result) + "% idiot"
			embed1 = discord.Embed(title="Stupid-inator 2000", description=str(message12))
			embed1.set_author(name=user, icon_url=user.avatar)
			embed1.timestamp = ctx.message.created_at
			embed1.color = 1356771
			await ctx.send(embed=embed1)
		else:
			message2 = "<:dummie:837842451505872946> " + "You are " + str(result) + "% idiot"
			embed013 = discord.Embed(title="Stupid-inator 2000", description=str(message2))
			embed013.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar)
			embed013.timestamp = ctx.message.created_at
			embed013.color = 1356771
			await ctx.send(embed=embed013)


	@commands.command(name = "coolrate",
					usage="<optional:mention>",
					description = "Finds what percent out of 100 you are cool.",
					aliases = ["howcool"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def coolrate(self, ctx, user: discord.Member = None):
		"😎 Finds how cool you are out of 100."
		result = str(random.randint(1,100))
		if user:
			message0 = ":sunglasses: <@!" + str(user.id) + "> Is " + str(result) + "% cool"
			embed1 = discord.Embed(title="Cool-inator 2000", description=str(message0))
			embed1.set_author(name=user, icon_url=user.avatar)
			embed1.timestamp = ctx.message.created_at
			embed1.color = 1356771
			await ctx.send(embed=embed1)
		else:
			message01 = ":sunglasses: " + "You are " + str(result) + "% cool"
			embed = discord.Embed(title="Cool-inator 2000", description=str(message01))
			embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar)
			embed.timestamp = ctx.message.created_at
			embed.color = 1356771
			await ctx.send(embed=embed)


def setup(bot:commands.Bot):
	bot.add_cog(FunCog(bot))
