import discord
from discord import app_commands
from discord.ext import commands
import os
import typing
from typing import *


bot = commands.Bot(command_prefix = "L!", intents = discord.Intents.all())
Intents = discord.Intents.all

@bot.event
async def on_ready():
	await bot.tree.sync()
	print("RedY")

@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.tree.command(name="say_hi",description = "say hi")
async def say_hi(interaction : discord.Interaction):
    await interaction.response.send_message("Hi")

bot.run("MTEzMzM4MDc0NzA4NDk2MzkxMQ.G0MuDC.6ekGU3ptPg446otQ9LGCYLaPlWgQPREVXM7j8Q")