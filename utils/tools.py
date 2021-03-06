import discord
from utils.dataIO import dataIO
from importlib import import_module
config = dataIO.load_json("data/config.json")
db = import_module(config["storage"])
tb_d = ["serversettings", "settings"]
db_d = {"name": "Alter", "prefix": "::", "locale": "en_US", "status": "online",
        "presence_type": "game", "presence_value": "::help"}


def check_defaults():
    for t in tb_d:
        db.create_table(t)
    db.delete_table("temp")
    db.create_table("temp")
    for x in db_d:
        if not db.read("settings", 0, x):
            db.write("settings", 0, x, db_d[x])


def get_presence(p_type, p_val):
    if p_type == "none":
        return None
    elif p_type == "game":
        return discord.Game(p_val)
    elif p_type == "listen":
        return discord.Activity(name=p_val, type=discord.ActivityType.listening)
    elif p_type == "watch":
        return discord.Activity(name=p_val, type=discord.ActivityType.watching)
    elif p_type == "compete":
        return discord.Activity(name=p_val, type=discord.ActivityType.competing)
    elif p_type == "stream":
        s = p_val.split(";", 1)
        return discord.Streaming(name=s[1], url=s[0])


def get_status(status):
    if status == "online":
        return discord.Status.online
    elif status == "idle":
        return discord.Status.idle
    elif status == "dnd":
        return discord.Status.dnd
    elif status == "offline":
        return discord.Status.offline


def paginate(inp, base, first=None, inline=False, embeds=None, i_nb=25, i_st=0):
    first = first or base
    embeds = embeds or []
    inp.sort(key=lambda c: c[0], reverse=False)
    for x in inp[i_st:i_nb]:
        first.add_field(name=x[0], value=x[1], inline=inline)
        i_st += 1
    embeds.append(first)
    i_nb += i_nb
    while i_st < len(inp):
        embed = base.copy()
        for x in inp[i_st:i_nb]:
            embed.add_field(name=x[0], value=x[1], inline=inline)
            i_st += 1
        embeds.append(embed)
        i_nb += i_nb
    return embeds


def split_text(inp, chars=2000):
    return [inp[x:x+chars] for x in range(0, len(inp), chars)]


def paginate_text(inp, base_pre="", base_after="", first=None, mid_sep=": ", line_sep="\n", max_char=2000):
    first = first or base_pre
    outputs = [""]
    output_cursor = 0
    base_len = len(base_pre) + len(base_after)
    outputs[output_cursor] += first + line_sep
    inp.sort(key=lambda c: c[0], reverse=False)
    for x in inp:
        ap_len = len(x[0]) + len(mid_sep) + len(x[1]) + len(line_sep)
        if len(outputs[output_cursor]) + ap_len + base_len >= max_char:
            outputs[output_cursor] += base_after
            outputs.append("")
            output_cursor += 1
            outputs[output_cursor] += base_pre + line_sep
        outputs[output_cursor] += x[0] + mid_sep + x[1] + line_sep
    return outputs
