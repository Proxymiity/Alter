import discord
from discord.ext import commands
from utils import locale as loc
from datetime import datetime

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
        embed.set_footer(text=loc.get(ctx, mn, "id").format(g.id))
        if g.icon_url:
            embed.set_thumbnail(url=g.icon_url)
        embed.add_field(name=loc.get(ctx, mn, "general"), value=loc.get(ctx, mn, "srv_general").format(
            g.owner, online, g.member_count, g.premium_subscription_count, len(g.emojis), g.emoji_limit, len(g.roles),
            g.icon_url
        ))
        embed.add_field(name=loc.get(ctx, mn, "channel"), value=loc.get(ctx, mn, "srv_channel").format(
            len(g.text_channels), len(g.voice_channels), len(g.categories), str(g.region)
        ))
        embed.add_field(name=loc.get(ctx, mn, "history"), value=loc.get(ctx, mn, "srv_history").format(
            g.created_at.strftime(loc.get(ctx, "region", "date")), int(delta.days)
        ))
        embed.add_field(name=loc.get(ctx, mn, "misc"), value=loc.get(ctx, mn, "srv_misc").format(
            int(g.filesize_limit/1024/1024), int(g.bitrate_limit/1000),
            loc.get(ctx, mn, "ct_filter")[str(g.explicit_content_filter)],
            loc.get(ctx, mn, "vr_level")[str(g.verification_level)]
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
                await ctx.send(loc.get(ctx, mn, "user_notfound"))
                return
        roles = u.roles
        roles.remove(ctx.guild.default_role)
        delta_c = datetime.now() - u.created_at
        delta_j = datetime.now() - u.joined_at
        embed = discord.Embed(color=u.color, title=u.name)
        embed.set_footer(text=loc.get(ctx, mn, "id").format(u.id))
        embed.set_thumbnail(url=u.avatar_url)
        embed.add_field(name=loc.get(ctx, mn, "general"), value=loc.get(ctx, mn, "usr_general").format(
            u.name, u.discriminator, u.display_name, loc.get(ctx, mn, "status")[u.raw_status],
            u.avatar_url
        ))
        embed.add_field(name=loc.get(ctx, mn, "roles"), value=loc.get(ctx, mn, "usr_roles").format(
            len(roles), ", ".join([r.mention for r in roles]) or loc.get(ctx, mn, "empty")
        ))
        embed.add_field(name=loc.get(ctx, mn, "history"), value=loc.get(ctx, mn, "usr_history").format(
            u.created_at.strftime(loc.get(ctx, "region", "date")), int(delta_c.days),
            u.joined_at.strftime(loc.get(ctx, "region", "date")), int(delta_j.days)
        ))
        embed.add_field(name=loc.get(ctx, mn, "misc"), value=loc.get(ctx, mn, "usr_misc").format(
            ", ".join([loc.get(ctx, mn, "flags")[p[0]] for p in u.public_flags if p[1] is True]) or
            loc.get(ctx, mn, "empty")
        ))
        await ctx.send(embed=embed)

    @commands.command(help="g_userinfo_help", brief="userinfo_brief", aliases=["guser"], name="guserinfo")
    async def g_userinfo(self, ctx, user: int = None):
        if not user:
            await ctx.send(loc.get(ctx, mn, "user_invalid_format"))
            return
        try:
            u = await self.bot.fetch_user(user)
        except discord.NotFound:
            await ctx.send(loc.get(ctx, mn, "user_notfound"))
            return
        delta_c = datetime.now() - u.created_at
        embed = discord.Embed(color=discord.Color.teal(), title=u.name)
        embed.set_footer(text=loc.get(ctx, mn, "usr_reduced_info").format(u.id))
        embed.set_thumbnail(url=u.avatar_url)
        embed.add_field(name=loc.get(ctx, mn, "general"), value=loc.get(ctx, mn, "usr_general_id").format(
            u.name, u.discriminator, u.avatar_url
        ))
        embed.add_field(name=loc.get(ctx, mn, "history"), value=loc.get(ctx, mn, "usr_history_id").format(
            u.created_at.strftime(loc.get(ctx, "region", "date")), int(delta_c.days)
        ))
        embed.add_field(name=loc.get(ctx, mn, "misc"), value=loc.get(ctx, mn, "usr_misc_id").format(
            loc.get(ctx, mn, str(u.system)),
            ", ".join([loc.get(ctx, mn, "flags")[p[0]] for p in u.public_flags if p[1] is True]) or
            loc.get(ctx, mn, "empty")
        ))
        await ctx.send(embed=embed)

    @commands.command(help="fetch_help", brief="fetch_brief")
    async def fetch(self, ctx, invite):
        try:
            f = await self.bot.fetch_invite(invite, with_counts=True)
        except discord.HTTPException or discord.NotFound:
            await ctx.send(loc.get(ctx, mn, "fetch_error"))
            return
        if invite is None:
            await ctx.send(loc.get(ctx, mn, "fetch_error"))
            return
        embed = discord.Embed(color=discord.Color.teal(), title=f.guild.name)
        if f.guild.icon_url:
            embed.set_thumbnail(url=f.guild.icon_url)
        if f.inviter:
            inviter = loc.get(ctx, mn, "user").format(f.inviter.name, f.invite.discriminator)
            embed.set_footer(text=loc.get(ctx, mn, "inv_f").format(f.inviter.id, f.guild.id))
        else:
            inviter = loc.get(ctx, mn, "empty")
            embed.set_footer(text=loc.get(ctx, mn, "inv_f_no_user").format(f.guild.id))
        embed.add_field(name=loc.get(ctx, mn, "inv_details"), value=loc.get(ctx, mn, "inv_details_v").format(
            f.code, inviter, f.url
        ))
        embed.add_field(name=loc.get(ctx, mn, "inv_guild"), value=loc.get(ctx, mn, "inv_guild_v").format(
            f.approximate_presence_count, f.approximate_member_count, f.channel.name or loc.get(ctx, mn, "empty")
        ))
        await ctx.send(embed=embed)


def setup(bot):
    plugin = Utility(bot)
    bot.add_cog(plugin)
