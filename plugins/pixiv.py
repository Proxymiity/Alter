import discord
import asyncio
import requests
import pixivpy3
from discord.ext import commands
from utils import help
from utils import locale as loc
from utils.dataIO import dataIO

p_conf = dataIO.load_json("data/pixiv.config.json")
mn = "plugins.pixiv"
proxy = {"cache": p_conf["image_proxy"], "api": p_conf["image_proxy_api"]}
site_url = "https://www.pixiv.net/"
icon_url = "https://www.pixiv.net/favicon.ico"
user_url = "https://www.pixiv.net/users/{0}"
art_url = "https://www.pixiv.net/artworks/{0}"


class Pixiv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = pixivpy3.aapi.AppPixivAPI()
        self.api = pixivpy3.papi.PixivAPI()
        self._refresh_tokens()

    @commands.group(help="pixiv_help", brief="pixiv_brief", aliases=["px"])
    async def pixiv(self, ctx):
        if ctx.invoked_subcommand is None:
            await help.send_cmd_help(ctx)

    @commands.cooldown(1, 5)
    @pixiv.command(help="pixiv_tags_help", brief="pixiv_tags_brief", aliases=["tag"])
    async def tags(self, ctx, *, term: str):
        term = term[:32]
        page = 1
        offset = 0
        np = False

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            await ctx.trigger_typing()
            r = self._search_illustrations(term, offset)
            if not r["list"]:
                await ctx.send(loc.get(ctx, mn, "tag_search_empty"))
                return
            ilu_embed = self._embed_illustrations(ctx, term, r, page)
            list_msg = await ctx.send(embed=ilu_embed)
            while True:
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    await ctx.send(loc.get(ctx, mn, "tag_timeout"))
                    break
                if msg.content.strip().lower() == "next":
                    if r["next"]:
                        await msg.delete()
                        np = True
                        break
                    else:
                        await ctx.send(loc.get(ctx, mn, "tag_no_next_page"))
                elif msg.content.strip().lower() == "all":
                    send_msg = await ctx.send(loc.get(ctx, mn, "tag_sending"))
                    for x in r["list"]:
                        await ctx.trigger_typing()
                        await self._send_illustration(ctx, x, False)
                    await send_msg.delete()
                elif msg.content.strip().lower() == "quit":
                    await ctx.send(loc.get(ctx, mn, "tag_quit"))
                    break
                else:
                    try:
                        select = int(msg.content.strip())-1
                        if select in range(0, len(r["list"])):
                            send_msg = await ctx.send(loc.get(ctx, mn, "tag_sending"))
                            await ctx.trigger_typing()
                            await self._send_illustration(ctx, r["list"][select])
                            await send_msg.delete()
                        else:
                            await ctx.send(loc.get(ctx, mn, "tag_choice_err"))
                            return
                    except ValueError:
                        await ctx.send(loc.get(ctx, mn, "tag_choice_err"))
                        return
            if np:
                np = False
                await list_msg.delete()
                page += 1
                offset = r["next"]
            else:
                return

    @staticmethod
    def _preload_cache(ilu):
        if ilu["meta_pages"]:
            for x in ilu["meta_pages"]:
                req = requests.get(proxy["api"].format(x["image_urls"]["original"], site_url))
                if not req.json()["cached"]:
                    requests.get(proxy["api"].format(x["image_urls"]["original"], site_url) + "&create=1")
        else:
            req = requests.get(proxy["api"].format(ilu["meta_single_page"]["original_image_url"], site_url))
            if not req.json()["cached"]:
                requests.get(proxy["api"].format(ilu["meta_single_page"]["original_image_url"], site_url)
                             + "&create=1")
        i_req = requests.get(proxy["api"].format(ilu["user"]["profile_image_urls"]["medium"], site_url))
        if not i_req.json()["cached"]:
            requests.get(proxy["api"].format(ilu["user"]["profile_image_urls"]["medium"], site_url)
                         + "&create=1")

    async def _send_illustration(self, ctx, ilu, send_error=True):
        if ilu["x_restrict"] == 1:
            if not p_conf["allow_nsfw"]:
                if send_error:
                    await ctx.send(loc.get(ctx, mn, "tag_no_nsfw"))
                return
            if not ctx.channel.is_nsfw():
                if send_error:
                    await ctx.send(loc.get(ctx, mn, "tag_is_nsfw"))
                return
        embed = discord.Embed(title=ilu["title"][:256], description=ilu["caption"][:2048],
                              url=art_url.format(ilu["id"]), color=discord.Color.teal())
        embed.set_author(name=ilu["user"]["name"][:256], url=user_url.format(ilu["user"]["id"]),
                         icon_url=proxy["cache"].format(ilu["user"]["profile_image_urls"]["medium"], site_url))
        tags = ", ".join([x["translated_name"] or x["name"] for x in ilu["tags"]])
        embed.add_field(name="tag_e_tags", value=tags[:1024])
        self._preload_cache(ilu)
        if ilu["meta_pages"]:
            y = 1
            embed.set_image(url=proxy["cache"].format(ilu["meta_pages"][0]["image_urls"]["original"], site_url))
            embed.set_footer(text=loc.get(ctx, mn, "tag_e_id_page").format(
                ilu["id"], y, len(ilu["meta_pages"])))
            to_send = [embed]
            y += 1
            for x in ilu["meta_pages"][1:]:
                part_embed = discord.Embed(color=discord.Color.teal())
                part_embed.set_image(url=proxy["cache"].format(x["image_urls"]["original"], site_url))
                part_embed.set_footer(text=loc.get(ctx, mn, "tag_e_id_page").format(
                    ilu["id"], y, len(ilu["meta_pages"])))
                to_send.append(part_embed)
                y += 1
            for x in to_send:
                await ctx.send(embed=x)
        else:
            embed.set_image(url=proxy["cache"].format(ilu["meta_single_page"]["original_image_url"], site_url))
            embed.set_footer(text=loc.get(ctx, mn, "tag_e_id").format(ilu["id"]))
            await ctx.send(embed=embed)

    def _embed_illustrations(self, ctx, term, r, cp):
        strings = []
        y = 1
        for x in r["list"]:
            strings.append(f"{y}. " + self._format_illustration(ctx, x))
            y += 1
        embed = discord.Embed(color=discord.Color.teal(), name=term, description=loc.get(ctx, mn, "tag_e_desc"))
        embed.set_author(icon_url=icon_url, name=loc.get(ctx, mn, "tag_e_sr"))
        embed.set_footer(text=loc.get(ctx, mn, "tag_e_page").format(cp))
        if strings[15:]:
            embed.add_field(name=loc.get(ctx, mn, "tag_e_works1"), value="\n".join(strings[:15]))
            embed.add_field(name=loc.get(ctx, mn, "tag_e_works2"), value="\n".join(strings[15:]))
        else:
            embed.add_field(name=loc.get(ctx, mn, "tag_e_works"), value="\n".join(strings[:15]))
        return embed

    @staticmethod
    def _format_illustration(ctx, ilu):
        r18 = True if ilu["x_restrict"] == 1 else False
        if r18:
            ilu_string = loc.get(ctx, mn, "tag_fs")
        else:
            ilu_string = loc.get(ctx, mn, "tag_fs_nsfw")
        ilu_name = ilu["title"][:30]
        ilu_author = ilu["user"]["name"][:20]
        ilu_pages = len(ilu["meta_pages"]) if ilu["meta_pages"] else 1
        return ilu_string.format(ilu_name, ilu_author, ilu_pages)

    def _search_illustrations(self, term, offset=0):
        self._refresh_tokens()
        req = self.app.search_illust(word=term, offset=offset)
        return {"list": req["illusts"], "next": offset+len(req["illusts"]) if req["next_url"] else 0}

    def _refresh_tokens(self):
        self.app_token = self.app.auth(refresh_token=p_conf["refresh_token"])["access_token"]
        self.api_token = self.api.auth(refresh_token=p_conf["refresh_token"])["access_token"]


def setup(bot):
    plugin = Pixiv(bot)
    bot.add_cog(plugin)
