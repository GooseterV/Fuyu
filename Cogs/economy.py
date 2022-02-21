
import json
import math
import os
import random
import time
from datetime import datetime

import discord
import pandas as pd
from discord.ext import commands
from pytz import timezone
from sqlalchemy import create_engine
#from dotenv import load_dotenv
#load_dotenv()
tz = timezone('US/Eastern')
DB_URL = os.getenv("DB_URL")
FUYUCOIN = "<:fuyucoin:945363163115815032>"
class Errors:
	class InvalidBalanceError:
		def __init__(self, msg):
			self.msg = msg
	class InvalidUserError:
		def __init__(self, id, msg):
			self.msg = msg
			self.userid = id
	class UserRegisteredError:
		def __init__(self, id, msg):
			self.msg = msg
			self.userid = id


def refreshConn(url):
	return create_engine(url, echo = False)

def initializeDB(conn):
	ud = pd.DataFrame([{
			"wallet":0,
			"bank":0,
			"id":0,
			"items":[],
			"lvl":0,
			"xp":0
		}])
	ud.to_sql("users", conn, if_exists="replace")
	return 1

def registerUser(id, conn):
	if not userRegistered(id, conn):
		ud = pd.DataFrame([{
			"wallet":0,
			"bank":0,
			"id":id,
			"items":[],
			"lvl":0,
			"xp":0
		}])
		ud.to_sql("users", conn, if_exists="append")
		return 1
	elif userRegistered(id, conn):
		return Errors.UserRegisteredError(id, "User is already registered!")


def getUsers(conn):
	return conn.execute("SELECT * FROM users").mappings().all()


#c = refreshConn(DB_URL)
#print (
	#getUsers(
		#c
	#)
#)

def getUserById(id, conn):
	results = conn.execute(f"SELECT * FROM users WHERE id={id};").mappings().all()
	if len(results) < 1:
		return Errors.InvalidUserError(id, "User not found. Make sure user is registered in db.")
	elif len(results) > 0:
		return results[0]

def userRegistered(id, conn):
	return not isinstance(getUserById(id, conn), Errors.InvalidUserError)

def updateUser(id, newdata, conn):
	users = getUsers(conn)
	users = [newdata if user["id"] == id else user for user in users]
	pd.DataFrame(users).to_sql("users", conn, if_exists="replace")
	return 1

def withdrawMoney(amount, id, conn):
	if amount > getUserById(id)["bank"]:
		return Errors.InvalidBalanceError(f"Bank amount less than withdrawl amount.")
	elif amount <= getUserById(id)["bank"]:
		user = getUserById(id)
		updateUser(id, {
			"wallet":user["wallet"]+amount,
			"bank":user["bank"]-amount,
			"id":id,
			"items":[],
			"lvl":0,
			"xp":0
		}, conn)
		return 1

def depositMoney(amount, id, conn):
	if amount > getUserById(id, conn)["wallet"]:
		return Errors.InvalidBalanceError(f"Wallet amount less than deposit amount.")
	elif amount <= getUserById(id, conn)["wallet"]:
		user = getUserById(id, conn)
		updateUser(id, {
			"wallet":user["wallet"]-amount,
			"bank":user["bank"]+amount,
			"id":id,
			"items":[],
			"lvl":0,
			"xp":0
		}, conn)
		return 1

def addMoney(amount, id, conn):
	user = getUserById(id, conn)
	updateUser(id, {
		"wallet":user["wallet"]+amount,
		"bank":user["bank"],
		"id":id,
		"items":[],
		"lvl":0,
		"xp":0
	}, conn)
	return 1

class EconomyCog(commands.Cog, name="Economy Commands"):
	"Commands that interact with the economy of the bot."
	def __init__(self, bot:commands.bot):
		self.bot = bot



	@commands.command(name = "register",
					usage="",
					description = "Registers a user in the economy section of the bot",
					aliases = [])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def register(self, ctx):
		conn = refreshConn(DB_URL)
		if userRegistered(ctx.author.id, conn):
			e = discord.Embed(description="You are already registered!", color=1356771)
			await ctx.send(embed=e)
		elif not userRegistered(ctx.author.id, conn):
			registerUser(ctx.author.id, conn)
			e = discord.Embed(description="Successfully registered into the economy.", color=1356771)
			await ctx.send(embed=e)
		conn.dispose()

	@commands.command(name = "initialize",
					usage="",
					description = "Owner only (initializes the db)",
					aliases = [])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def initialize(self, ctx):
		conn = refreshConn(DB_URL)
		if ctx.author.id == 657993676257099788:
			initializeDB(conn)
			await ctx.send("Initialized DB!")
		elif ctx.author.id != 657993676257099788:
			await ctx.send("You cannot run this command!")
		conn.dispose()

	@commands.command(name = "balance",
					usage="<member:optional>",
					description = "check the balance of your account.",
					aliases = ["bal"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def balance(self, ctx, member:discord.Member=None):
		conn = refreshConn(DB_URL)
		if not member and not userRegistered(ctx.author.id, conn):
			await ctx.send(embed=discord.Embed(description=f"You are not registered!"), color=1356771)
			return 0

		if not member:
			inf = getUserById(ctx.author.id, conn)
			e = discord.Embed(title=f"Your Balance", description=f"**Wallet:** {inf['wallet']} {FUYUCOIN}\n**Bank:** {inf['bank']} {FUYUCOIN}\n**Total:** {inf['bank'] + inf['wallet']} {FUYUCOIN}", color=1356771)
			await ctx.send(embed=e)
		elif member:
			if userRegistered(member.id, conn):
				inf = getUserById(member.id, conn)
				e = discord.Embed(title=f"{member.name}'s Balance", description=f"**Wallet:** {inf['wallet']} {FUYUCOIN}\n**Bank:** {inf['bank']} {FUYUCOIN}\n**Total:** {inf['bank'] + inf['wallet']} {FUYUCOIN}", color=1356771)
				await ctx.send(embed=e)
			elif not userRegistered(member.id, conn):
				await ctx.send(embed=discord.Embed(description=f"{member.name} is not registered!", color=1356771))
				return 0
		conn.dispose()

	@commands.command(name = "withdraw",
					usage="<amount:INT>",
					description = "Withdraw money from your bank account.",
					aliases = ["with", "wd"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def withdraw(self, ctx, amount:int):
		conn = refreshConn(DB_URL)
		if userRegistered(ctx.author.id, conn):
			withdrawMoney(amount, ctx.author.id, conn)
			await ctx.send(embed=discord.Embed(description=f"Withdrawn {amount} {FUYUCOIN} from your bank.", color=1356771))
		elif not userRegistered(ctx.author.id, conn):
			await ctx.send(embed=discord.Embed(description=f"You are not registered!", color=1356771))
		else:
			print("test")
		conn.dispose()

	@commands.command(name = "deposit",
					usage="<amount:INT>",
					description = "Deposit money from your wallet to your bank account.",
					aliases = ["dep", "dp"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def deposit(self, ctx, amount:int):
		conn = refreshConn(DB_URL)
		if userRegistered(ctx.author.id, conn):
			depositMoney(amount, ctx.author.id, conn)
			await ctx.send(embed=discord.Embed(description=f"Deposited {amount} {FUYUCOIN} to your bank.", color=1356771))
		elif not userRegistered(ctx.author.id, conn):
			await ctx.send(embed=discord.Embed(description=f"You are not registered!", color=1356771))
		conn.dispose()

	@commands.command(name = "addmoney",
					usage="<amount:INT> <member:discord.Member>",
					description = "Add money to someone's account (owner only)",
					aliases = ["addbalance", "givemoney", "aw"])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def withdraw(self, ctx, amount:int, member:discord.Member):
		conn = refreshConn(DB_URL)
		if ctx.author.id == 657993676257099788:
			if not userRegistered(member.id, conn):
				await ctx.send(embed=discord.Embed(description=f"{member.name} is not registered!", color=1356771))
			elif userRegistered(member.id, conn):
				addMoney(amount, member.id, conn)
				await ctx.send(embed=discord.Embed(description=f"Added {amount} {FUYUCOIN} to {member.name}'s wallet.", color=1356771))
		elif not ctx.author.id == 657993676257099788:
			await ctx.send("You cannot run this command!")
		conn.dispose()

def setup(bot:commands.Bot):
	bot.add_cog(EconomyCog(bot))
