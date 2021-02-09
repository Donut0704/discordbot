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
CHAT_CHANNEL = os.getenv('chat_channel')
RULES_CHANNEL = os.getenv('rules_channel')
LINK = os.getenv('link')
ROLE = os.getenv('role')
guild_name = os.getenv('GUILD_NAME')

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
    if member.guild.name == guild_name:
        await member.create_dm()
        await member.dm_channel.send(
            f''' Hey {member.name} ,  welcome to my server. My name is Bjarn and I am the king here. 
                I\'m sure you will respect the rules. Don't forget to read them. 
                Together with my moderators I will try to make the best server. 
                I hope you will enjoy your time here. 
                Greetings your king
                Bjarn & CO'
                '''
        )
    else:
        await member.create_dm()
        await member.dm_channel.send(
            f'Hey {member.name} ,  welkom in onze server. Ik hoop dat je veel plezier beleeft.'
        )


@bot.event
async def on_member_remove(member):
    if member.guild.name == guild_name:
        channel = bot.get_channel(int(CHAT_CHANNEL))
        embedVar = discord.Embed(
            title="Player left", description=member.mention+', heeft net de server verlaten, wat een loser.'
            + ' Hij zal nu een slecht leven hebben. Hij zal de hele dag huilen omdat hij deze fout heeft gemaakt'
            + ' Ik hoop dat hij voor hem blijft leven en dat hij misschien de uitnodigingslink krijgt. Dat was het', color=0xF1F014)
        await channel.send(embed=embedVar)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    rythm_quotes = [
        'Good job Rythm!',
        'Je bent de beste Rythm',
        'Toffe muziek Rythm'
    ]
    if message.content.startswith('!p'):
        response = random.choice(rythm_quotes)
        await message.channel.send(response)


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


@ bot.command(name='99', help='Reageert met een random zin van Brooklyn 99.')
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


@bot.command(name='simp', help='Zegt hoe simp je bent.')
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


@bot.command(name='Bjarnismyking', help='Zegt jou wie de koning is.')
async def bjarnismyking(ctx):
    await ctx.send(ctx.message.author.mention + " je weet toch wel wie de baas is hier.")


@bot.command(name='Bjarn', help="Zegt random zinnen.")
async def Bjarn(ctx):
    bjarn_quotes = [
        'Kerst komt eraan, ben je al op zoek naar je cadeautjes? Vergeet ze niet, als je er geen hebt, krijg je zelf geen cadeautjes.',
        'Jouw koning is toegekomen.',
        'Hoe is je dag?',
        'Ja'
    ]
    antwoord = random.choice(bjarn_quotes)
    await ctx.send(antwoord)


@bot.command(name='gay', help="Zegt hoe gay je bent.")
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
        ' is verslaafd aan fortnite maar aan het hoogste level. Hij spendeert de hele dag een deze game, terwijl zijn vrienden Minecraft samenspelen en fun hebben. Hij denkt zelfs dat hij een fortnite cup zal winnen.',
        ' wilt het spel spelen als hij het kan spelen met zijn vrienden, maar wou nooitt alleen spelen. Anders speelt hij iets anders met zijn vrienden of belt hij met meisjes omdat hij dat ook leuk vind.',
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
        ' heeft het spel nooit gewild dat het spel bestond en zal het nooit spelen. Hij denkt dat het een schaamte is voor de hele gamingworld.',
        ' is verslaafd aan fortnite maar aan het hoogste level. Hij spendeert de hele dag een deze game, terwijl zijn vrienden Minecraft samenspelen en fun hebben. Hij denkt zelfs dat hij een fortnite cup zal winnen.',
        ' wilt het spel spelen als hij het kan spelen met zijn vrienden, maar wou nooit alleen spelen. Anders speelt hij iets anders met zijn vrienden of belt hij met meisjes omdat hij dat ook leuk vind.',
    ]
    fortniteanswer = random.choice(fortnite_quotes)
    embedVar = discord.Embed(
        title="Fortnite verslaving", description=ctx.message.author.mention + fortniteanswer, color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@bot.command(name='randomgif', help='Zoekt random gifs op giphy.')
async def randomgif(ctx):
    gif = await search_gifs('random')
    await ctx.send('Gif URL : ' + gif)


@bot.command(name='score', help='Geeft server score weer.')
async def score(ctx):
    score = random.choice(range(0, 101))
    embedVar = discord.Embed(
        title="Momentele server score", description=ctx.message.author.mention+" ,jouw server score is: "+str(score) + "%", color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@bot.command(name='sortinghat', help='Zegt in welke Zweinstein afdeling bent.')
async def sortinghat(ctx, user: discord.Member):
    hat_quotes = [
        'Deze was een moeilijke.',
        'Ah, die familie ken ik.',
    ]
    sorting_quotes = [
        'GRIFFOENDOR!',
        'ZWADDERICH!',
        'HUFFELPUF!',
        'RAVENKLAUW!'
    ]

    titel = random.choice(hat_quotes)
    sorting = random.choice(sorting_quotes)
    if sorting == 'GRIFFOENDOR!':
        embedVar = discord.Embed(
            title=titel, description=user.mention+" , jij bent: "+sorting, color=0xF72006)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'ZWADDERICH!':
        embedVar = discord.Embed(
            title=titel, description=user.mention+" , jij bent: "+sorting, color=0x24CD1D)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'HUFFELPUF!':
        embedVar = discord.Embed(
            title=titel, description=user.mention+" , jij bent: "+sorting, color=0xFBFA00)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'RAVENKLAUW!':
        embedVar = discord.Embed(
            title=titel, description=user.mention+" , jij bent: "+sorting, color=0x0061FB)
        await ctx.channel.send(embed=embedVar)


@sortinghat.error
async def on_command_error(ctx, error):
    hat_quotes = [
        'Deze was een moeilijke.',
        'Ah, die familie ken ik.',
    ]
    sorting_quotes = [
        'GRIFFOENDOR!',
        'ZWADDERICH!',
        'HUFFELPUF!',
        'RAVENKLAUW!'
    ]

    titel = random.choice(hat_quotes)
    sorting = random.choice(sorting_quotes)
    if sorting == 'GRIFFOENDOR!':
        embedVar = discord.Embed(
            title=titel, description=ctx.message.author.mention+" , jij bent: "+sorting, color=0xF72006)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'ZWADDERICH!':
        embedVar = discord.Embed(
            title=titel, description=ctx.message.author.mention+" , jij bent: "+sorting, color=0x24CD1D)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'HUFFELPUF!':
        embedVar = discord.Embed(
            title=titel, description=ctx.message.author.mention+" , jij bent: "+sorting, color=0xFBFA00)
        await ctx.channel.send(embed=embedVar)

    if sorting == 'RAVENKLAUW!':
        embedVar = discord.Embed(
            title=titel, description=ctx.message.author.mention+" , jij bent: "+sorting, color=0x0061FB)
        await ctx.channel.send(embed=embedVar)


@bot.command(name='sus', help='Verdenk anderen hiermee.')
async def sus(ctx, user: discord.Member):
    sus_quotes = [
        ' is totaal niet sus. Wat ben je aan het denken ,gast. Hij is de meest zachtaardigste persoon in de wereld. Hij kan niet eens liegen.',
        ' kan sus zijn, maar ik denk van niet.',
        ' vertrouw hem niet. Hij doet alleen wat goed is voor hem.',
        ' is kinda sus.',
        ' kan alleen sus zijn in Among Us.',
        ' gaat je binnenkort verraden. Hij is nogal sus.',
        ' ziet er misschien sus, maar dat is juist maar omdat hij snel gestrest is.'
    ]
    susanswer = random.choice(sus_quotes)
    embedVar = discord.Embed(
        title='Sus rate', description=user.mention + susanswer, color=0xF1F014)
    await ctx.channel.send(embed=embedVar)


@sus.error
async def on_command_error(ctx, error):
    await ctx.channel.send(ctx.message.author.mention + ", je kunt toch niet jezelf verdenken?")


@bot.command(name='link', help='Creëert een link ')
async def create_invite(ctx):
    if ctx.message.guild.name == guild_name:
        await ctx.send(LINK)
    else:
        newlink = await ctx.channel.create_invite(max_age=300)
        await ctx.send(newlink)


@bot.command(name='rules', help='De regels.')
async def rules(ctx):
    if ctx.message.guild.name == guild_name:
        embedVar = discord.Embed(
            title='The rules', description="Je kunt de regels vinden in <#"+RULES_CHANNEL+">. Vergeet niet te checken.", color=0xF1F014)
        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(
            title='The rules', description="Er zijn geen regels luister gewoon naar elkaar. Wat dacht je misschien, dat we in een strenge server zaten?", color=0xF1F014)
        await ctx.channel.send(embed=embedVar)


@bot.command(name='loser', help='Een toffe command.')
async def newrole(ctx):
    if ctx.message.guild.name == guild_name:
        await ctx.send('test')
        role = ctx.guild.get_role(int(ROLE))
        await ctx.author.add_roles(role)
        await ctx.send(ctx.message.author.mention+', jij bent een loser! Waarom probeerde je deze command? Nu heb je de loser role.')
    else:
        role = await ctx.guild.create_role(name='Loser', colour=discord.Colour(0xFB00F3), mentionable=True)
        await ctx.author.add_roles(role)
        await ctx.send(ctx.message.author.mention+', jij bent een loser! Waarom probeerde je deze command? Nu heb je de loser role.')


@bot.command(name='execute', help='iemand executeren')
async def execute(ctx, user: discord.Member):
    executeanswer = random.choice(range(0, 2))
    if executeanswer == 1:
        await ctx.send(user.mention+' is een goed persoon.  Ik kan dit niet tolereren.\n \n' +
                       ctx.message.author.mention + ' is gearresteerd door de poltie')
    else:
        await ctx.send(user.mention+' zal binnenkort worden uitgevoerd. Ik maak de elektrische stoel al klaar.')


@execute.error
async def on_command_error(ctx, error):
    executeanswer = random.choice(range(0, 2))
    if executeanswer == 1:
        await ctx.send(' is een goed persoon.  Ik kan dit niet tolereren.\n \n' +
                       ctx.message.author.mention + ' is gearresteerd door de poltie')
    else:
        await ctx.send(' will be executed soon. I am making the electric chair ready.')


@bot.command(name='mortsmortre', help='Roep de duitsere teken op.')
async def mortsmortre(ctx):
    embedVar = discord.Embed(
        title="Dark sign", description=ctx.message.author.mention+" heeft de duistere teken opgeroept.", color=0xCD4118)
    await ctx.channel.send(embed=embedVar)


@bot.command(name='Avadakedavra', help='Vermoord iemand met deze spreuk.')
async def Avadakedavra(ctx, user: discord.Member):
    avadaeanswer = random.choice(range(0, 2))
    if avadaeanswer == 0:
        embedVar = discord.Embed(
            title="Avada Kedavra", description=ctx.message.author.mention+" vermoordde "+user.mention+" met de doodsvloek. Jij vuile dooddoener. Voldemort is alang dood.", color=0x24CD1D)
        await ctx.channel.send(embed=embedVar)
    if avadaeanswer == 1:
        embedVar = discord.Embed(
            title="Avada Kedavra", description=ctx.message.author.mention+" probeerde "+user.mention+" te vermoorden, maar vergat dat zijn stok kapot was en blies zijn hand op.", color=0x24CD1D)
        await ctx.channel.send(embed=embedVar)


@Avadakedavra.error
async def on_command_error(ctx, error):
    embedVar = discord.Embed(
        title="Avada Kedavra", description=ctx.message.author.mention+" probeerde te vermoorden, maar vergat dat zijn stok kapot was en blies zijn hand op.", color=0x24CD1D)
    await ctx.channel.send(embed=embedVar)


bot.run(TOKEN)
