import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils import locale

config = dataIO.load_json("data/config.json")
prefix = config["prefix"]
lang = locale.load(config["lang"], "commands")


async def summary(bot, ctx):
    pass  # todo add summary with core plugin and plugin list


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
            help_part = discord.Embed(title=cog, color=discord.Color.blurple())
            help_part.set_author(name=lang["help_all"])
            for cmd in cmds[p:n]:
                if cmd.hidden is True and include is False:
                    pass
                elif cmd.brief:
                    help_part.add_field(name=cmd.name, value=lang[cmd.brief], inline=False)
                else:
                    help_part.add_field(name=cmd.name, value=lang["help_undef"], inline=True)
                p = p+1
            embeds.append(help_part)
            n = n+20
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_plugin_help(bot, ctx, cog):
    embeds = []
    cmds = cog.get_commands()
    cmds.sort(key=lambda c: c.name, reverse=False)
    p = 0
    n = 20
    while p < len(cmds):
        help_part = discord.Embed(title=cog.qualified_name, color=discord.Color.blurple())
        help_part.set_author(name=lang["help_title"])
        for cmd in cmds[p:n]:
            if cmd.hidden is True:
                pass
            elif cmd.brief:
                help_part.add_field(name=cmd.name, value=lang[cmd.brief], inline=False)
            else:
                help_part.add_field(name=cmd.name, value=lang["help_undef"], inline=True)
            p = p+1
        embeds.append(help_part)
        n = n+20
    for to_send in embeds:
        await ctx.send(embed=to_send)


async def send_cmd_help(bot, ctx, cmd: discord.ext.commands.Command):
    embed = discord.Embed(title=cmd.name, description=lang[cmd.brief])
    embed.add_field(name=lang["help_title"], value=lang[cmd.help].format(prefix))
    embed.set_author(name=cmd.cog_name)
    await ctx.send(embed=embed)