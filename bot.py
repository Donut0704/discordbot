# bot.py
# gif
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
# discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
import discord

api_instance = giphy_client.DefaultApi()

# 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('giphy_api_key')
# 2
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!k ',
                   guild_subscriptions=True, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='jouw problemen'))
    print(f'{bot.user.name} has connected to Discord!')


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(
            giphy_token, query, limit=100, rating='g')
        lst = list(response.data)
        gif = random.choices(lst)

        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


@bot.event
async def on_member_join(member):

    channel = bot.get_channel(775697365662302222)
    await channel.send(f'Hoi {member.mention}, welkom Bij Bjarn&co!')


@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Ongeldige command.')


@ bot.command(name='roll_dice', help='Simuleert een dobbelsteen.')
async def roll(ctx, aantal_dobbelstenen: int, aantal_zijdes: int):
    dice = [
        str(random.choice(range(1, aantal_zijdes + 1)))
        for _ in range(aantal_dobbelstenen)
    ]
    await ctx.send(', '.join(dice))


@ roll.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Gelieve het aantal dobbelstenen en zijdes te specifiëren. Typ !k help roll_dice voor meer info.')


@ bot.command(name='99', help='Reageert met een random zin van Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'Ik ben de menselijke vorm van de 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='simp', help='Zegt hoe simp je bent')
async def simp(ctx, user: discord.Member):

    simprate = random.choice(range(0, 101))
    if simprate > 0 and simprate < 30:
        answer = " heeft gelukkige tijden. Zelf gaat hij weinig om met jongens/meisjes. Ben je zeker gelukkig?"

    if simprate >= 30 and simprate <= 80:
        answer = ' is gezond en in evenwicht.'

    if simprate >= 80 and simprate <= 100:
        answer = 'is te druk bezig met zijn/haar liefdesleven. Ga eens om met je vrienden.'

    embedVar = discord.Embed(
        title="Simp machine", description=user.mention + answer+" simprate: " + str(simprate) + "%", color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@simp.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        simprate = random.choice(range(0, 101))
        if simprate > 0 and simprate < 30:
            answer = " heeft gelukkige tijden. Zelf gaat hij weinig om met meisjes. Ben je zeker gelukkig?"

        if simprate >= 30 and simprate <= 80:
            answer = ' is gezond en in evenwicht.'

        if simprate >= 80 and simprate <= 100:
            answer = ' is te druk bezig met zijn liefdesleven. Ga eens om met je vrienden.'
        embedVar = discord.Embed(
            title="Simp machine", description=ctx.message.author.mention + answer+" Simprate: " + str(simprate) + "%", color=0xF1F014)
        await ctx.channel.send(embed=embedVar)


@bot.command(name='Bjarnismyking', help='Zegt jou wie de koning is')
async def bjarnismyking(ctx):
    await ctx.send(ctx.message.author.mention + " je weet toch wel wie de baas is hier.")


@bot.command(name='Bjarn', help="Zegt random zinnen")
async def Bjarn(ctx):
    bjarn_quotes = [
        'Kerst komt eraan, ben je al op zoek naar je cadeautjes? Vergeet ze niet, als je er geen hebt, krijg je zelf geen cadeautjes.',
        'Jouw koningin is toegekomen.',
        'Hoe is je dag?',
        'Ja'
    ]
    antwoord = random.choice(bjarn_quotes)
    await ctx.send(antwoord)


@bot.command(name='gay', help="Zegt hoe gay je bent")
async def gay(ctx, user: discord.Member):
    gay_quotes = [
        ' ha gaaayyyy!',
        ' is gay van het maximum level. Hij simpst zelfs voor jongens.',
        ' heeft wat gay trekjes, maar hij valt niet op jongens.',
        ' is hetero. Niets meer om te zeggen.',
        ' heef gewoon een gay naam.',
        ' is bi. Hij moet echt weten wat hij wilt.'
    ]
    gayanswer = random.choice(gay_quotes)
    await ctx.send(user.mention + gayanswer)


@gay.error
async def on_command_error(ctx, error):

    gay_quotes = [
        ' ha gaaayyyy!',
        ' is gay van het maximum level. Hij simpst zelfs voor jongens.',
        ' heeft wat gay trekjes, maar hij valt niet op jongens.',
        ' is hetero. Niets meer om te zeggen.',
        ' heef gewoon een gay naam.',
        ' is bi. Hij moet echt weten wat hij wilt.'
    ]
    gayanswer = random.choice(gay_quotes)
    await ctx.send(ctx.message.author.mention + gayanswer)


@bot.command(name='fortnite', help='Zegt hoe verslaafd je bent aan fortnite.')
async def fortnite(ctx, user: discord.Member):
    fortnite_quotes = [
        ' speelde fortnite toen het nog een hype was. Hij verwijderde het spel en heeft nu een betere leven.',
        ' is totaal niet verslaafd aan fortnite. Ik denk dat hij zelfs niet eens weet wat het is.',
        ' heeft het spel nooit gewild dat het spel beston en zal het nooit spelen. Hij denkt dat het een schaamte is voor de hele gamingworld.',
        ' is verslaafd aan fortnite maar aan het hoogste level. Hij spendeert de hele dag een deze game, terwijl zijn vrienden Minecraft samenspelen en fun hebben. Hij denkt zelfs dat hij een fartnite cup zal winnen.',
        ' wilt het spel spelen als hij kan spelen met zijn vrienden, maar wou nooitt alleen spelen. Dan speelt hij iets anders met zijn vrienden of belt hij met meisjes omdat hij dat ook leuk vind.',
    ]
    fortniteanswer = random.choice(fortnite_quotes)
    embedVar = discord.Embed(
        title="Fortnite verslaving", description=user.mention + fortniteanswer, color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@fortnite.error
async def on_command_error(ctx, error):
    fortnite_quotes = [
        ' speelde fortnite toen het nog een hype was. Hij verwijderde het spel en heeft nu een betere leven.',
        ' is totaal niet verslaafd aan fortnite. Ik denk dat hij zelfs niet eens weet wat het is.',
        ' heeft het spel nooit gewild dat het spel beston en zal het nooit spelen. Hij denkt dat het een schaamte is voor de hele gamingworld.',
        ' is verslaafd aan fortnite maar aan het hoogste level. Hij spendeert de hele dag een deze game, terwijl zijn vrienden Minecraft samenspelen en fun hebben. Hij denkt zelfs dat hij een fartnite cup zal winnen.',
        ' wilt het spel spelen als hij kan spelen met zijn vrienden, maar wou nooit alleen spelen. Dan speelt hij iets anders met zijn vrienden of belt hij met meisjes omdat hij dat ook leuk vind.',
    ]
    fortniteanswer = random.choice(fortnite_quotes)
    embedVar = discord.Embed(
        title="Fortnite verslaving", description=ctx.message.author.mention + fortniteanswer, color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@bot.command(name='randomgif', help='Zoekt random gifs op giphy.')
async def magic_eight_ball(ctx):
    gif = await search_gifs('random')
    await ctx.send('Gif URL : ' + gif)

bot.run(TOKEN)
