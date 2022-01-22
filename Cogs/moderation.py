import time
from datetime import datetime

import discord
from discord.ext import commands
from pytz import timezone

tz = timezone('US/Eastern')

class ModerationCog(commands.Cog, name="Mod Commands"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
		
	@commands.command(name = "kick",
					usage="{user} {reason}",
					description = "Kicks a member from the server")
	@commands.cooldown(1, 2, commands.BucketType.member)
	@commands.has_permissions(administrator=True, kick_members=True)
	async def kick(self, ctx, user:discord.Member, *, reason:str):
		await user.kick(reason=reason)
		currenttime = datetime.now(tz) 
		embed = discord.Embed(description=f"**{user}** has been kicked from **{ctx.message.guild.name}**. Reason: **{reason}**.", color=1356771)
		#embed.timestamp=currenttime
		#embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name = "ban",
					usage="{user} {reason}",
					description = "Bans a member from the server")
	@commands.cooldown(1, 2, commands.BucketType.member)
	@commands.has_permissions(administrator=True, ban_members=True)
	async def ban(self, ctx, user:discord.Member, *, reason:str):
		await user.ban(reason=reason)
		currenttime = datetime.now(tz) 
		embed = discord.Embed(description=f"**{user}** has been banned from **{ctx.message.guild.name}**. Reason: **{reason}**.", color=1356771)
		#embed.timestamp = currenttime
		#embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name = "unban",
					usage="{user}",
					description = "Unbans a member from the server")
	@commands.cooldown(1, 2, commands.BucketType.member)
	@commands.has_permissions(administrator=True, ban_members=True)
	async def _unban(self, ctx, *, member_id: int): 
		"Unban command for admins."
		await ctx.guild.unban(discord.Object(id=member_id))
		user = await self.bot.fetch_user(member_id)
		currenttime = datetime.now(tz) 
		embed = discord.Embed(description=f"**{user}** has been unbanned from **{ctx.message.guild.name}**.", color=1356771, timestamp=currenttime)
		await ctx.send(embed=embed)

def setup(bot:commands.Bot):
	bot.add_cog(ModerationCog(bot))
