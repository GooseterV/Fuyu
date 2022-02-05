import math
import random
import time
from datetime import datetime
import json
import tempfile
import zipfile
import discord
import shutil
import os
from discord.ext import commands
from pytz import timezone

tz = timezone('US/Eastern')

def absoluteFilePaths(directory):
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			yield os.path.abspath(os.path.join(dirpath, f))

class MinecraftCog(commands.Cog, name="Minecraft Commands"):
	"Commands relating to minecraft"
	def __init__(self, bot:commands.bot):
		self.bot = bot

	@commands.command(name = "datapack",
					usage="{name} {description} {icon_url} <pack_version=8>",
					description = "Generates a datapack template with the parameters specified.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def datapack(self, ctx, name, description, icon_url, pack_version=8):
		packmeta = {
			"pack": {
				"pack_format": pack_version,
				"description": description,
				"name":name
			}
		}
		os.mkdir(f"temporary\\{name}")
		os.mkdir(f"temporary\\{name}\\data")
		os.mkdir(f"temporary\\{name}\\data\\{name}")
		os.mkdir(f"temporary\\{name}\\data\\{name}\\functions\\")
		packdir = f"temporary\\{name}"
		print(packdir)
		print(os.path.abspath(packdir))
		metafile = open(f"{os.path.abspath(packdir)}\\pack.mcmeta", "w")
		tickfile = open(f"{os.path.abspath(packdir)}\\data\\{name}\\functions\\tick.mcfunction", "w")
		tickfile.write("# This is where you put minecraft commands that will execute each tick.\n#Separate by new lines.")
		json.dump(packmeta, metafile, indent=4)
		#zf = zipfile.ZipFile(f"temporary/{name}.zip","w")
		#for fp in absoluteFilePaths(packdir):
			#zf.write(fp)
		shutil.make_archive(f"temporary\\{name}", 'zip', os.path.abspath(packdir))
		print(os.path.abspath(f"temporary/{name}.zip"))
		zippedPack = discord.File(os.path.abspath(f"temporary/{name}.zip"), filename=name+".zip")
		tickfile.close()
		metafile.close()
		print(os.path.abspath(packdir))
		shutil.rmtree(os.path.abspath(packdir))
		await ctx.send("Created pack template!", file=zippedPack)
		os.remove(os.path.abspath(f"temporary\\{name}.zip"))


		
		
		

def setup(bot:commands.Bot):
	bot.add_cog(MinecraftCog(bot))
