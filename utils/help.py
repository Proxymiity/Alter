import discord
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


async def send_help(bot, ctx, include=False):
    embeds = []
    cogs = bot.cogs
    ordered_cogs = sorted(cogs)
    for cog in ordered_cogs:
        cmds = cogs[cog].get_commands()
        cmds.sort(key=lambda c: c.name, reverse=False)
        p = 0
        n = 20
        while p < len(cmds):
            help_part = discord.Embed(title=cog, color=discord.Color.teal())
            help_part.set_author(name=loc["help_all"])
            for cmd in cmds[p:n]:
                if cmd.hidden is True and include is False:
                    pass
                elif cmd.brief:
                    help_part.add_field(name=cmd.name, value=doc[cmd.brief], inline=False)
                else:
                    help_part.add_field(name=cmd.name, value=loc["help_undef"], inline=True)
                p = p+1
            embeds.append(help_part)
            n = n+20
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_plugin_help(ctx, cog):
    embeds = []
    cmds = cog.get_commands()
    cmds.sort(key=lambda c: c.name, reverse=False)
    p = 0
    n = 20
    while p < len(cmds):
        help_part = discord.Embed(title=cog.qualified_name, color=discord.Color.teal(),
                                  description=doc[cog.qualified_name.lower()])
        help_part.set_author(name=loc["help_title"])
        for cmd in cmds[p:n]:
            if cmd.hidden is True:
                pass
            elif cmd.brief:
                help_part.add_field(name=cmd.name, value=doc[cmd.brief], inline=False)
            else:
                help_part.add_field(name=cmd.name, value=loc["help_undef"], inline=True)
            p = p+1
        embeds.append(help_part)
        n = n+20
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
