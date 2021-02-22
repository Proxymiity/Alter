import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import checks, help
from utils import locale as loc
from importlib import import_module

config = dataIO.load_json("data/config.json")
locales = dataIO.load_json("locales/locales.json")
db = import_module(config["storage"])
mn = "plugins.core"


class Core(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="shutdown_help", brief="shutdown_brief")
    @checks.bot_owner()
    async def shutdown(self, ctx, opt="normal"):
        if "kill" in opt:
            print("Bot shutdown seq. called with exit()")
            exit(-1)
        else:
            print(loc.get(ctx, db, mn, "shutdown"))
            await ctx.send(loc.get(ctx, db, mn, "shutdown"))
            await self.bot.logout()

    @commands.group(help="plugin_help", brief="plugin_brief")
    @checks.bot_owner()
    async def plugin(self, ctx):
        if ctx.invoked_subcommand is None:
            await help.send_cmd_help(ctx, ctx.command)

    @plugin.command(brief="plugin_load_brief", hidden=False)
    @checks.bot_owner()
    async def load(self, ctx, ext, store=None):
        try:
            self.bot.load_extension(ext)
            await ctx.send(loc.get(ctx, db, mn, "ext_loaded").format(ext))
        except commands.ExtensionNotFound:
            await ctx.send(loc.get(ctx, db, mn, "ext_notfound").format(ext))
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(loc.get(ctx, db, mn, "ext_alreadyloaded").format(ext))
        finally:
            if ext not in config["loadPlugins"] and store == "-config":
                config["loadPlugins"].append(ext)
                dataIO.save_json("data/config.json", config)

    @plugin.command(brief="plugin_unload_brief", hidden=False)
    @checks.bot_owner()
    async def unload(self, ctx, ext, store=None):
        try:
            self.bot.unload_extension(ext)
            await ctx.send(loc.get(ctx, db, mn, "ext_unloaded").format(ext))
        except commands.ExtensionNotLoaded:
            await ctx.send(loc.get(ctx, db, mn, "ext_notloaded").format(ext))
        finally:
            if ext in config["loadPlugins"] and store == "-config":
                config["loadPlugins"].remove(ext)
                dataIO.save_json("data/config.json", config)

    @plugin.command(brief="plugin_reload_brief", hidden=False)
    @checks.bot_owner()
    async def reload(self, ctx, ext):
        try:
            self.bot.reload_extension(ext)
            await ctx.send(loc.get(ctx, db, mn, "ext_reloaded").format(ext))
        except commands.ExtensionNotFound:
            await ctx.send(loc.get(ctx, db, mn, "ext_notfound").format(ext))
        except commands.ExtensionNotLoaded:
            await ctx.send(loc.get(ctx, db, mn, "ext_notloaded").format(ext))

    @commands.command(hidden=False, help="info_help", brief="info_brief")
    async def info(self, ctx):
        owner = self.bot.get_user(config["owner"])
        if owner is None:
            owner = loc.get(ctx, db, mn, "info_unknown")
        ping = int(self.bot.latency * 1000)
        embed = discord.Embed(title=loc.get(ctx, db, mn, "info_about"), color=discord.Color.teal())
        bot = self.bot.user
        embed.set_author(name=bot.name, icon_url=str(bot.avatar_url))
        embed.add_field(name=loc.get(ctx, db, mn, "info_bot_title"),
                        value=loc.get(ctx, db, mn, "info_bot").format(owner, len(self.bot.users),
                                                                      len(self.bot.guilds),
                                                                      db.read("settings", 0, "prefix"),
                                                                      len(self.bot.cogs)), inline=True)
        embed.add_field(name=loc.get(ctx, db, mn, "info_other_title"),
                        value=loc.get(ctx, db, mn, "info_other").format(ping, self.bot.user.id,
                                                                        len(self.bot.cached_messages),
                                                                        discord.__version__), inline=True)
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
            await ctx.send(loc.get(ctx, db, mn, "help_not_found"))
        else:
            await help.summary(self.bot, ctx)

    @commands.guild_only()
    @commands.command(hidden=False, help="lang_help", brief="lang_brief")
    async def lang(self, ctx, lang=None):
        if lang:
            if lang in locales:
                db.write("server_settings", ctx.guild.id, "locale", lang)
                ctx.send(loc.get(ctx, db, mn, "lang_changed").format(locales[lang]))
            else:
                ctx.send(loc.get(ctx, db, mn, "lang_not_found"))
        else:
            lc = []
            for x in locales:
                lc.append("`" + x + "` " + locales[x])
            await ctx.send(loc.get(ctx, db, mn, "lang_list").format("\n".join(lc)))


def setup(bot):
    plugin = Core(bot)
    bot.add_cog(plugin)
