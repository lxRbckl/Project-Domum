# Project Domum by Alex Arbuckle


# Import <
from suntime import Sun
#import RPi.GPIO as GPIO
from asyncio import sleep
from discord import Intents
from json import load, dump
from datetime import datetime
from discord.ext.commands import Bot

# >


# Declaration <
#GPIO.setmode(GPIO.board)
uid, lat, lon = '', 0, 0
domum = Bot(command_prefix = uid, intents = Intents.all())
token = ''

# >


async def jsonLoad():
    '''  '''

    with open('Domum.json', 'r') as fileVariable:

        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:

        dump(arg, fileVariable, indent = 4)


@domum.event
async def on_ready():
    '''  '''

    # Algorithm <
    while (True):

        dictVariable = await jsonLoad()
        for key in dictVariable.keys():

            if (dictVariable[key]['isManual'] == 'False'):

                # timeCurrent Variable <
                timeCurrent = str(datetime.now()).split()[1].split(':')
                timeCurrent = '{}{}'.format(int(timeCurrent[0]), timeCurrent[1])

                # >

                # Timer Check <
                if (dictVariable[key]['isTimer'] == 'True'):

                    timeOn = dictVariable[key]['timerOn']
                    timeOff = dictVariable[key]['timerOff']

                    # Condition Start <
                    if (timeCurrent == timeOn):

                        dictVariable[key]['isOnline'] = True

                    # >

                    # Condition End <
                    if (timeCurrent == timeOff):

                        dictVariable[key]['isOnline'] = False

                    # >

                # >

                # Solar Check <
                if (dictVariable[key]['isSolar'] == 'True'):

                    # timeSunset Variable <
                    timeSunset = str(Sun(lat, lon).get_sunset_time()).split()[1].split(':')
                    timeSunset = '{}{}'.format(((int(timeSunset[0]) + 7) % 12), timeSunset[1])

                    # >

                    # timeSunrise Variable <
                    timeSunrise = str(Sun(lat, lon).get_sunrise_time()).split()[1].split(':')
                    timeSunrise = '{}{}'.format(((int(timeSunrise[0]) + 7) % 12), timeSunrise[1])

                    # >

                    # Condition Sunset <
                    if (timeCurrent == timeSunset):

                        dictVariable[key]['isOnline'] = True

                    # >

                    # Condition Sunrise <
                    if (timeCurrent == timeSunrise):

                        dictVariable[key]['isOnline'] = False

                    # >

                # >

                #GPIO.output(dictVariable[key]['Pin'], dictVariable[key]['isOnline'])

            await jsonDump(dictVariable) if (await jsonLoad() != dictVariable) else (None)

            # >

        await sleep(30)

    # >


@domum.command()
async def setId(ctx, arg):
    ''' arg : str '''

    dictVariable = await jsonLoad()

    if (arg not in dictVariable.keys()):

        dictVariable[arg] = {'Pin' : "False",
                             'isSolar' : "False",
                             'isTimer' : "False",
                             'isManual' : "True",
                             'timerOn' : "False",
                             'timerOff' : "False",
                             'isOnline' : "False"}

        await ctx.channel.send(f'{arg} was created.', delete_after = 60)
        await jsonDump(dictVariable)

    else:

        await ctx.channel.send(f'{arg} already exists.', delete_after = 60)


@domum.command()
async def getId(ctx, arg):
    ''' arg : str '''

    dictVariable = await jsonLoad()

    if (arg in dictVariable.keys()):

        strVariable = '{}{}{}{}{}{}{}'.format('Pin : {}\n'.format(dictVariable[arg]['Pin']),
                                              'isSolar : {}\n'.format(dictVariable[arg]['isSolar']),
                                              'isTimer : {}\n'.format(dictVariable[arg]['isTimer']),
                                              'timerOn : {}\n'.format(dictVariable[arg]['timerOn']),
                                              'timerOff : {}\n'.format(dictVariable[arg]['timerOff']),
                                              'isManual : {}\n'.format(dictVariable[arg]['isManual']),
                                              'isOnline : {}\n'.format(dictVariable[arg]['isOnline']))

        await ctx.channel.send(f'```{arg}```', delete_after = 60)
        await ctx.channel.send(f'```{strVariable}```', delete_after = 60)

    else:

        await ctx.channel.send(f'{arg} does not exist', delete_after = 60)


@domum.command()
async def setPin(ctx, *args):
    ''' args[0] : str
        args[1] : int '''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        dictVariable[args[0]]['Pin'] = int(args[1])

        await ctx.channel.send(f'{args[0]} : Pin : {args[1]}', delete_after = 60)
        await jsonDump(dictVariable)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setManual(ctx, *args):
    ''' args[0] : str
        args[1] : bool '''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        dictVariable[args[0]]['isManual'] = args[1]

        await ctx.channel.send(f'{args[0]} : isManual : {args[1]}', delete_after = 60)
        await jsonDump(dictVariable)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setSolar(ctx, *args):
    ''' args[0] : str
        args[1] : bool '''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        dictVariable[args[0]]['isSolar'] = args[1]
        dictVariable[args[0]]['isTimer'] = 'False'
        dictVariable[args[0]]['isManual'] = 'False'

        await ctx.channel.send(f'{args[0]} : isSolar : {args[1]}', delete_after = 60)
        await jsonDump(dictVariable)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setTimer(ctx, *args):
    ''' args[0] : str
        args[1] : bool '''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        dictVariable[args[0]]['isTimer'] = args[1]
        dictVariable[args[0]]['isSolar'] = 'False'
        dictVariable[args[0]]['isManual'] = 'False'

        await ctx.channel.send(f'{args[0]} : isTimer : {args[1]}', delete_after = 60)
        await jsonDump(dictVariable)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setTimerOn(ctx, *args):
    ''' args[0] : str
        args[1] : str'''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        if (dictVariable[args[0]]['isTimer'] == 'True'):

            dictVariable[args[0]]['timerOn'] = args[1]

            await ctx.channel.send(f'{args[0]} : timerOn : {args[1]}', delete_after = 60)
            await jsonDump(dictVariable)

        else:

            await ctx.channel.send(f'isTimer for {args[0]} is False.', delete_after = 60)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setTimerOff(ctx, *args):
    ''' args[0] : str
        args[1] : str'''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        if (dictVariable[args[0]]['isTimer'] == 'True'):

            dictVariable[args[0]]['timerOff'] = args[1]

            await ctx.channel.send(f'{args[0]} : timerOff : {args[1]}', delete_after = 60)
            await jsonDump(dictVariable)

        else:

            await ctx.channel.send(f'isTimer for {args[0]} is False.', delete_after = 60)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


@domum.command()
async def setOnline(ctx, *args):
    ''' args[0] : str
        args[1] : bool'''

    dictVariable = await jsonLoad()

    if (args[0] in dictVariable.keys()):

        if (dictVariable[args[0]]['isManual'] == 'True'):

            dictVariable[args[0]]['isOnline'] = True if (args[1] == 'True') else (False)

            await ctx.channel.send(f'{args[0]} : isOnline : {args[1]}', delete_after = 60)
            await jsonDump(dictVariable)

        else:

            await ctx.channel.send(f'isManual for {args[0]} is False.', delete_after = 60)

    else:

        await ctx.channel.send(f'{args[0]} does not exist.', delete_after = 60)


domum.run(token)
