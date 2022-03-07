import math
import time
from datetime import datetime

import discord
from discord.ext import commands
from pytz import timezone

tz = timezone('US/Eastern')

def is_square(n):
	return math.sqrt(n) ** math.sqrt(n) == n
def factors(n):
	return list({f for i in range(1, int(n**0.5)+1) if n % i == 0 for f in [i, n//i]})
def is_prime(n):
	return len(set(factors(n))) == 2
def is_even(n):
	return n % 2 == 0
class MathCog(commands.Cog, name="Math Commands"):
	def __init__(self, bot:commands.bot):
		self.bot = bot

	@commands.command(name = "sqrt",
					usage="{number}",
					description = "Finds the square root of a number.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def sqrt(self, ctx, num:float):
		""" Returns with the square root of a number. """
		await ctx.send(f"The square root of `{num}` is **{math.sqrt(num)}**")

	@commands.command(name = "issquare",
					usage="{number}",
					description = "Finds out if the number is a perfect square.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def issquare(self, ctx, num:float):
		""" Returns with true/false depending if the number is a perfect square. """
		if is_square(num):
			await ctx.send(f"`{num}` is a perfect square.")
		elif not is_square(num):
			await ctx.send(f"`{num}` is not a perfect square.")

	@commands.command(name = "factorial",
					usage="{number}",
					description = "The product of each number from 1 to n.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def factorial(self, ctx, num:float):
		""" Returns with the factorial of the number ( product of every number from one to n )"""
		await ctx.send(f"Your product is **{math.factorial(num)}**")

	@commands.command(name = "isprime",
					usage="{number}",
					description = "Finds out if the number is a prime number.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def isprime(self, ctx, num:float):
		""" Checks whether a number is prime or not. (has no other factors but 1, and itself)"""
		if is_prime(num):
			await ctx.send(f"`{num}` is prime.")
		elif not is_prime(num):
			await ctx.send(f"`{num}` is not prime.")
			

def setup(bot:commands.Bot):
	bot.add_cog(MathCog(bot))
