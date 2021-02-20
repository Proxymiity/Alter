import discord
from discord.ext import commands as discord_commands
from utils.dataIO import dataIO
from utils import locale as loc
from importlib import import_module

config = dataIO.load_json("data/config.json")
mn = "utils.help"
dn = "commands"
db = import_module(config["storage"])
db.create_table("serversettings")
prefix = config["prefix"]


async def summary(bot, ctx):
    cl = ""
    cogs = sorted(bot.cogs)
    for cog in cogs:
        cl = cl + "`{}` {}\n".format(cog, loc.get(ctx, db, dn, cog.lower()))
    embed = discord.Embed(title=loc.get(ctx, db, mn, "help_title"),
                          description=loc.get(ctx, db, mn, "about_bot").format(config["name"]),
                          color=discord.Color.teal())
    embed.add_field(name=loc.get(ctx, db, mn, "help_title"), value=loc.get(ctx, db, mn, "help_how").format(prefix),
                    inline=False)
    embed.add_field(name=loc.get(ctx, db, mn, "modules_all"), value=cl[:-1], inline=False)
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
    desc = loc.get(ctx, db, mn, "help_undef")
    if cmd.brief:
        desc = loc.get(ctx, db, dn, cmd.brief)
    embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.teal())
    if error:
        embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.red())
        embed.set_footer(text=loc.get(ctx, db, mn, "arg_error"))
    if cmd.help:
        embed.add_field(name=loc.get(ctx, db, mn, "help_title"), value=loc.get(ctx, db, dn, cmd.help).format(prefix))
    embed.set_author(name=cmd.cog_name)
    await ctx.send(embed=embed)
    if isinstance(cmd, discord_commands.Group):
        embeds = _paginate(ctx, list(cmd.commands))
        for to_send in embeds:
            await ctx.send(embed=to_send)


def _paginate(ctx, commands, embeds_input=None):
    if embeds_input is None:
        embeds_input = []
    command_list = commands
    cmds = command_list.copy()
    for command in command_list:
        if command.hidden is True:
            cmds.remove(command)
    cmds.sort(key=lambda c: c.name, reverse=False)
    p = 0
    n = 25
    while p < len(cmds):
        help_part = discord.Embed(title=cmds[0].cog.qualified_name, color=discord.Color.teal(),
                                  description=loc.get(ctx, db, dn, cmds[0].cog.qualified_name.lower()))
        help_part.set_author(name=loc.get(ctx, db, mn, "help_title"))
        for x in cmds[p:n]:
            if x.brief:
                help_part.add_field(name=x.name, value=loc.get(ctx, dn, mn, x.brief), inline=False)
            else:
                help_part.add_field(name=x.name, value=loc.get(ctx, db, mn, "help_undef"), inline=True)
            p = p + 1
        embeds_input.append(help_part)
        n = n + 25
    return embeds_input
