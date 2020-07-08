import discord
import requests
import json
import re
import asyncio
import datetime
import time
import os
from key_loader import GENERAL_ACCESS_TOKEN as TKN
from urllib import parse, request
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from discord.embeds import Embed
from discord.ext import commands, timers, tasks
from bs4 import BeautifulSoup

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

description = """An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here."""
bot = commands.Bot(command_prefix="!!", description=description)
bot.timer_manager = timers.TimerManager(bot)
bot.activity = discord.Activity(
    name="!!commands",
    detail="!!commands",
    type=discord.ActivityType.listening,
    start=datetime.datetime.now(),
)

temp_dict = {}
temp_act = {}
temp_img = ""
corona_temp_dict = {}


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def request_song_info(song_title, artist_name):
    headers = {'Authorization': 'Bearer ' + TKN.GENIUS.value}
    url = 'https://api.genius.com/search'
    data = {'q': '{} {}'.format(song_title, artist_name)}
    response = requests.get(url, params=data, headers=headers)
    return response


def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = None
    # Determine the class of the div
    old_div = html.find("div", class_="lyrics")
    new_div = html.find(
        "div", class_="SongPageGrid-sc-1vi6xda-0 DGVcp Lyrics__Root-sc-1ynbvzw-0 jvlKWy")
    if old_div:
        lyrics = old_div.get_text()
    elif new_div:
        # Clean the lyrics since get_text() fails to convert "</br/>"
        lyrics = str(new_div)
        lyrics = lyrics.replace('<br/>', '\n')
        lyrics = re.sub(r'(\<.*?\>)', '', lyrics)
    else:
        return None  # In case the lyrics section isn't found
    return lyrics


def search_movie_torrent(data, movie_count, footer):
    data = data["data"]["movies"]
    embeds = []
    for i in range(movie_count):
        movie = data[i]
        temp_img = movie["medium_cover_image"]
        img = re.split("//", temp_img, 1)
        temp_img = img[0] + "//img." + img[1]
        embed = Embed(title=movie['title_long'], description='',
                      color=0x115599).set_thumbnail(url=temp_img)
        for x in range(len(movie['torrents'])):
            movie_torrent = movie['torrents'][x]
            quality = "{} {}".format(
                movie_torrent['type'].capitalize(), movie_torrent['quality'])
            embed.add_field(name=quality,
                            value=movie_torrent['url'],
                            inline=False,)
        embed.set_footer(text=footer)
        embeds.append(embed)
    return embeds


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def commands(ctx):
    embed = discord.Embed(color=16711680)
    # embed.set_author(name="These are my commands, remember I am a basic bot.", icon_url="https://cdn.discordapp.com/avatars/691329837951877181/6f14df2c65e997774265fee7388a3b16.png?size=2048")
    embed.add_field(
        name="!!search [movie name]",
        value="Search movie on YTS to download a torrent",
        inline=False,
    )
    embed.add_field(
        name="!!latest [number]",
        value="Search latest added movie with default 10 if input empty number",
        inline=False,
    )
    embed.add_field(
        name="!!top [limit number] [type] [genre]",
        value="Search Top movie with 3 different type by downloads, likes and rating",
        inline=False,
    )
    embed.add_field(
        name="!!youtube [search]", value="Search something on youtube", inline=False
    )
    embed.add_field(
        name="!!covid [country]",
        value="Return the covid-19 data for the selected country",
        inline=False,
    )
    embed.add_field(
        name="!!lyrics",
        value="Search lyrics for your listening song in spotify",
        inline=False,
    )
    embed.add_field(
        name="!!rate [movie name]",
        value="Search a rate of movie in my database",
        inline=False,
    )
    embed.set_footer(
        text="This bot is just a basic bot created by a guy that was cold with this shit of programming Py, just used as an exercise."
    )
    await ctx.send(embed=embed)


@bot.command()
async def lyrics(message):
    act = message.author.activities
    if is_empty(act):
        await message.channel.send(
            "**Your input is invalid. Please Listening Spotify For The Lyrics.**\n"
        )
    else:
        if act[-1].name == "Spotify":
            act = act[-1]
            title = act.title
            artist = act.artists[0]
            if '(' in title:
                # only take the title song, ignore a feat detail
                title = title.split(' (')[0]
            response = request_song_info(title, artist)
            data = response.json()
            song = None
            for hit in data['response']['hits']:
                if artist.lower() in hit['result']['primary_artist']['name'].lower():
                    song = hit
                    break
            if song:
                song_url = song['result']['url']
                lyrics = scrap_song_url(song_url)
                length_string = len(lyrics)
                title_name = "**{} by {} **".format(title, artist)
                footer = "**Request by {} **".format(
                    message.author.display_name
                )
                embeds = [
                ]
                l = lyrics.split('\n\n')
                if len(l) < 2:
                    embeds.append(
                        Embed(title=title_name, description=l[0], color=0x115599))
                else:
                    if len(l) % 2 == 0:
                        for i in range(0, len(l), 2):
                            l[i] = l[i]+"\n\n"+l[i+1]
                            embeds.append(
                                Embed(title=title_name, description=l[i], color=0x115599))
                    else:
                        for i in range(0, len(l)-1, 2):
                            l[i] = l[i]+"\n\n"+l[i+1]
                            embeds.append(
                                Embed(title=title_name, description=l[i], color=0x115599))
                            embeds.append(
                                Embed(title=title_name, description=l[len(l)-1], color=0x115599))
                paginator = BotEmbedPaginator(message, embeds)
                await paginator.run()
            else:
                await message.channel.send(
                    "**Sorry, there are no lyrics from this song**\n"
                )
        else:
            await message.channel.send(
                "**Your input is invalid. Please Listening Spotify For The Lyrics.**\n"
            )


@bot.command()
async def rate(message, *s: str):
    query = {"s": " ".join(s)}
    with requests.get("https://apimarbidev.000webhostapp.com/movie", params=query) as req:
        if req.status_code == 200:
            data = req.json()
            for x in data:
                for i in x:
                    if i == "id":
                        continue
                    await message.channel.send("```" + str(i) + " => " + str(x[i]) + "```")
        elif req.status_code == 404:
            data = req.json()
    await message.channel.send("```" + str(data["message"]) + "```")


@bot.command()
async def addrate(message, rate: float, *s: str):
    if message.author.id == TKN.DEVELOPERID.value:
        query = {"name": " ".join(s), "status": "Done", "rate": rate}
        with requests.post(
            "https://apimarbidev.000webhostapp.com/movie", data=query
        ) as req:
            data = req.json()
            await message.channel.send("```" + str(data["message"]) + "```")
    else:
        await message.channel.send(
            "**Sorry, You aren't developer**\n"
        )


@bot.command()
async def editrate(message, rate: float, *s: str):
    if message.author.id == TKN.DEVELOPERID.value:
        query = {"name": " ".join(s), "status": "Done", "rate": rate}
    else:
        await message.channel.send(
            "**Sorry, You aren't developer**\n"
        )


@bot.command()
async def search(message, *s: str):
    if is_empty(s):
        await message.channel.send(
            "**Your input is invalid!. Please input only Name of Movie (String)**\n"
        )
    else:
        s = " ".join(s)
        query = {"query_term": s, "sort_by": "download_count"}
        with requests.get("https://yts.mx/api/v2/list_movies.json", params=query) as req:
            if req.status_code == 200:
                data = req.json()
                footer = 'Search {} request by {}'.format(
                    s, message.author.display_name)
                movie_count = data["data"]["movie_count"]
                embeds = search_movie_torrent(data, movie_count, footer)
                paginator = BotEmbedPaginator(message, embeds)
                await paginator.run()
            elif req.status_code == 404:
                data = req.json()
                await message.channel.send("```" + str(data["status_message"]) + "```")


@bot.command()
async def latest(message, l='10'):
    if (l.isdigit()):
        l = int(l)
        # Only can be 50 Limit in YTS.mx
        if l <= 50 and l > 0:
            query = {"limit": l, "sort_by": "date_added"}
            with requests.get("https://yts.mx/api/v2/list_movies.json", params=query) as req:
                if req.status_code == 200:
                    data = req.json()
                    movie_count = data["data"]["limit"]
                    footer = 'Latest {} Movie Added Request by {}'.format(l,
                                                                          message.author.display_name)
                    embeds = search_movie_torrent(data, movie_count, footer)
                    paginator = BotEmbedPaginator(message, embeds)
                    await paginator.run()
                elif req.status_code == 404:
                    data = req.json()
                    await message.channel.send("```" + str(data["status_message"]) + "```")
        else:
            await message.channel.send(
                "**Limit between 1-50**\n"
            )
    else:
        await message.channel.send(
            "**Your input is invalid!. Please input only Numbers(Integer)**\n"
        )


@bot.command()
async def top(message, l='10', *s: str):
    if (l.isdigit()):
        if is_empty(s):
            await message.channel.send(
                "**Input list = download, rating, like. cannot be double**\n"
            )
        else:
            genre_name = ''
            if len(s) > 1:
                genre_name = s[1].lower()
            s = s[0].lower()
            if s == 'download' or s == 'downloads':
                l = int(l)
                if l <= 50 and l > 0:
                    query = {"limit": l, "sort_by": "download_count",
                             "genre": genre_name}
                    with requests.get("https://yts.mx/api/v2/list_movies.json", params=query) as req:
                        if req.status_code == 200:
                            data = req.json()
                            movie_count = data["data"]["limit"]
                            genre_check = False
                            if len(data['data']['movies']) == 1:
                                for genre in data['data']['movies'][0]['genres']:
                                    if genre_name == genre.lower():
                                        genre_check = True
                                        break
                            else:
                                genre_check = True

                            if genre_check:
                                footer = 'Top {} {} {} Movie  Request by {}'.format(
                                    l, s.capitalize(), genre_name.capitalize(), message.author.display_name)
                                embeds = search_movie_torrent(
                                    data, movie_count, footer)
                                paginator = BotEmbedPaginator(message, embeds)
                                await paginator.run()
                            else:
                                await message.channel.send(
                                    "**Genre isn't found. (See http://www.imdb.com/genre/ for full list genre)**\n"
                                )
                        elif req.status_code == 404:
                            data = req.json()
                            await message.channel.send("```" + str(data["status_message"]) + "```")
                else:
                    await message.channel.send(
                        "**Limit between 1-50**\n"
                    )
            elif s == 'rating':
                l = int(l)
                if l <= 50 and l > 0:
                    query = {"limit": l, "sort_by": "rating",
                             "genre": genre_name}
                    with requests.get("https://yts.mx/api/v2/list_movies.json", params=query) as req:
                        if req.status_code == 200:
                            data = req.json()
                            movie_count = data["data"]["limit"]
                            genre_check = False
                            if len(data['data']['movies']) == 1:
                                for genre in data['data']['movies'][0]['genres']:
                                    if genre_name == genre.lower():
                                        genre_check = True
                                        break
                            else:
                                genre_check = True
                            if genre_check:
                                footer = 'Top {} {} {} Movie  Request by {}'.format(
                                    l, s.capitalize(), genre_name.capitalize(), message.author.display_name)
                                embeds = search_movie_torrent(
                                    data, movie_count, footer)
                                paginator = BotEmbedPaginator(message, embeds)
                                await paginator.run()
                            else:
                                await message.channel.send(
                                    "**Genre isn't found. (See http://www.imdb.com/genre/ for full list genre)**\n"
                                )
                        elif req.status_code == 404:
                            data = req.json()
                            await message.channel.send("```" + str(data["status_message"]) + "```")
                else:
                    await message.channel.send(
                        "**Limit between 1-50**\n"
                    )
            elif s == 'like' or s == 'likes':
                l = int(l)
                if l <= 50 and l > 0:
                    query = {"limit": l, "sort_by": "like_count",
                             "genre": genre_name}
                    with requests.get("https://yts.mx/api/v2/list_movies.json", params=query) as req:
                        if req.status_code == 200:
                            data = req.json()
                            movie_count = data["data"]["limit"]
                            genre_check = False
                            if len(data['data']['movies']) == 1:
                                for genre in data['data']['movies'][0]['genres']:
                                    if genre_name == genre.lower():
                                        genre_check = True
                                        break
                            else:
                                genre_check = True
                            if genre_check:
                                footer = 'Top {} {} {} Movie  Request by {}'.format(
                                    l, s.capitalize(), genre_name.capitalize(), message.author.display_name)
                                embeds = search_movie_torrent(
                                    data, movie_count, footer)
                                paginator = BotEmbedPaginator(message, embeds)
                                await paginator.run()
                            else:
                                await message.channel.send(
                                    "**Genre isn't found. (See http://www.imdb.com/genre/ for full list genre)**\n"
                                )
                        elif req.status_code == 404:
                            data = req.json()
                            await message.channel.send("```" + str(data["status_message"]) + "```")
                else:
                    await message.channel.send(
                        "**Limit between 1-50**\n"
                    )
            else:
                await message.channel.send(
                    "**Input list = download, rating, like. cannot be double**\n"
                )
    else:
        await message.channel.send(
            "**Please Input limit with only number**\n"
        )


@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({"search_query": search})
    html_content = request.urlopen(
        "http://www.youtube.com/results?" + query_string)
    search_results = re.findall(
        'href="\\/watch\\?v=(.{11})', html_content.read().decode()
    )
    await ctx.send("https://www.youtube.com/watch?v=" + search_results[0])


@bot.command()
async def covid(ctx, *country: str):
    country = " ".join(country).lower()
    if country.isdigit() == True:
        await ctx.send(
            "**Please select a country with ``!!covid ['country name']`` , ex: ``!!covid Italy`` or type ``!!covid global``**"
        )
    else:
        url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
        headers = {
            "x-rapidapi-host": "coronavirus-monitor.p.rapidapi.com",
            "x-rapidapi-key": TKN.RAPIDAPI.value,
        }
        if country == "south korea":
            country = "s. korea"
        elif country == "united states":
            country = "usa"
        elif country == "us":
            country = "usa"
        elif country == "united states of america":
            country = "usa"
        elif country == "america":
            country = "usa"
        elif country == "united kingdom":
            country = "uk"
        query = {"country": country}
        url_2 = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"
        if country == "global" or is_empty(country):
            with requests.get(url_2, headers=headers) as req:
                if req.status_code == 200:
                    data = req.json()
                    embed = discord.Embed(title="Global", colour=0xFF69B4)
                    embed.set_thumbnail(
                        url="https://icons.iconarchive.com/icons/wikipedia/flags/512/UN-United-Nations-Flag-icon.png"
                    )
                    for i in data:
                        if i == "statistic_taken_at":
                            update = i + " " + data[i]
                            embed.set_footer(text=update)
                        else:
                            embed.add_field(name=i, value=data[i], inline=True)
                        if i == "total_cases":
                            cases = data[i]
                        elif i == "total_deaths":
                            deaths = data[i]
                        elif i == "total_recovered":
                            recovers = data[i]
                    cases = int(re.sub(",", "", cases))
                    deaths = int(re.sub(",", "", deaths))
                    recovers = int(re.sub(",", "", recovers))
                    embed.add_field(
                        name="Death Rate",
                        value=str(round(deaths / cases * 100, 2)) + "%",
                        inline=True,
                    )
                    embed.add_field(
                        name="Recover Rate",
                        value=str(round(recovers / cases * 100, 2)) + "%",
                        inline=True,
                    )
                    embed.add_field(
                        name="Active Cases Rate",
                        value=str(
                            round((cases - recovers - deaths) / cases * 100, 2))
                        + "%",
                        inline=True,
                    )
                    url_affected = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/affected.php"
                    with requests.get(url_affected, headers=headers) as hasil:
                        data_affected = hasil.json()
                        for i in data_affected:
                            if i == "affected_countries":
                                embed.add_field(
                                    name=i, value=len(data_affected[i]), inline=True
                                )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("**Server Error**")
        else:
            with requests.get(url, headers=headers, params=query) as req:
                if req.status_code == 200:
                    if is_empty(req.text):
                        await ctx.send("This Country don't have Covid-19 Data")
                    else:
                        data = req.json()
                        data = data["latest_stat_by_country"][0]
                        for i in data:
                            if is_empty(data[i]):
                                data[i] = 0
                        cases = data["total_cases"]
                        deaths = data["total_deaths"]
                        recovers = data["total_recovered"]
                        tests = data["total_tests"]
                        new_deaths = data["new_deaths"]
                        new_cases = data["new_cases"]
                        last_update = data["record_date"]
                        f = open(os.path.join(
                            __location__, "country_id.json"), "rb")
                        data_id = json.load(f)
                        for x in range(0, len(data_id)):
                            code = data_id[x]["code"]
                            name = data_id[x]["name"].lower()
                            if country == name:
                                idc = code
                        if country == "usa":
                            idc = "US"
                        embed = discord.Embed(
                            title=data["country_name"], colour=0xFF69B4)
                        embed.set_thumbnail(
                            url="https://www.countryflags.io/" + idc + "/flat/64.png"
                        )
                        embed.set_footer(text="Last Update: " + last_update)
                        embed.add_field(name="Cases", value=cases, inline=True)
                        embed.add_field(
                            name="Deaths", value=deaths, inline=True)
                        embed.add_field(name="Recovers",
                                        value=recovers, inline=True)
                        embed.add_field(
                            name="New Cases Today", value=new_cases, inline=True
                        )
                        embed.add_field(
                            name="New Deaths Today", value=new_deaths, inline=True
                        )
                        embed.add_field(name="Total Tests",
                                        value=tests, inline=True)
                        cases = int(re.sub(",", "", cases))
                        deaths = int(re.sub(",", "", deaths))
                        recovers = int(re.sub(",", "", recovers))
                        embed.add_field(
                            name="Death Rate",
                            value="{}% ".format(
                                str(round(deaths / cases * 100, 2))),
                            inline=True,
                        )
                        embed.add_field(
                            name="Recover Rate",
                            value="{}% ".format(
                                str(round(recovers / cases * 100, 2))),
                            inline=True,
                        )
                        active = cases - recovers - deaths
                        embed.add_field(
                            name="Active Cases Rate",
                            value="{}% ".format(
                                str(round(active / cases * 100, 2))),
                            inline=True,
                        )
                        await ctx.send(embed=embed)
                elif req.status_code == 404:
                    data = req.json()
                    await ctx.send("```" + str(data["message"]) + "```")


@bot.command()
async def test(message):
    msg = await message.channel.send("hello")


bot.run(TKN.DISCORD.value)
