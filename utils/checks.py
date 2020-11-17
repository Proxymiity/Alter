from discord.ext import commands
from utils.dataIO import dataIO
bot_owner_id = dataIO.load_json("data/config.json")["owner"]


def bot_owner():
    return commands.check(bot_owner_raw)


def bot_owner_raw(ctx):
    return ctx.message.author.id == bot_owner_id


def server_owner():
    return commands.check(server_owner_raw)


def server_owner_raw(ctx):
    if ctx.message.guild is None:
        return False
    guild = ctx.message.guild
    if ctx.message.author.id == guild.owner_id:
        return True
    else:
        return False


def server_perms(ctx, perms):
    if bot_owner_raw(ctx):
        return True
    elif server_owner_raw(ctx):
        return True
    elif not perms:
        return False
    channel = ctx.message.channel
    author = ctx.message.author
    resolved = channel.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.item())
    # https://gitlab.com/Proxymiity/proxybot/-/blob/master/releases/8.0.6/cogs/utils/checks.py
