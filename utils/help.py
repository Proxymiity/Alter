import discord
from discord.ext import commands as discord_commands
from utils.dataIO import dataIO
from utils import tools
from utils import locale as loc
from importlib import import_module

config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
mn = "utils.help"
dn = "commands"
prefix = db.read("settings", 0, "prefix")


async def summary(bot, ctx):
    cl = ""
    cogs = sorted(bot.cogs)
    for cog in cogs:
        cl = cl + "`{}` {}\n".format(cog, loc.get(ctx, dn, cog.lower()))
    embed = discord.Embed(title=loc.get(ctx, mn, "help_title"),
                          description=loc.get(ctx, mn, "about_bot").format(db.read("settings", 0, "name")),
                          color=discord.Color.teal())
    embed.add_field(name=loc.get(ctx, mn, "help_title"), value=loc.get(ctx, mn, "help_how").format(prefix),
                    inline=False)
    embed.add_field(name=loc.get(ctx, mn, "modules_all"), value=cl[:-1], inline=False)
    await ctx.send(embed=embed)


async def send_help(bot, ctx):
    embeds = []
    cogs = bot.cogs
    ordered_cogs = sorted(cogs)
    for cog in ordered_cogs:
        cmds = cogs[cog].get_commands()
        embeds = _paginate(ctx, cmds, embeds)
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_plugin_help(ctx, cog):
    commands = cog.get_commands()
    embeds = _paginate(ctx, commands)
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_cmd_help(ctx, cmd, error=False):
    desc = loc.get(ctx, mn, "help_undef")
    if cmd.brief:
        desc = loc.get(ctx, dn, cmd.brief)
    embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.teal())
    if error:
        embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.red())
        embed.set_footer(text=loc.get(ctx, mn, "arg_error"))
    if cmd.help:
        embed.add_field(name=loc.get(ctx, mn, "help_title"), value=loc.get(ctx, dn, cmd.help).format(prefix))
    embed.set_author(name=cmd.cog_name)
    await ctx.send(embed=embed)
    if isinstance(cmd, discord_commands.Group):
        embeds = _paginate(ctx, list(cmd.commands))
        for to_send in embeds:
            await ctx.send(embed=to_send)


def _paginate(ctx, commands, embeds_input=None):
    pages = []
    cmds = commands.copy()
    for command in commands:
        if command.hidden is True:
            cmds.remove(command)
    for x in cmds:
        pages.append([x.name, loc.get(ctx, dn, x.brief or "help_undef")])
    main = discord.Embed(title=cmds[0].cog.qualified_name, color=discord.Color.teal(),
                         description=loc.get(ctx, dn, cmds[0].cog.qualified_name.lower()))
    return tools.paginate(pages, discord.Embed(color=discord.Color.teal()), main, False, embeds=embeds_input)
