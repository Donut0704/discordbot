# bot.py
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
import discord


# 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!k ',
                   guild_subscriptions=True, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='jouw problemen'))
    print(f'{bot.user.name} has connected to Discord!')


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
async def simp(ctx):
    simprate = random.choice(range(0, 101))
    if simprate > 0 and simprate < 30:
        answer = " heeft gelukkige tijden. Zelf gaat hij weinig om met jongens/meisjes. Ben je zeker gelukkig?"

    if simprate >= 30 and simprate <= 80:
        answer = ' is gezond en in evenwicht.'

    if simprate >= 80 and simprate <= 100:
        answer = 'is te druk bezig met zijn/haar liefdesleven. Ga eens om met je vrienden.'

    await ctx.send(ctx.message.author.mention + answer+" simprate: " + str(simprate) + "%")
bot.run(TOKEN)
