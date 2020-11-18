import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import locale
from utils import help

config = dataIO.load_json("data/config.json")
token = config["token"]
prefix = config["prefix"]
loc = locale.load(config["locale"], "alter")
bot = commands.Bot(prefix)


@bot.event
async def on_ready():
    print(loc["logged_in_as"].format(bot.user))
    bot.remove_command("help")
    for p in config["loadPlugins"]:
        print(loc["loading_ext"].format(p))
        bot.load_extension(p)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.invoked_subcommand:
            await help.send_cmd_help(ctx, ctx.invoked_subcommand, error=True)
        else:
            await help.send_cmd_help(ctx, ctx.command, error=True)
    elif isinstance(error, commands.BadArgument):
        if ctx.invoked_subcommand:
            await help.send_cmd_help(ctx, ctx.invoked_subcommand, error=True)
        else:
            await help.send_cmd_help(ctx, ctx.command, error=True)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(loc["err_disabled"])
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.Forbidden):
            await ctx.send(loc["err_missing_perm"])
        elif "Missing Permission" in "{}".format(error):
            await ctx.send(loc["err_missing_perm"])
        elif "FORBIDDEN" in "{}".format(error):
            await ctx.send(loc["err_missing_perm"])
        else:
            await ctx.send(loc["err_exec"].format(error))
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(loc["err_pm"])
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(loc["err_cd"].format(error.retry_after))
    else:
        print("Uncaught exception {}".format(error))
        dataIO.save_json("error.json", [error])
        await ctx.send(loc["err_uncaught"])


print(loc["logging_in"].format(token[0:5]))
bot.run(token)
