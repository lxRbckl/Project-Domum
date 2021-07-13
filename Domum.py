# Project Domum by Alex Arbuckle


import RPi.GPIO as GPIO
from asyncio import sleep
from discord import Intents
from json import load, dump
from discord.ext.commands import Bot


uid = ''
domum = Bot(command_prefix = uid, intents = Intents.all())
token = 'ODY0MzQwODI4ODc2NTcwNjQ2.YO0CIA.7z9MlDu5px2XgwCqX3xaBOQTMXk'


@domum.event
async def on_ready():
        
    GPIO.setmode(GPIO.BOARD)
    dictVariable = await jsonLoad()
    for value in dictVariable.values():
        
        GPIO.setup(value[1], True if (value[0] == 'On') else (False))
    
    while (True):
        
        for value in dictVariable.values():
            
            GPIO.output(value[1], True if (value[0] == 'On') else (False))
            
            dictVariable = await jsonLoad()
            await sleep(30)


async def jsonLoad():
    '''  '''

    with open('Domum.json', 'r') as fileVariable:
        
        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:
        
        dump(arg, fileVariable, indent=4)


@domum.command()
async def domumAddAdmin(ctx, arg):
    ''' arg : str '''

    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):
    
        dictVariable['Admin'].append(arg) if (arg not in dictVariable['Admin']) else (None)
        
        await jsonDump(dictVariable)
    

@domum.command()
async def domumRemoveAdmin(ctx, arg):
    ''' arg : str '''
   
    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):
    
        dictVariable['Admin'].remove(arg) if (arg in dictVariable['Admin']) else (None)
        
        await jsonDump(dictVariable)


@domum.command()
async def domumShowAdmin(ctx):
    '''  '''
    
    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):
    
        strVariable = ''.join('{}\n'.format(i) for i in dictVariable['Admin'])
        
        await ctx.channel.send(strVariable, delete_after = 60)
    

@domum.command(aliases = ['add', 'Add'])
async def domumAdd(ctx, *args):
    ''' args[0] : str
        args[1] : int '''
    
    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):
    
        dictVariable[args[0]] = ['Off', args[1], False]
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was added.'.format(args[0]), delete_after = 60)    


@domum.command(aliases = ['delete', 'Delete'])
async def domumDelete(ctx, arg):
    ''' arg : str '''
    
    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):
        
        del dictVariable[arg]
        
        await jsonDump(dictVariable)
        await ctx.channel.send('{} was removed.'.format(arg), delete_after = 60)


@domum.command(aliases = ['set', 'Set'])
async def domumSet(ctx, *args):
    ''' args[n] : str '''
    
    dictVariable = await jsonLoad()
    
    if (str(ctx.author) in dictVariable['Admin']):

        for arg in [i for i in dictVariable.keys()] if (args[1:] == []) else args[1:]:
        
            dictVariable[arg][0] = args[0].title() if (arg in dictVariable.keys()) else (None)
        
        await jsonDump(dictVariable)


domum.run(token)