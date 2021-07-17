# Project Domum by Alex Arbuckle


'''#domum.run(token)
var = ctime().split()
print(var)'''

from suntime import Sun
#mport RPi.GPIO as GPIO
from asyncio import sleep
from discord import Intents
from json import load, dump
from datetime import datetime
from discord.ext.commands import Bot


uid = ''
lat, lon = 39, -94
domum = Bot(command_prefix = uid, intents = Intents.all())
token = 'ODY0MzQwODI4ODc2NTcwNjQ2.YO0CIA.jDnZsFDaAsTJP0QLjdR1JpgQf_A'


@domum.event
async def on_ready():
            
    #GPIO.setmode(GPIO.BOARD)
    while (True):

        dictVariable = await jsonLoad()
        for key in dictVariable.keys():

            timeCurrent = str(datetime.now()).split()[1].split(':')
            timeSunset = str(Sun(lat, lon).get_sunset_time()).split()[1].split(':')
            timeSunrise = str(Sun(lat, lon).get_sunrise_time()).split()[1].split(':')

            timeCurrent = '{}{}'.format(int(timeCurrent[0]), timeCurrent[1])
            timeSunset = '{}{}'.format(((int(timeSunset[0]) + 7) % 12), timeSunset[1])
            timeSunrise = '{}{}'.format(((int(timeSunrise[0]) + 7) % 12), timeSunrise[1])

            # Schedule #
            if (timeCurrent in dictVariable[key]['Schedule'].keys()):

                dictVariable[key]['Status'] = dictVariable[key]['Schedule'][timeCurrent]

            # Night Cycle # Sunset #
            if (timeCurrent == timeSunset):

                dictVariable[key]['Status'] = True

            # Night Cycle # Sunrise #
            if (timeCurrent == timeSunrise):

                dictVariable[key]['Status'] = False

            # Manual Cycle #
            #GIPO.output(value['Pin'], True if (value['Status'] == 'On') else (False))

        await sleep(15)


async def jsonLoad():
    '''  '''

    with open('Domum.json', 'r') as fileVariable:
        
        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:
        
        dump(arg, fileVariable, indent = 4)


@domum.command(aliases = ['addPin'])
async def domumAddPin(ctx, *args):
    ''' args[0] : str
        args[1] : int '''
    
    dictVariable = await jsonLoad()
    
    if (args[0] not in dictVariable.keys()):
        
        dictVariable[args[0]] = {'Status' : 'Off',
                                 'Schedule' : False,
                                 'Pin' : int(args[1])}
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was added.'.format(args[0]), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} already exists.'.format(args[0]), delete_after = 60)
    

@domum.command(aliases = ['deletePin'])
async def domumDeletePin(ctx, arg):
    ''' arg : str '''
    
    dictVariable = await jsonLoad()
    
    if (arg in dictVariable.keys()):
        
        del dictVariable[arg]
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was removed.'.format(arg), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist.'.format(arg), delete_after = 60)


@domum.command(aliases = ['showPin'])
async def domumShowPin(ctx, arg):
    ''' arg : str '''

    dictVariable = await jsonLoad()

    if (arg in dictVariable.keys()):

        strVariable = '{} : Pin : {}'.format(arg, dictVariable[arg]['Pin'])

        await ctx.channel.send(strVariable, delete_after = 60)

    else:

        await ctx.channel.send('{} does not exist.'.format(arg), delete_after = 60)
        

@domum.command(aliases = ['setPin'])
async def domumSetPin(ctx, *args):
    ''' args[n] : str
        args[-1] : str '''
    
    dictVariable = await jsonLoad()
    
    for arg in [i for i in dictVariable.keys()] if (args[1:] == []) else (args[1:]):
        
        if (arg in dictVariable.keys()):
        
            dictVariable[arg]['Status'] = args[-1].title()
            
            await jsonDump(dictVariable)
            await ctx.channel.send('{} : Status : {}'.format(arg, args[-1].title), delete_after = 60)
            
        else:
            
            await ctx.channel.send('{} does not exist'.format(arg), delete_after = 60)


@domum.command(aliases = ['addSchedule'])
async def domumAddSchedule(ctx, *args):
    ''' args[0] : str
        args[1] : bool | str
        args[2] :      | str '''
    
    dictVariable = await jsonLoad()
    
    if (args[0] in dictVariable.keys()):
        
        if (type(args[1]) == bool):
            
            dictVariable[args[0]]['Schedule'] = args[1]
        
        else:
        
            dictVariable[args[0]]['Schedule'].append({args[1] : True,
                                                      args[2] : False})
            
        await jsonDump(dictVariable)
        strVariable = ''.join('{} '.format(i) for i in args[1:])
        await ctx.channel.send('{} : Schedule : {}'.format(args[0], strVariable), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist.'.format(args[0]), delete_after = 60)
        

@domum.command(aliases = ['deleteSchedule'])
async def domumDeleteSchedule(ctx, *args):
    ''' args[0] : str
        args[1] : int '''
    
    dictVariable = await jsonLoad()
    
    if (args[0] in dictVariable.keys()):

        if (type(dictVariable[args[0]]['Schedule']) == bool):

            await ctx.channel.send('{} has no schedule.'.format(args[0]), delete_after = 60)

        else:
        
            dictVariable[args[0]]['Schedule'].pop(args[1])

            await jsonDump(dictVariable)
            await ctx.channel.send('{} was removed from {}.'.format(args[1], args[0]), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist'.format(args[0]), delete_after = 60)


@domum.command(aliases = ['showSchedule'])
async def domumShowSchedule(ctx, arg):
    ''' arg : str '''
    
    dictVariable = await jsonLoad()
    
    if (arg in dictVariable.keys()):

        if (type(dictVariable[arg]['Schedule']) == bool):

            strVariable = 'Night Cycle' if (dictVariable[arg]['Schedule'] == True) else ('Manual Cycle')

        else:

            strVariable = f'{arg}\n\n'
            strVariable += ''.join(f'{c}\t{i[0]} {i[1]}' for c, i in enumerate(dictVariable[arg]['Schedule']))

        await ctx.channel.send(strVariable, delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist.'.format(arg), delete_after = 60)


domum.run(token)
