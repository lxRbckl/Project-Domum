# Project Domum by Alex Arbuckle


'''#domum.run(token)
var = ctime().split()
print(var)'''

#mport RPi.GPIO as GPIO
from asyncio import sleep
from discord import Intents
from json import load, dump
from time import time, ctime
from discord.ext.commands import Bot


uid = ''
domum = Bot(command_prefix = uid, intents = Intents.all())
token = ''


'''@domum.event
async def on_ready():
            
    #GPIO.setmode(GPIO.BOARD)
    dictVariable = await jsonLoad()
    while (True):
        
        for value in dictVariable.values():
            
            #GPIO.output(value['Pin'], True if (value[0] == 'On') else (False))
    
        dictVariable = await jsonLoad()
        await sleep(15)'''


async def jsonLoad(): # *
    '''  '''

    with open('Domum.json', 'r') as fileVariable:
        
        return load(fileVariable)


async def jsonDump(arg): # *
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:
        
        dump(arg, fileVariable, indent = 4)


@domum.command(aliases = ['add', 'Add']) # *
async def domumAdd(ctx, *args):
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
    

@domum.command(aliases = ['delete', 'Delete']) # *
async def domumDelete(ctx, arg):
    ''' arg : str '''
    
    dictVariable = await jsonLoad()
    
    if (arg in dictVariable.keys()):
        
        del dictVariable[arg]
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was removed.'.format(arg), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist.'.format(arg), delete_after = 60)
        

@domum.command(aliases = ['set', 'Set']) # *
async def domumSet(ctx, *args):
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


@domum.command(aliases = ['add schedule', 'Add Schedule'])
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
        

@domum.command(aliases = ['delete schedule', 'Delete Schedule'])
async def domumDeleteSchedule(ctx, *args):
    ''' args[0] : str
        args[1] : int '''
    
    dictVariable = await jsonLoad()
    
    if (args[0] in dictVariable.keys()):
        
        dictVariable[args[0]]['Schedule'].pop(args[1])
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was removed from {}.'.format(args[1], args[0]), delete_after = 60)
    
    else:
        
        await ctx.channel.send('{} does not exist'.format(args[0]), delete_after = 60)


@domum.command(aliases = ['show schedule', 'Show Schedule'])
async def domumShowSchedule(ctx, arg):
    ''' arg : str '''
    
    dictVariable = await jsonLoad()
    
    if (arg in dictVariable.keys()):
        
        #strVariable = ''.join('{}\t{} {}'.format())
        # TODO
        # comprehension to join all scheduled times together
        # then move on incorporating them into the on_ready algorithm.
    
    else:
        
        await ctx.channel.send('{} does not exist.'.format(arg), delete_after = 60)