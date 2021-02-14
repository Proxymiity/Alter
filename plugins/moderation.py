import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import locale, checks

config = dataIO.load_json("data/config.json")
loc = locale.load(config["locale"], "plugins.moderation")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.permission(discord.Permissions.ban_members)
    @commands.command(help="ban_help", brief="ban_brief")
    async def ban(self, ctx, user: discord.User, *, reason=None):
        if user == ctx.me or user == ctx.author or user == ctx.guild.owner:
            await ctx.send(loc["target_error"])
            return
        if reason:
            reason = loc["ban_reason"].format(ctx.author.name, reason)
        else:
            reason = loc["ban_reason_empty"].format(ctx.author.name)
        member = ctx.guild.get_member(user.id)
        try:
            await member.send("")  # todo: https://github.com/Proxymiity/Alter/projects/2#card-54896806
        except discord.Forbidden:
            pass
        await member.ban(reason=reason)
        await ctx.send(loc["ban_success"].format(member.name, reason))


def setup(bot):
    plugin = Moderation(bot)
    bot.add_cog(plugin)
