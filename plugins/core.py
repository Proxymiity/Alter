from discord.ext import commands
from utils.dataIO import dataIO
from utils import locale
from utils import help as h

config = dataIO.load_json("data/config.json")
loc = locale.load(config["locale"], "utils.help")


class Core(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False, help="help_help", brief="help_brief")
    async def help(self, ctx, query=None):
        if query:
            if query.lower() == "all":
                await h.send_help(self.bot, ctx)
                return
            for cog in self.bot.cogs:
                if query.lower() == cog.lower():
                    await h.send_plugin_help(ctx, self.bot.cogs[cog])
                    return
            if any(c.name == query.lower() for c in self.bot.commands):
                await h.send_cmd_help(ctx, self.bot.get_command(query.lower()))
                return
            await ctx.send(loc["help_not_found"])
        else:
            await h.summary(self.bot, ctx)


def setup(bot):
    plugin = Core(bot)
    bot.add_cog(plugin)


def teardown(bot):
    import logging
    logging.critical("Core module unloaded. The bot will now shutdown in order to prevent something bad to happen.")
    exit(-2)
