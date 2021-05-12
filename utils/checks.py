import discord
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


def permissions(**perms):
    def check(ctx):
        return server_perms(ctx, discord.Permissions(**perms))
    return commands.check(check)


def server_perms(ctx, perms):
    if bot_owner_raw(ctx):
        return True
    elif server_owner_raw(ctx):
        return True
    elif not perms:
        return False
    resolved = ctx.message.channel.permissions_for(ctx.message.author)
    return perms <= resolved
