from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="help_help", brief="help_brief", hidden=True)
    async def hello(self, ctx):
        await ctx.send("Yes")


def setup(bot):
    plugin = Test(bot)
    bot.add_cog(plugin)


def teardown(bot):
    bot.remove_cog('Test')
