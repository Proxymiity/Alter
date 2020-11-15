import discord
from discord.ext import commands
from utils.dataIO import dataIO

config = dataIO.load_json("data/config.json")
token = config["token"]
prefix = config["prefix"]
bot = commands.Bot(prefix)


@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user))
    bot.remove_command("help")
    for p in config["loadPlugins"]:
        print("Loading extension " + p)
        bot.load_extension(p)


@bot.event
async def on_command_error(ctx, error):
    c = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        print("Missing required argument.")
    elif isinstance(error, commands.BadArgument):
        print("Bad argument.")
    elif isinstance(error, commands.DisabledCommand):
        print("Disabled command.")
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.Forbidden):
            print("Discord Forbidden.")
        elif "Missing Permission" in "{}".format(error):
            print("Missing Permission. {}".format(error))
        elif "FORBIDDEN" in "{}".format(error):
            print("Forbidden. {}".format(error))
        else:
            print("Execution Error. {}".format(error))
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        print("Command not usable in DM.")
    elif isinstance(error, commands.CommandOnCooldown):
        print("Command is on cooldown.")
    else:
        print("Uncaught exception. {}".format(error))


print("Logging in with token {}...".format(token[0:5]))
bot.run(token)
