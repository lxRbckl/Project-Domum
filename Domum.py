# Project Domum by Alex Arbuckle


from json import load, dump
from discord import utils, Intents
from discord.ext.commands import Bot


uid = ''
admin = ''
domum = Bot(command_prefix = uid, intents = Intents.all())
token = ''


async def jsonLoad():
    '''  '''

    with open('Domum.json', 'r') as fileVariable:
        
        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:
        
        dump(arg, fileVariable, indent=4)


@domum.command(aliases = ['+'])
async def domumAppend(*args):
    ''' args[0] : int
        args[1] : str '''
    
    dictVariable = jsonLoad()
    dictVariable[args[1]] = args[0]
    await jsonDump(dictVariable)
    

@domum.command(aliases = ['-'])
async def domumRemove(arg):
    ''' arg : str '''
    
    dictVariable = jsonLoad()
    del dictVariable[arg]
    await jsonDump(dictVariable)