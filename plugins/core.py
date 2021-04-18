import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import db, checks, help, tools
from utils import locale as loc
from datetime import datetime

config = dataIO.load_json("data/config.json")
locales = dataIO.load_json("locales/locales.json")
mn = "plugins.core"
inv_d = "https://bot.proxymiity.fr/@/"


class Core(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @checks.bot_owner()
    @commands.command(help="shutdown_help", brief="shutdown_brief")
    async def shutdown(self, ctx, opt="normal"):
        db.delete_table("temp")
        print(loc.get(ctx, mn, "shutdown"))
        await ctx.send(loc.get(ctx, mn, "shutdown"))
        await self.bot.change_presence(status=tools.get_status("offline"))
        if "kill" in opt:
            exit(-1)
        else:
            await self.bot.close()

    @checks.bot_owner()
    @commands.group(help="plugin_help", brief="plugin_brief")
    async def plugin(self, ctx):
        if ctx.invoked_subcommand is None:
            await help.send_cmd_help(ctx)

    @checks.bot_owner()
    @plugin.command(brief="plugin_load_brief", hidden=False)
    async def load(self, ctx, ext, store=None):
        try:
            self.bot.load_extension(ext)
            await ctx.send(loc.get(ctx, mn, "ext_loaded").format(ext))
        except commands.ExtensionNotFound:
            await ctx.send(loc.get(ctx, mn, "ext_notfound").format(ext))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(loc.get(ctx, mn, "ext_alreadyloaded").format(ext))
        finally:
            if ext not in config["loadPlugins"] and store == "-config":
                config["loadPlugins"].append(ext)
                dataIO.save_json("data/config.json", config)

    @checks.bot_owner()
    @plugin.command(brief="plugin_unload_brief", hidden=False)
    async def unload(self, ctx, ext, store=None):
        try:
            self.bot.unload_extension(ext)
            await ctx.send(loc.get(ctx, mn, "ext_unloaded").format(ext))
        except commands.ExtensionNotLoaded:
            await ctx.send(loc.get(ctx, mn, "ext_notloaded").format(ext))
        finally:
            if ext in config["loadPlugins"] and store == "-config":
                config["loadPlugins"].remove(ext)
                dataIO.save_json("data/config.json", config)

    @checks.bot_owner()
    @plugin.command(brief="plugin_reload_brief", hidden=False)
    async def reload(self, ctx, ext):
        try:
            self.bot.reload_extension(ext)
            await ctx.send(loc.get(ctx, mn, "ext_reloaded").format(ext))
        except commands.ExtensionNotFound:
            await ctx.send(loc.get(ctx, mn, "ext_notfound").format(ext))
        except commands.ExtensionNotLoaded:
            await ctx.send(loc.get(ctx, mn, "ext_notloaded").format(ext))

    @checks.bot_owner()
    @commands.group(help="config_help", brief="config_brief", aliases=["conf"])
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await help.send_cmd_help(ctx)

    @checks.bot_owner()
    @config.command(brief="config_shard_brief", name="shards", hidden=False)
    async def list_shards(self, ctx):
        sds = self.bot.shards
        pages = []
        first = discord.Embed(title=loc.get(ctx, mn, "config_shard").format(len(self.bot.shards)),
                              color=discord.Color.teal())
        for s in sds:
            pages.append([loc.get(ctx, mn, "config_shard_n").format(sds[s].id),
                          loc.get(ctx, mn, "config_shard_v").format(int(sds[s].latency*1000),
                                                                    loc.get(ctx, mn, str(not sds[s].is_closed())),
                                                                    loc.get(ctx, mn, str(sds[s].is_ws_ratelimited())))])
        for e in tools.paginate(pages, discord.Embed(color=discord.Color.teal()), first, True):
            await ctx.send(embed=e)

    @checks.bot_owner()
    @config.command(brief="config_servers_brief", name="servers", hidden=False)
    async def list_servers(self, ctx):
        servers = []
        for s in self.bot.guilds:
            servers.append([f"`{s.id}`", loc.get(ctx, mn, "config_servers_desc").format(s.name, s.owner_id)])
        for x in tools.paginate_text(servers, first=loc.get(ctx, mn, "config_servers").format(len(self.bot.guilds)),
                                     mid_sep="\n", line_sep="\n\n"):
            await ctx.send(x)

    @checks.bot_owner()
    @config.command(help="config_server_help", brief="config_server_brief", name="server", hidden=False)
    async def get_server(self, ctx, sid: int, action=None):
        g = self.bot.get_guild(sid)
        if not g:
            await ctx.send(loc.get(ctx, mn, "server_notfound"))
        elif not action:
            await ctx.send(loc.get(ctx, mn, "config_server_info").format(g.name, g.id, g.shard_id,
                                                                         loc.get(ctx, mn, str(not g.unavailable))))
        elif action == "leave":
            await g.leave()
            await ctx.send(loc.get(ctx, mn, "config_server_left").format(g.name))
        else:
            await help.send_cmd_help(ctx, error=True)

    @checks.bot_owner()
    @config.command(brief="config_invite_brief", name="invite", hidden=False)
    async def set_invite(self, ctx, link: str = None):
        if not link:
            await ctx.send(loc.get(ctx, mn, "config_invite").format(db.read("settings", 0, "invite")
                                                                    or inv_d + str(ctx.me.id)))
            return
        if link == "default":
            db.delete("settings", 0, "invite")
        elif link == "off":
            db.write("settings", 0, "invite", "off")
            await ctx.send(loc.get(ctx, mn, "config_invite_disabled"))
            return
        else:
            if not link.startswith("https://"):
                await ctx.send(loc.get(ctx, mn, "config_invite_invalid"))
                return
            db.write("settings", 0, "invite", link)
        await ctx.send(loc.get(ctx, mn, "config_invite_set").format(db.read("settings", 0, "invite")
                                                                    or inv_d + str(ctx.me.id)))

    @checks.bot_owner()
    @config.command(help="config_status_help", brief="config_status_brief", name="status", hidden=False)
    async def set_status(self, ctx, status=None):
        if status not in ["online", "idle", "dnd", "offline"]:
            await help.send_cmd_help(ctx, error=True)
            return
        db.write("settings", 0, "status", status)
        await self.bot.change_presence(status=tools.get_status(status))
        await ctx.send(loc.get(ctx, mn, "config_status_set"))

    @checks.bot_owner()
    @config.command(help="config_presence_help", brief="config_presence_brief", name="presence", hidden=False)
    async def set_presence(self, ctx, p_type, *, p_val=None):
        if p_type not in ["none", "game", "listen", "watch", "compete", "stream"] or not p_val and p_type != "none":
            await help.send_cmd_help(ctx, error=True)
            return
        if p_type == "none":
            db.write("settings", 0, "presence_type", "none")
            db.write("settings", 0, "presence_value", "none")
        else:
            db.write("settings", 0, "presence_type", p_type)
            db.write("settings", 0, "presence_value", p_val)
        await self.bot.change_presence(activity=tools.get_presence(p_type, p_val))
        await ctx.send(loc.get(ctx, mn, "config_presence_set"))

    @commands.command(hidden=False, help="invite_help", brief="invite_brief")
    async def invite(self, ctx):
        inv = db.read("settings", 0, "invite") or inv_d + str(ctx.me.id)
        if inv == "off":
            await ctx.send(loc.get(ctx, mn, "invite_disabled"))
        else:
            await ctx.send(loc.get(ctx, mn, "invite").format(inv))

    @commands.command(hidden=False, help="info_help", brief="info_brief")
    async def info(self, ctx):
        owner = self.bot.get_user(config["owner"])
        if owner is None:
            owner = loc.get(ctx, mn, "info_unknown")
        ping = int(self.bot.latency * 1000)
        embed = discord.Embed(title=loc.get(ctx, mn, "info_about"), color=discord.Color.teal())
        bot = self.bot.user
        start_at = datetime.strptime(db.read("temp", 1, "start_time"), "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - start_at
        h, r = divmod(int(diff.total_seconds()), 3600)
        m, s = divmod(r, 60)
        d, h = divmod(h, 24)
        up = f"{d}:{h}:{m}:{s}"
        embed.set_author(name=bot.name, icon_url=str(bot.avatar_url))
        embed.add_field(name=loc.get(ctx, mn, "info_bot_title"),
                        value=loc.get(ctx, mn, "info_bot").format(owner, len(self.bot.users),
                                                                  len(self.bot.guilds),
                                                                  db.read("settings", 0, "prefix"),
                                                                  len(self.bot.cogs)), inline=True)
        embed.add_field(name=loc.get(ctx, mn, "info_other_title"),
                        value=loc.get(ctx, mn, "info_other").format(ping, self.bot.user.id,
                                                                    len(self.bot.cached_messages),
                                                                    discord.__version__, up), inline=True)
        embed.set_footer(text=db.read("settings", 0, "name"))
        await ctx.send(embed=embed)

    @commands.command(hidden=False, help="help_help", brief="help_brief", name="help")
    async def _help(self, ctx, query=None):
        if query:
            if query.lower() == "all":
                await help.send_help(self.bot, ctx)
                return
            for cog in self.bot.cogs:
                if query.lower() == cog.lower():
                    await help.send_plugin_help(ctx, self.bot.cogs[cog])
                    return
            if any(c.name == query.lower() for c in self.bot.commands):
                await help.send_cmd_help(ctx, self.bot.get_command(query.lower()))
                return
            await ctx.send(loc.get(ctx, mn, "help_not_found"))
        else:
            await help.summary(self.bot, ctx)

    @checks.permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command(hidden=False, help="lang_help", brief="lang_brief", aliases=["locale"])
    async def lang(self, ctx, lang=None):
        if lang:
            if lang in locales:
                db.write("serversettings", ctx.guild.id, "locale", lang)
                await ctx.send(loc.get(ctx, mn, "lang_changed").format(locales[lang]))
            else:
                await ctx.send(loc.get(ctx, mn, "lang_not_found"))
        else:
            lc = []
            for x in locales:
                lc.append("`" + x + "` " + locales[x])
            await ctx.send(loc.get(ctx, mn, "lang_list").format("\n".join(lc)))


def setup(bot):
    plugin = Core(bot)
    bot.add_cog(plugin)
