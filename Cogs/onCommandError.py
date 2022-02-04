import difflib
import time

import discord
from discord.ext import commands
from discord.ext.commands import (CheckFailure, CommandNotFound,
								  MissingPermissions, MissingRequiredArgument,
								  NotOwner)


class OnCommandErrorCog(commands.Cog, name="on command error"):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
		if isinstance(error, commands.CommandOnCooldown):
			day = round(error.retry_after/86400)
			hour = round(error.retry_after/3600)
			minute = round(error.retry_after/60)
			if day > 0:
				await ctx.send(f"This command has a cooldown. Please wait `{str(day)}` day(s)")
			elif hour > 0:
				await ctx.send(f"This command has a cooldown. Please wait `{str(hour)}` hour(s)")
			elif minute > 0:
				await ctx.send(f"This command has a cooldown. Please wait `{str(minute)}` day(minute)")
			else:
				await ctx.send(f"This command has a cooldown. Please wait `{error.retry_after:.2f}` second(s)")
		elif isinstance(error, CommandNotFound):
			cmds = [(i, v)[0] for i, v in self.bot.all_commands.items()]
			ccmd = difflib.get_close_matches(f"{ctx.invoked_with}", cmds, n=1)[0]
			await ctx.send(f"Command `~{ctx.invoked_with}` does not exist. Did you mean **~{ccmd}**?")
			return
		elif isinstance(error, MissingPermissions):
			await ctx.send("You are missing the required permissions to use this command!");print(error)
		elif isinstance(error, CheckFailure):
			await ctx.send(error)
		elif isinstance(error, NotOwner):
			await ctx.send("You must be the owner to use this command!")
		elif isinstance(error, MissingRequiredArgument):
			#print(error)
			await ctx.send(f"**{str(error)[0:-40].capitalize()}** is a required argument that is missing.")
		else:
			print(error) 

def setup(bot):
	bot.add_cog(OnCommandErrorCog(bot))
