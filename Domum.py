# Project Domum by Alex Arbuckle


from json import load, dump
from discord import utils, Intents
from discord.ext.commands import Bot


uid = 'Office'
admin = 'Germx5000#5554'
domum = Bot(command_prefix = uid, intents = Intents.all())
token = 'ODY0MzQwODI4ODc2NTcwNjQ2.YO0CIA.ED7hjdd4-BDYvgnW2Hg1WX_lMOk'


async def jsonLoad():
    '''  '''

    with open('Domum.json', 'r') as fileVariable:
        
        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('Domum.json', 'w') as fileVariable:
        
        dump(arg, fileVariable, indent=4)


@domum.command(aliases = ['+'])
async def domumAppend(ctx, *args):
    ''' args[0] : int
        args[1] : str '''
    
    # load JSON
    dictVariable = jsonLoad()
    
    # append
    dictVariable[args[1]] = {'Status' : True,
                             'Name' : args[0],
                             'Schedule' : False}
    
    # update JSON
    await jsonDump(dictVariable)
    

@domum.command(aliases = ['-'])
async def domumRemove(ctx, arg):
    ''' arg : str '''
    
    # load JSON
    dictVariable = jsonLoad()
    
    # remove
    del dictVariable[arg]
    
    # update JSON
    await jsonDump(dictVariable)


@domum.command(aliases = [])
async def domumOn(ctx, *args):
    '''  '''
    
    # load JSON
    dictVariable = await jsonLoad()
    
    
    

@domum.command(aliases = [])
async def domumOff(ctx, *args):
    '''  '''
    
    # load JSON
    dictVariable = await jsonLoad()
    
    
    

@domum.command(aliases = [])
async def domumRestart(ctx, *args):
    '''  '''
    
    # load JSON
    dictVariable = await jsonLoad()
    
    
    
    

domum.run(token)