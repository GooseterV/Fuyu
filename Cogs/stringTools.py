import itertools
import os
import random
import time
from datetime import datetime

import discord
import pronouncing
from discord.channel import VocalGuildChannel
from discord.ext import commands
from pytz import timezone


class StringCog(commands.Cog, name="String Commands"):
	def __init__(self, bot:commands.bot):
		self.bot = bot

	@commands.command(name = "rhymes",
				usage="{word:string} {amount:integer=15}",
				description = "List rhymes that rhyme with said word. Minimum of 1 and maximum of 25.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def rhymes(self, ctx, word:str, amount:int=10):
		rhymes = pronouncing.rhymes(word)
		random.shuffle(rhymes)
		if amount <= 25:
			msgText = " "
			for rhyme in rhymes[:amount-1]:
				msgText += f"{rhyme}, "
			if len(rhymes) == 0:
				msgText += f"There are no words that rhyme with {word}"
			await ctx.send(msgText)
		elif amount <= 0 or amount > 25:
			await ctx.send("**Amount** must be greater than 0 and less than 26!")

def setup(bot:commands.Bot):
	bot.add_cog(StringCog(bot))
