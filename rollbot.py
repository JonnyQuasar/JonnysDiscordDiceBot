import discord
import logging
import secrets

client = discord.Client()
TOKEN = 'NzQzNDM2ODMxMTgxMjQyNDc5.XzUpgA.awJrZM7H_2H2gJtt-sHRVOAkjvM'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
async def cut_string(message, cutting):
    length = len(message)
    new_message = message[cutting:length]
    return new_message
    
async def read_dice(msg): #msg == string split by whitespace; eg. "!roll", "1d6", "+4"
    #init
    num_dice = 0 # number of dice
    which_dice = 0 # what sort of dice
    sum_dice = 0 # the sum of the roll
    mod_dice = 0 # the modifier, if available
    modif_str = '' # the parsed string of the modifier
    dice_str = msg[1] # the parsed string of the roll
    # print(dice_str)
    
    if len(msg) > 2: #does the roll have a modifier?
        modif_str = msg[2]
    
    #check how many dice
    if dice_str[0].isdigit(): 
            if dice_str[1].isdigit(): # is number of dice >10?
                # print(dice_str[0:2]) # DEBUG
                num_dice = int(dice_str[0:2])
                dice_str = await cut_string(dice_str, 2) # remove from parsed string
            else:
                num_dice = int(dice_str[0])
                dice_str = await cut_string(dice_str, 1) #remove from parsed string
    elif dice_str[0] == 'd': #check if single dice
        num_dice = 1
    else: 
        return "Error!"
    
    # determine which dice to use
    if dice_str[0] == 'd':
        dice_str = await cut_string(dice_str, 1) # to 'pop' the 'd'
        if dice_str.isdigit: #check if only digits left
            which_dice = int(dice_str)
        else:
            return "Error!"
    
    # determine the modifier    
    if len(modif_str) != 0:
        if modif_str[0] == '+':
            modif_str = await cut_string(modif_str, 1)
            if modif_str.isdigit():
                mod_dice = int(modif_str)
            else:
                return "Error!"
        elif modif_str[0] == '-':
            modif_str = await cut_string(modif_str, 1)
            if modif_str.isdigit():
                mod_dice = int(modif_str) * (-1)
            else:
                return "Error!"
        else:
            return "Error!"
    
            
            
        
    which_dice -= 1
    
    # print("Debug: which_dice = " + str(which_dice)) # DEBUG
    # print("Debug: num_dice = " + str(num_dice)) # DEBUG
    # print("Debug: mod_dice = " + str(mod_dice)) # DEBUG
    
    for x in range(num_dice):
        sum_dice += secrets.randbelow(which_dice) + 1
    else:
        if mod_dice != 0:
            sum_dice += mod_dice
        return sum_dice

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!roll"):
        dice = message.content.split()
        if dice[1] == "d20" and len(dice) == 2: # rolls a d20
            tally = secrets.randbelow(19) + 1
            tally_msg = str(message.author) + ", you rolled a " + str(tally) + "!"
            await message.channel.send(tally_msg)
        else:
            result = await read_dice(dice)
            if result == "Error!":
                await message.channel.send(result)
            else:
                tally_msg = str(message.author) + ", you rolled a total of " + str(result) + "!"
                await message.channel.send(tally_msg)

client.run(TOKEN)