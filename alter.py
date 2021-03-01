import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import tools; tools.check_defaults()
from utils import locale as loc
from utils import help
from datetime import datetime
from importlib import import_module

config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
mn = "alter"
dl = db.read("settings", 0, "locale")
token = config["token"]
prefix = db.read("settings", 0, "prefix")
bot = commands.Bot(prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(loc.load(dl, mn, "logged_in_as").format(bot.user))
    bot.remove_command("help")
    for p in config["loadPlugins"]:
        print(loc.load(dl, mn, "loading_ext").format(p))
        bot.load_extension(p)
    await bot.change_presence(status=tools.get_status(db.read("settings", 0, "status")),
                              activity=tools.get_presence(db.read("settings", 0, "presence_type"),
                                                          db.read("settings", 0, "presence_value")))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send(loc.load(dl, mn, "err_pm"))
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.send(loc.get(ctx, db, mn, "err_pm_only"))
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(loc.get(ctx, db, mn, "err_disabled"))
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(loc.load(dl, mn, "err_nsfw"))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(loc.get(ctx, db, mn, "err_cd").format(error.retry_after))
    elif isinstance(error, commands.MissingRequiredArgument):
        await help.send_cmd_help(ctx, ctx.command, error=True)
    elif isinstance(error, commands.BadArgument):
        await help.send_cmd_help(ctx, ctx.command, error=True)
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.Forbidden):
            await ctx.send(loc.get(ctx, db, mn, "err_missing_perm"))
        else:
            await ctx.send(loc.get(ctx, db, mn, "err_exec").format(error))
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        print("Uncaught exception {}".format(error))
        dataIO.save_json("error.json", [error])
        await ctx.send(loc.get(ctx, db, mn, "err_uncaught"))


db.write("temp", 1, "start_time", str(datetime.now()))
print(loc.load(dl, mn, "logging_in").format(token[0:5]))
bot.run(token)
