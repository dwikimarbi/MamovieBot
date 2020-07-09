## Motives & Background
From the beginning,  I created this bot to make it easier for me to get the data of the films that I had watched. 

The First Thing i do is create a **REST API**. I want to assess the films that I have watched and put that value into the database. I want to easily access it in the future. In the same time, I often use Discord to communicate. Especially for communicate with my friends and play with some bot. In Discord the bots is massively used on all servers. Bots are made in different ways, some are very useful to the odd ones. From here I thought to make a discord bot and at the same time completing a portfolio to add some value to my courses. For the First time i do to my bot is see a rate from my movie database at my REST API. After then i create for **CRUD in my bot**. 

But I found something interesting than just making a film database. That is downloading the torrent. I know this illegal, but this is first api for me to study public api. I will that feature in the future. Then I thought about getting the latest **covid-19** data to find out the development of the pandemic in this day.

For the latest features, which are lyrics when listening to spotify, I was inspired to get the lyrics without having to go to the Google web to search for them and use Discord bot to quickly search for the lyrics.

## Project & Duration
I started this project in **March 2020** and it's been running for 4 months at the time of i write this. 

But there were times when I stopped developing the bot because of a lot of things that I was working on. As of the date of i write this documentation, my bot is already in the 55th version according to deployment to cloud hosted on Heroku. With the development details as follows:
* REST API for movie database: 1 Week
* Making Bot: 1 Day
* Accessing rest api and making torrent links: 2-3 Weeks + 2 weeks (There is a change from updates to faster performance. Improvements to make it easier for users)
* Making covid-19 info: 2-3 days + a days (There is a change from updates to faster performance. Improvements to make it easier for users)
* Making spotify lyrics: 2-3 days + a days (There is a change from updates to faster performance. Improvements to make it easier for users. Especially For this i make a major change from musixmatch api to genius api. i will explain this in insight.md) 

### Note
I just guessed but i can be sure this is right. I forgot exactly how much time that i spend.

## Structure Codes
For my discord.py bot that i use divided into several files :
```
MamovieBot
├── .gitignore
├── LICENSE.txt
├── README.md
├── .env
├── country_id.json
├── mamovie_bot.py
|     ├── is_empty
|     ├── request_song_info
|     ├── scrap_song_url
|     ├── search_movie_torrent
|     ├── on_ready
|     ├── commands
|     ├── lyrics
|     ├── rate
|     ├── editrate
|     ├── search
|     ├── latest
|     ├── top
|     ├── youtube
|     ├── covid
|     └── test
├── key_loader.py
|     └── GENERAL_ACCESS_TOKEN
└── requirements.txt
```

And then for my REST-API i use a CodeIgniter Framework. With add a library from [codeigniter-restserver](https://github.com/chriskacerguis/codeigniter-restserver) by  chriskacerguis. :
```
Mamovie REST API
|   application
|   ├── config
|   |     └── rest.php
|   ├── controllers
|   |     ├── CountryId.php (In the Future, i will use my country id api for my bot)
|   |     |     ├── get
|   |     |     ├── post
|   |     |     ├── put
|   |     |     └── delete
|   |     ├── Movie.php
|   |     |     ├── get
|   |     |     ├── post
|   |     |     ├── put
|   |     └──   └── delete
|   ├── libraries
|   |     └── RestController.php
|   ├── controllers
|   |     ├── CountryId_model.php (In the Future, i will use my country id api for my bot)
|   |     |     ├── get
|   |     |     ├── create
|   |     |     ├── update
|   |     |     └── delete
|   |     ├── Movie_model.php
|   |     |     ├── get
|   |     |     ├── post
|   |     |     ├── put
└── └──   └──   └── delete
```

## Class and Function 
File: mamovie_bot.py
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
is_empty | public | any_structure | Boolean
request_song_info | public | song_title : str, artist_name : str | response : response
scrap_song_url | public | url : str | lyrics : str
search_movie_torrent | public | data : dict, movie_count : int, footer : str | embeds : list
on_ready | public | None | None
commands | public | ctx : discord.ctx | None
lyrics | public | message : discord.message | None
rate | public | message : discord.message, s : Tuple | None
addrate | public | message : discord.message, rate : float, s : Tuple | None
editrate | public | message : discord.message, rate : float, s : Tuple | None
search | public | message : discord.message, s : Tuple | None
latest | public | message : discord.message, l : int | None
top | public | message : discord.message, l : int, s : Tuple | None
youtube | public | ctx : discord.ctx, search : Tuple | None
covid | public | message : discord.message, country : Tuple | None
test | public | message : discord.message | None

File: key_loader.py
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
load_dotenv | public | None | None

File: CountryId.php
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
construct | private | None | None
index_get | public | code : str, name : str | response : response
index_post | public | code : str, name : str | response : response
index_put | public | code : str, name : str | response : response
index_delete | public | code : str | response : response

File: Movies.php
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
construct | private | None | None
index_get | public | id : int, name : str | response : response
index_post | public | name : str, status : str, rate : float | response : response
index_put | public | name : str, status : str, rate : float | response : response
index_delete | public | id : int | response : response

File: CountryId_model.php
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
getCountryId | public | code : str, name : str | response : response
createCountryId | public | code : str, name : str | response : response
updateCountryId | public | code : str, name : str | response : response
deleteCountryId | public | code : str | response : response

File: Movies_model.php
Function Name | Access Level | Parameter | Return 
--- | --- | --- | --- 
getMovie | public | id : int, name : str | response : response
createMovie | public | name : str, status : str, rate : float | response : response
updateMovie | public | name : str, status : str, rate : float | response : response
deleteMovie | public | id : int | response : response

## Statistics
mamovie_bot.py = 596 - 24 lines = 572 lines
key_loader.py = 14 lines
CountryId.php = 118 lines
Movies.php = 121 lines
CountryId_model.php = 34 lines
Movies_model.php = 34 lines
.env = 6 lines

### Total Lines = 899 lines

