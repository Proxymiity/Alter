import discord
from discord.ext import commands as discord_commands
from utils.dataIO import dataIO
from utils import locale

config = dataIO.load_json("data/config.json")
prefix = config["prefix"]
loc = locale.load(config["locale"], "utils.help")
doc = locale.load(config["locale"], "commands")


async def summary(bot, ctx):
    cl = ""
    cogs = sorted(bot.cogs)
    for cog in cogs:
        cl = cl + "`{}` {}\n".format(cog, doc[cog.lower()])
    embed = discord.Embed(title=loc["help_title"], description=loc["about_bot"].format(config["name"]),
                          color=discord.Color.teal())
    embed.add_field(name=loc["help_title"], value=loc["help_how"].format(prefix), inline=False)
    embed.add_field(name=loc["modules_all"], value=cl[:-1], inline=False)
    await ctx.send(embed=embed)


async def send_help(bot, ctx):
    embeds = []
    cogs = bot.cogs
    ordered_cogs = sorted(cogs)
    for cog in ordered_cogs:
        cmds = cogs[cog].get_commands()
        embeds = _paginate(cmds, embeds)
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_plugin_help(ctx, cog):
    commands = cog.get_commands()
    embeds = _paginate(commands)
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_cmd_help(ctx, cmd, error=False):
    desc = loc["help_undef"]
    if cmd.brief:
        desc = doc[cmd.brief]
    embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.teal())
    if error:
        embed = discord.Embed(title=cmd.name, description=desc, color=discord.Color.red())
        embed.set_footer(text=loc["arg_error"])
    if cmd.help:
        embed.add_field(name=loc["help_title"], value=doc[cmd.help].format(prefix))
    embed.set_author(name=cmd.cog_name)
    await ctx.send(embed=embed)
    if isinstance(cmd, discord_commands.Group):
        embeds = _paginate(list(cmd.commands))
        for to_send in embeds:
            await ctx.send(embed=to_send)


def _paginate(commands, embeds_input=None):
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
                                  description=doc[cmds[0].cog.qualified_name.lower()])
        help_part.set_author(name=loc["help_title"])
        for x in cmds[p:n]:
            if x.brief:
                help_part.add_field(name=x.name, value=doc[x.brief], inline=False)
            else:
                help_part.add_field(name=x.name, value=loc["help_undef"], inline=True)
            p = p + 1
        embeds_input.append(help_part)
        n = n + 25
    return embeds_input
