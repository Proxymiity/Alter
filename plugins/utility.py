import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import checks, help
from utils import locale as loc
from datetime import datetime
from importlib import import_module

config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
mn = "plugins.utility"


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(help="serverinfo_help", brief="serverinfo_brief", aliases=["server"])
    async def serverinfo(self, ctx):
        g = ctx.guild
        online = len([m.status for m in g.members if m.status != discord.Status.offline])
        delta = datetime.now() - g.created_at
        embed = discord.Embed(color=discord.Color.teal(), title=g.name)
        embed.set_footer(text=loc.get(ctx, db, mn, "id").format(g.id))
        if g.icon_url:
            embed.set_thumbnail(url=g.icon_url)
        embed.add_field(name=loc.get(ctx, db, mn, "general"), value=loc.get(ctx, db, mn, "srv_general").format(
            g.owner, online, g.member_count, g.premium_subscription_count, len(g.emojis), g.emoji_limit, len(g.roles)
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "channel"), value=loc.get(ctx, db, mn, "srv_channel").format(
            len(g.text_channels), len(g.voice_channels), len(g.categories), str(g.region)
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "history"), value=loc.get(ctx, db, mn, "srv_history").format(
            g.created_at.strftime(loc.get(ctx, db, "region", "date")), int(delta.days)
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "misc"), value=loc.get(ctx, db, mn, "srv_misc").format(
            int(g.filesize_limit/1024/1024), int(g.bitrate_limit/1000),
            loc.get(ctx, db, mn, "ct_filter")[str(g.explicit_content_filter)],
            loc.get(ctx, db, mn, "vr_level")[str(g.verification_level)]
        ))
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(help="userinfo_help", brief="userinfo_brief", aliases=["user"])
    async def userinfo(self, ctx, user: discord.User = None):
        if not user:
            u = ctx.author
        else:
            u = ctx.guild.get_member(user.id)
            if u is None:
                await ctx.send(loc.get(ctx, db, mn, "user_notfound"))
                return
        roles = u.roles
        roles.remove(ctx.guild.default_role)
        delta_c = datetime.now() - u.created_at
        delta_j = datetime.now() - u.joined_at
        embed = discord.Embed(color=u.color, title=u.name)
        embed.set_footer(text=loc.get(ctx, db, mn, "id").format(u.id))
        embed.set_thumbnail(url=u.avatar_url)
        embed.add_field(name=loc.get(ctx, db, mn, "general"), value=loc.get(ctx, db, mn, "usr_general").format(
            u.name, u.discriminator, u.display_name, loc.get(ctx, db, mn, "status")[u.raw_status]
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "roles"), value=loc.get(ctx, db, mn, "usr_roles").format(
            len(roles), ", ".join([r.mention for r in roles]) or loc.get(ctx, db, mn, "empty")
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "history"), value=loc.get(ctx, db, mn, "usr_history").format(
            u.created_at.strftime(loc.get(ctx, db, "region", "date")), int(delta_c.days),
            u.joined_at.strftime(loc.get(ctx, db, "region", "date")), int(delta_j.days)
        ))
        embed.add_field(name=loc.get(ctx, db, mn, "misc"), value=loc.get(ctx, db, mn, "usr_misc").format(
            ", ".join([loc.get(ctx, db, mn, "flags")[p[0]] for p in u.public_flags if p[1] is True]) or
            loc.get(ctx, db, mn, "empty")
        ))
        await ctx.send(embed=embed)


def setup(bot):
    plugin = Utility(bot)
    bot.add_cog(plugin)
