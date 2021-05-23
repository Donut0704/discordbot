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
ROLE2 = os.getenv('role2')
guild_name = os.getenv('GUILD_NAME')
guild_name2 = os.getenv('GUILD_NAME2')

# 2
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!k ',
                   guild_subscriptions=True, intents=intents)

# game variables

player1 = ""
player2 = ""
turn = ""
gameOver = True
bot1 = False
board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
# game variables2

player3 = ""
player4 = ""
turn2 = ""
gameOver2 = True
bot2 = False
board2 = []
# game variables3

player5 = ""
player6 = ""
turn3 = ""
gameOver3 = True
bot3 = False
board3 = []


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
        'Pasen komt eraan, ben je al op zoek naar je paaseitjes? Vergeet ze niet, als je er geen hebt, krijg je zelf geen paaseitjes.',
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
        role = ctx.guild.get_role(int(ROLE))
        await ctx.author.add_roles(role)
        await ctx.send(ctx.message.author.mention+', jij bent een loser! Waarom probeerde je deze command? Nu heb je de loser role.')
    elif ctx.message.guild.name == guild_name2:
        role2 = ctx.guild.get_role(int(ROLE2))
        await ctx.author.add_roles(role2)
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


@bot.command(name="rps", help="Speel het spel steen, papier, schaar")
async def rps(ctx):
    rpsGame = ['steen', 'papier', 'schaar']
    await ctx.send(f"Steen, papier of schaar? Neem een wijze keuze...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await bot.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'steen':
        if comp_choice == 'steen':
            await ctx.send(f'Nou, dat was raar. We eindigden gelijk.\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'papier':
            await ctx.send(f'Goed geprobeerd, maar deze keer heb ik gewonnen!!\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'schaar':
            await ctx.send(f"Aw, je hebt me verslaan. Dit gaat niet meer gebeuren!\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}")

    elif user_choice == 'papier':
        if comp_choice == 'steen':
            await ctx.send(f'Verslaat de pen het zwaard? Meer zoals het papier de rots verslaat !!\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'papier':
            await ctx.send(f'Oh, gek. We eindigden gelijk. Ik daag je uit voor een herkansing !!\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'schaar':
            await ctx.send(f"Ach man, het is je echt gelukt om me te verslaan.\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}")

    elif user_choice == 'schaar':
        if comp_choice == 'steen':
            await ctx.send(f'HAHA !! Ik heb je net verpletterd !! Ik heb steen !!\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'papier':
            await ctx.send(f'Bruh. >: |\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}')
        elif comp_choice == 'schaar':
            await ctx.send(f"Nou ja, we eindigden gelijk.\nJouw keuze: {user_choice}\nMijn keuze: {comp_choice}")

    else:
        await ctx.send("Gebruik schaar, papier, steen")


@bot.command(name="tictactoe", help="Het beroemde spel Tictactoe")
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    if ctx.message.guild.name == guild_name:
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            if str(player1) == "Bjarn#3726":
                turn = player2
                await ctx.send("Het is <@" + str(player2.id) + ">beurt.")

            elif str(player2) == "Bjarn#3726":
                turn = player1
                await ctx.send("Het is <@" + str(player1.id) + "> beurt.")

            else:
                # determine who goes first
                num = random.randint(1, 2)
                if num == 1:
                    turn = player1
                    await ctx.send("Het is <@" + str(player1.id) + "> beurt.")
                elif num == 2:
                    turn = player2
                    await ctx.send("Het is <@" + str(player2.id) + ">beurt.")
        else:
            await ctx.send("Een spel is nog bezig! Eindig deze eerst voordat je een nieuwe begint.")
    elif ctx.message.guild.name == guild_name2:
        global count2
        global player3
        global player4
        global turn2
        global gameOver2

        if gameOver2:
            global board2
            board2 = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn2 = ""
            gameOver2 = False
            count2 = 0

            player3 = p1
            player4 = p2

            # print the board
            line2 = ""
            for x in range(len(board2)):
                if x == 2 or x == 5 or x == 8:
                    line2 += " " + board2[x]
                    await ctx.send(line2)
                    line2 = ""
                else:
                    line2 += " " + board2[x]

            if str(player3) == "Bjarn#3726":
                turn2 = player4
                await ctx.send("Het is <@" + str(player4.id) + ">beurt.")

            elif str(player4) == "Bjarn#3726":
                turn2 = player3
                await ctx.send("Het is <@" + str(player3.id) + "> beurt.")

            else:
                # determine who goes first
                num2 = random.randint(1, 2)
                if num2 == 1:
                    turn2 = player3
                    await ctx.send("Het is <@" + str(player3.id) + "> beurt.")
                elif num2 == 2:
                    turn2 = player4
                    await ctx.send("Het is <@" + str(player4.id) + ">beurt.")
        else:
            await ctx.send("Een spel is nog bezig! Eindig deze eerst voordat je een nieuwe begint.")
    else:
        global count3
        global player5
        global player6
        global turn3
        global gameOver3

        if gameOver3:
            global board3
            board3 = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:",
                      ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn3 = ""
            gameOver3 = False
            count3 = 0

            player5 = p1
            player6 = p2
            # print the board
            line3 = ""
            for x in range(len(board3)):
                if x == 2 or x == 5 or x == 8:
                    line3 += " " + board3[x]
                    await ctx.send(line3)
                    line3 = ""
                else:
                    line3 += " " + board3[x]
            if str(player5) == "Bjarn#3726":
                turn3 = player6
                await ctx.send("Het is <@" + str(player6.id) + ">beurt.")

            elif str(player6) == "Bjarn#3726":
                turn3 = player5
                await ctx.send("Het is <@" + str(player5.id) + "> beurt.")

            else:
                # determine who goes first
                num3 = random.randint(1, 2)
                if num3 == 1:
                    turn3 = player5
                    await ctx.send("Het is <@" + str(player5.id) + "> beurt.")
                elif num3 == 2:
                    turn3 = player6
                    await ctx.send("Het is <@" + str(player6.id) + ">beurt.")
        else:
            await ctx.send("Een spel is nog bezig! Eindig deze eerst voordat je een nieuwe begint.")


@bot.command(name="place", help="Gebruik dit om jouw symbool te plaatsen bij het spel Tictactoe")
async def place(ctx, pos: int):
    if ctx.message.guild.name == guild_name:
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver
        global bot1

        if not gameOver:
            mark = ""
            if turn == ctx.author or bot1 == True:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]
                    # switch turns
                    if turn == player1:
                        turn = player2
                        bot1 = False
                        await ctx.send("Het is <@" + str(player2.id) + "> beurt.")
                    elif turn == player2:
                        turn = player1
                        bot1 = False
                        await ctx.send("Het is <@" + str(player1.id) + "> beurt.")

                    checkWinner(winningConditions, mark)
                    if gameOver == True:
                        bot1 = False
                        await ctx.send(mark + " wint! :partying_face:")
                    elif count >= 9:
                        bot1 = False
                        gameOver = True
                        await ctx.send("Het is gelijkspel!")

                    if str(turn) == "Bjarn#3726" and gameOver == False:
                        botsnumber1 = random.choice(range(1, 10))
                        while board[botsnumber1-1] != ":white_large_square:":
                            botsnumber1 = random.choice(range(1, 10))

                        if board[botsnumber1-1] == ":white_large_square:":
                            await ctx.send("!k place " + str(botsnumber1))
                            bot1 = True
                            await place(ctx, botsnumber1)

                else:
                    await ctx.send("Wees zeker een getal te kiezen tussen 1 en 9(inclusief) en een niet gemarkeerde tegel.")
            else:
                await ctx.send("Het is niet jouw beurt.")
        else:
            await ctx.send("Start alstublieft een nieuwe spel met de !k tictactoe command.")

    elif ctx.message.guild.name == guild_name2:
        global turn2
        global player3
        global player4
        global board2
        global count2
        global gameOver2
        global bot2

        if not gameOver2:
            mark2 = ""
            if turn2 == ctx.author or bot2 == True:
                if turn2 == player3:
                    mark2 = ":regional_indicator_x:"
                elif turn2 == player4:
                    mark2 = ":o2:"
                if 0 < pos < 10 and board2[pos - 1] == ":white_large_square:":
                    board2[pos - 1] = mark2
                    count2 += 1

                    # print the board
                    line2 = ""
                    for x in range(len(board2)):
                        if x == 2 or x == 5 or x == 8:
                            line2 += " " + board2[x]
                            await ctx.send(line2)
                            line2 = ""
                        else:
                            line2 += " " + board2[x]
                    # switch turns
                    if turn2 == player3:
                        turn2 = player4
                        bot2 = False
                        await ctx.send("Het is <@" + str(player4.id) + "> beurt.")
                    elif turn2 == player4:
                        turn2 = player3
                        bot2 = False
                        await ctx.send("Het is <@" + str(player3.id) + "> beurt.")

                    checkWinner2(winningConditions, mark2)
                    if gameOver2 == True:
                        bot2 = False
                        await ctx.send(mark2 + " wint! :partying_face:")
                    elif count2 >= 9:
                        gameOver2 = True
                        bot2 = False
                        await ctx.send("Het is gelijkspel!")

                    if str(turn2) == "Bjarn#3726" and gameOver2 == False:
                        botsnumber2 = random.choice(range(1, 10))
                        while board2[botsnumber2-1] != ":white_large_square:":
                            botsnumber2 = random.choice(range(1, 10))

                        if board2[botsnumber2-1] == ":white_large_square:":
                            await ctx.send("!k place " + str(botsnumber2))
                            bot2 = True
                            await place(ctx, botsnumber2)

                else:
                    await ctx.send("Wees zeker een getal te kiezen tussen 1 en 9(inclusief) en een niet gemarkeerde tegel.")
            else:
                await ctx.send("Het is niet jouw beurt.")
        else:
            await ctx.send("Start alstublieft een nieuwe spel met de !k tictactoe command.")

    else:
        global turn3
        global player5
        global player6
        global board3
        global count3
        global gameOver3
        global bot3

        if not gameOver3:
            mark3 = ""
            if turn3 == ctx.author or bot3 == True:
                if turn3 == player5:
                    mark3 = ":regional_indicator_x:"
                elif turn3 == player6:
                    mark3 = ":o2:"
                if 0 < pos < 10 and board3[pos - 1] == ":white_large_square:":
                    board3[pos - 1] = mark3
                    count3 += 1
                    # print the board
                    line3 = ""
                    for x in range(len(board3)):
                        if x == 2 or x == 5 or x == 8:
                            line3 += " " + board3[x]
                            await ctx.send(line3)
                            line3 = ""
                        else:
                            line3 += " " + board3[x]
                    # switch turns
                    if turn3 == player5:
                        turn3 = player6
                        bot3 = False
                        await ctx.send("Het is <@" + str(player6.id) + "> beurt.")
                    elif turn3 == player6:
                        turn3 = player5
                        bot3 = False
                        await ctx.send("Het is <@" + str(player5.id) + "> beurt.")

                    checkWinner3(winningConditions, mark3)
                    if gameOver3 == True:
                        await ctx.send(mark3 + " wint! :partying_face:")
                        bot3 = False
                    elif count3 >= 9:
                        gameOver3 = True
                        bot3 = False
                        await ctx.send("Het is gelijkspel!")

                    if str(turn3) == "Bjarn#3726" and gameOver3 == False:
                        botsnumber3 = random.choice(range(1, 10))
                        while board3[botsnumber3-1] != ":white_large_square:":
                            botsnumber3 = random.choice(range(1, 10))

                        if board3[botsnumber3-1] == ":white_large_square:":
                            await ctx.send("!k place " + str(botsnumber3))
                            bot3 = True
                            await place(ctx, botsnumber3)

                else:
                    await ctx.send("Wees zeker een getal te kiezen tussen 1 en 9(inclusief) en een niet gemarkeerde tegel.")
            else:
                await ctx.send("Het is niet jouw beurt.")
        else:
            await ctx.send("Start alstublieft een nieuwe spel met de !k tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


def checkWinner2(winningConditions, mark2):
    global gameOver2
    for condition in winningConditions:
        if board2[condition[0]] == mark2 and board2[condition[1]] == mark2 and board2[condition[2]] == mark2:
            gameOver2 = True


def checkWinner3(winningConditions, mark3):
    global gameOver3
    for condition in winningConditions:
        if board3[condition[0]] == mark3 and board3[condition[1]] == mark3 and board3[condition[2]] == mark3:
            gameOver3 = True


@ tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mention 2 spelers voor deze command alstublieft")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Wees zeker spelers te mentionen/pingen (bv. <@786996376802164776>), alstublieft.")


@ place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Voer alstublieft een positie in om deze te markeren, alstublieft.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Wees zeker een getal in te voeren, alstublieft.")


bot.run(TOKEN)
