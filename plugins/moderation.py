import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import checks
from utils import locale as loc
from importlib import import_module

config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
mn = "plugins.moderation"


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.permission(discord.Permissions.ban_members)
    @commands.guild_only()
    @commands.command(help="ban_help", brief="ban_brief")
    async def ban(self, ctx, user: discord.User, *, reason=None):
        if user == ctx.me or user == ctx.author or user == ctx.guild.owner:
            await ctx.send(loc.get(ctx, db, mn, "target_error"))
            return
        if reason:
            reason = loc.get(ctx, db, mn, "ban_reason").format(ctx.author.name, reason)
        else:
            reason = loc.get(ctx, db, mn, "ban_reason_empty").format(ctx.author.name)
        member = ctx.guild.get_member(user.id)
        if member is None:
            await ctx.send(loc.get(ctx, db, mn, "user_notfound"))
            return
        try:
            await member.send(loc.get(ctx, db, mn, "ban_dm").format(ctx.guild.name, reason))
        except (discord.Forbidden, discord.errors.HTTPException):
            await ctx.send(loc.get(ctx, db, mn, "dm_error"))
        await member.ban(reason=reason)
        await ctx.send(loc.get(ctx, db, mn, "ban_success").format(member.name, reason))

    @checks.permission(discord.Permissions.kick_members)
    @commands.guild_only()
    @commands.command(help="kick_help", brief="kick_brief")
    async def kick(self, ctx, user: discord.User, *, reason=None):
        if user == ctx.me or user == ctx.author or user == ctx.guild.owner:
            await ctx.send(loc.get(ctx, db, mn, "target_error"))
            return
        if reason:
            reason = loc.get(ctx, db, mn, "kick_reason").format(ctx.author.name, reason)
        else:
            reason = loc.get(ctx, db, mn, "kick_reason_empty").format(ctx.author.name)
        member = ctx.guild.get_member(user.id)
        if member is None:
            await ctx.send(loc.get(ctx, db, mn, "user_notfound"))
            return
        try:
            await member.send(loc.get(ctx, db, mn, "kick_dm").format(ctx.guild.name, reason))
        except (discord.Forbidden, discord.errors.HTTPException):
            await ctx.send(loc.get(ctx, db, mn, "dm_error"))
        await member.kick(reason=reason)
        await ctx.send(loc.get(ctx, db, mn, "kick_success").format(member.name, reason))

    @checks.permission(discord.Permissions.kick_members)
    @commands.guild_only()
    @commands.command(help="idban_help", brief="idban_brief")
    async def idban(self, ctx, user: int, *, reason=None):
        try:
            member = ctx.guild.get_member(user)
        except discord.NotFound:
            member = None
        if member:
            await ctx.send(loc.get(ctx, db, mn, "idban_is_member").format(member.name, ctx.prefix, member.id))
            return
        if reason:
            reason = loc.get(ctx, db, mn, "ban_reason").format(ctx.author.name, reason)
        else:
            reason = loc.get(ctx, db, mn, "ban_reason_empty").format(ctx.author.name)
        try:
            await self.bot.http.ban(user, ctx.guild.id, reason=reason)
        except (discord.Forbidden, discord.errors.HTTPException):
            await ctx.send(loc.get(ctx, db, mn, "user_notfound"))
        else:
            for x in await ctx.guild.bans():
                if x.user.id == user:
                    member = x.user
            await ctx.send(loc.get(ctx, db, mn, "ban_success").format(member.name, reason))

    @checks.permission(discord.Permissions.ban_members)
    @commands.guild_only()
    @commands.command(help="unban_help", brief="unban_brief")
    async def unban(self, ctx, user):
        for x in await ctx.guild.bans():
            if x.user.name == user:
                await ctx.guild.unban(x.user)
                await ctx.send(loc.get(ctx, db, mn, "unban_success").format(x.user.name))
                return
            try:
                user = int(user)
            except ValueError:
                await ctx.send(loc.get(ctx, db, mn, "user_notfound"))
                return
            if x.user.id == user:
                await ctx.guild.unban(x.user)
                await ctx.send(loc.get(ctx, db, mn, "unban_success").format(x.user.name))
                return
        await ctx.send(loc.get(ctx, db, mn, "user_notfound"))


def setup(bot):
    plugin = Moderation(bot)
    bot.add_cog(plugin)
