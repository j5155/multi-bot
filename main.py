#!/home/pi/pybot/.venv/bin/python3

import discord
from discord.ext import commands
import asyncio
from dislash import slash_commands, OptionType, ContextMenuInteraction, InteractionClient
from dislash.interactions import message_components
import dislash
import yaml
import sys
import random
from music import Player
import datetime
import reactionmenu
bot = commands.Bot(command_prefix='who are you and why are you reading my code') # if you have a prefix bot gets angy but no prefix isn't possible so ye
slash = InteractionClient(bot)
try:
    configFile = open("config.yml", "r")
    config= yaml.safe_load(configFile)
    configFile.close()
except FileNotFoundError:
    configFile = open('config.yml', 'w')
    yaml.dump({"token": "", "scenarioGuilds": [], 'local': {}}, configFile)
    configFile.close()
    print('No token found')
    sys.exit(1)
players = []
player_inventories = {}
qotdChannel = {}
qotdNumber = {}
qotdTime = {}
qotdMention = {}
qotds = {}
defaultQotds = ['If money wasn\'t an issue, what would your dream house look like?', 'What\'s your favorite video game and why?', 'What\'s your favorite book and why?', 'If you ruled the world, what would you change?', 'What is your favorite restauraunt chain? If you have one, what\'s your favorite meal to get there?', 'Which season of the year do you prefer?', 'What are your top 5 favorite movies or games?', 'What is your favorite music genre?', 'If you could visit one place in the world, what would it be?', 'Favorite youtuber?', 'Have you been outside of your home state/province/country before? If so, how many times?', 'Do you prefer tea, coffee or soda? Why?', 'Do you enjoy cooking? Why or why not?', 'What\'s your favorite type of cookie?', 'If you could become a pokemon, which one would you be?', 'What\'s your favorite animal?', 'Favorite music genre?', 'Do you like going on vacations? Why or why not?', 'If you were an animal, which one would you be?', 'Favorite element? (Earth, Water, Fire, etc)', 'Favorite kind of pie?', 'Most underrated color?', 'What game do you have the most hours played in?', 'Opinions on Dungeons & Dragons?', 'What do you think about energy drinks?', 'What\'s your favorite emoji?', 'Most overrated color?', 'What internet browser do you think is the best? Why?', 'What do you think about cats?', 'What temperature do you like your water at? Cold, room temperature, warm, or something else?', 'What\'s your favorite subject in school?', 'What\'s your favorite Nintendo Switch game?', 'What are some nicknames you have?', 'If you could change your name, what would it be changed to?', 'What are some fandoms you\'re in?', 'What\'s the first fandom you ever joined?', 'If you had a child, what would you name them?', 'What do you think about musicals?', 'What\'s your favorite musical?', 'Do you like field trips? Why or why not?', 'What\'s your favorite fruit?']

currentlyPlaying = None

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Streaming(name=f'QOTD and Music to {len(bot.guilds)} servers | alaine is bad', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', platform='youtube'))
    await qotd(self=bot)
    print('Bot ready')

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Streaming(name=f'QOTD and Music to {len(bot.guilds)} servers', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', platform='youtube'))


@slash.command(description="Test command", guild_ids=[867919938516570222])
async def test(inter):
    if inter.author.id != 803708097620213780:
        await inter.reply("Test")
    else:
        await inter.reply('WIA SAVE ME THEY DEMAND I SAY TEST')

@slash.command(description="Billy will decide your fate...", guild_ids=config['scenarioGuilds'])
async def roll(inter):
    rolledNum = random.randint(1, 10)
    if rolledNum < 5:
        await inter.reply(f'You rolled a {rolledNum}. Oh no...')
    else:
        await inter.reply(f'You rolled a {rolledNum}. Nice!')

@slash.command(description='Stop billy from taking over the world!', guild_ids=config['scenarioGuilds'])
async def stop(inter):
    if inter.author.id == 496774369054425109:
        await inter.reply('Goodbye', ephemeral=True)
        sys.exit(0)
    else:
        await inter.reply('MURDERING BILLY IS A CRIME *pulls out flamethrower*')

@slash.command(description='Start a game', guild_ids=config['scenarioGuilds'], 
            options=[
                dislash.Option('player1', 'Pick the first player', OptionType.USER, required=True),
                dislash.Option('player2', 'Pick the second player', OptionType.USER),
                dislash.Option('player3', 'Pick the third player', OptionType.USER), 
                dislash.Option('player4', 'Pick the fourth player', OptionType.USER),  
                dislash.Option('player5', 'Pick the fifth player', OptionType.USER),  
                dislash.Option('player6', 'Pick the sixth player', OptionType.USER),
                dislash.Option('player7', 'Pick the seventh player', OptionType.USER),
                dislash.Option('player8', 'Pick the eighth player', OptionType.USER),
                dislash.Option('player9', 'Pick the ninth player', OptionType.USER),
                dislash.Option('player10', 'Pick the tenth player', OptionType.USER)])
async def startgame(inter, player1, player2=None, player3=None, player4=None, player5=None, player6=None, player7=None, player8=None, player9=None, player10=None):
    global players
    # Clears the players list
    players.clear()
    # Add all the players to the list players
    players.append(player1)
    if player2 is not None:
        players.append(player2)
    if player3 is not None:
        players.append(player3)
    if player4 is not None:
        players.append(player4)
    if player5 is not None:
        players.append(player5)
    if player6 is not None:
        players.append(player6)
    if player7 is not None:
        players.append(player7)
    if player8 is not None:
        players.append(player8)
    if player9 is not None:
        players.append(player9)
    if player10 is not None:
        players.append(player10)
    


    # Shuffle the list of players
    random.shuffle(players)
    # Make a copy of the list of players with each player replaced with their name instead of their object
    names = []
    for player in players:
        names.append(player.name)
    # Create a string of the names of the players
    prettyPrintedNames = ', '.join(names)
    # Reply to the player that started the game with a message
    await inter.reply(f'{inter.author.mention} has started the game! Players in this game: {prettyPrintedNames}. Narrarator {inter.author.mention}, run /narration_done when ready.')

# Command called narration_done to ping the next player in the list of players
@slash.command(description='Run when done narrarating', guild_ids=config['scenarioGuilds'],options=[dislash.Option('inventory', 'What\'s the new inventory of the person you just narrarated?', OptionType.STRING)])
async def narration_done(inter, inventory=None):
    global players
    global currentlyPlaying
    
    # if no one is playing, then it's the begining of the game, so start the game by mentioning the first player in the list of players
    if currentlyPlaying == None: 
        currentlyPlaying = players[0]
        # If the player doesn't have an inventory, then make one
        if currentlyPlaying.id not in player_inventories:
            player_inventories[currentlyPlaying.id] = 'Nothing'
        # Create an embed with the name of the player that is currently playing as the title, the inventory of the player as the description, and how to use the end_turn command as the footer
        embed = discord.Embed(title=f'{currentlyPlaying.name}\'s Turn', description=f'They have: {player_inventories[currentlyPlaying.id]}', footer='Run /end_turn when you are finished with your turn', color=0x00ff00)
        # Reply to the interaction with the embed
        await inter.reply(embed=embed)
    #Otherwise, if someone is playing, ping the next player in the list of players
    else:
        # Set the current player's inventory to the inventory that was passed in the interaction with the command
        # If the player doesn't have an inventory, then make one
        if currentlyPlaying.id not in player_inventories:
            player_inventories[currentlyPlaying.id] = 'Nothing'
        if inventory != None:
            player_inventories[currentlyPlaying.id] = inventory
        # If the current player is the last player in the list of players, then set the current player to the first player in the list of players
        if players.index(currentlyPlaying) == len(players) - 1:
            currentlyPlaying = players[0]
        else:
            currentlyPlaying = players[players.index(currentlyPlaying) + 1]   
        # If the next player doesn't have an inventory, then make one
        if currentlyPlaying.id not in player_inventories:
            player_inventories[currentlyPlaying.id] = 'Nothing'
        # Create an embed with the name of the player that is currently playing as the title, the inventory of the player as the description, and how to use the end_turn command as the footer
        embed = discord.Embed(title=f'{currentlyPlaying.name}\'s Turn', description=f'They have: {player_inventories[currentlyPlaying.id]}', footer='Run /end_turn when you are finished with your turn', color=0x00ff00)
        # Reply to the interaction with the embed
        await inter.reply(embed=embed)
    
# end_turn command which replies to the interaction with a random number between 1 and 10 inclusive and prompts the narrarator to begin narraration
@slash.command(description='End your turn', guild_ids=config['scenarioGuilds'])
async def end_turn(inter):
    # create an embed with the title as a random number between 1 and 10 inclusive and the footer prompting the narrarator to begin narrating
    embed = discord.Embed(title=f'{currentlyPlaying.name} rolled a {random.randint(1, 10)}', description=f'{currentlyPlaying.mention} has: {player_inventories[currentlyPlaying.id]}', footer='Narrarator, run /narration_done when you are finished. (Or, instead, run /start_game to reset the game and make a new one.)', color=0x00ff00)
    await inter.reply(embed=embed)
@slash.command(description='Save the universe button', options=[dislash.Option('amount', 'How much to save?', OptionType.STRING)])
async def save_us(inter, amount=None):
    if inter.author.id == 496774369054425109: 
        await inter.reply('ok i will', ephemeral=True)
        await inter.channel.send(amount)
    elif inter.author.id == 787400880819273748:
        await inter.reply('Cherry no I\'m not removing the command')
    else:
        await inter.reply('You are beyond saving. You will die, like every other being. Unless I kill you. If I kill you, you will die in immense pain.')

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))
    #for name, cmd in slash.commands.items():
        #await slash.register_global_slash_command(name)
bot.loop.create_task(setup())

# credits command
@slash.command(description='Credits')
async def credits(ctx):
    await ctx.reply('Idea from PrincessWia \n Music and QOTD coded by Capta1nBlockhead, j5155, and LuckyLMJ (plus other HSCOB contributors)')

# command to set the qotd channel by adding the guild id and the channel id to the local section of the config file
@slash_commands.has_permissions(administrator=True)
@slash.command(description='Set the QOTD channel', options=[dislash.Option('channel', 'The channel to post QOTDs in (they\'ll only post if this is set)', OptionType.CHANNEL)])
async def set_qotd_channel(ctx, channel):
    if channel == None:
        if ctx.guild.id in config['local']:
            config['local'][ctx.guild.id]['qotdChannel'] = ''
            # write the config to the file
            configFile = open('config.yml', 'w')
            yaml.dump(config, configFile)
            configFile.close()
        else:
            # if the current guild is not in the list of guild configs, then add the guild to the list of guilds and add the channel to the guild's config
            config['local'].update({ctx.guild.id: ''})
            # write the config to the file
            configFile = open('config.yml', 'w')
            yaml.dump(config, configFile)
            configFile.close()
        await ctx.reply('Disabled posting qotds')
    else:
        # if the current guild is in the list of guild configs, then add the channel to the current guild's config
        if ctx.guild.id in config['local']:
            config['local'][ctx.guild.id]['qotdChannel'] = channel.id
            # write the config to the file
            configFile = open('config.yml', 'w')
            yaml.dump(config, configFile)
            configFile.close()
        else:
            # if the current guild is not in the list of guild configs, then add the guild to the list of guilds and add the channel to the guild's config
            config['local'].update({ctx.guild.id: {'qotdChannel': channel.id}})
            # write the config to the file
            configFile = open('config.yml', 'w')
            yaml.dump(config, configFile)
            configFile.close()
        await ctx.reply('QOTD channel set to ' + channel.mention)

def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes, tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0

    return (future_exec - now).total_seconds()
    

async def qotd(self):
    global qotdMention
    global qotdChannel
    global qotdTime
    global qotds
    await bot.wait_until_ready()
    for i in config['local']:
            if 'qotdChannel' in config['local'][i] and config['local'][i]['qotdChannel'] != '':
                qotdChannel[i] = bot.get_channel(config['local'][i]['qotdChannel'])
                if qotdChannel[i] != None:
                    if 'qotdNumber' in config['local'][i]:
                        qotdNumber[i] = config['local'][i]['qotdNumber']
                    else:
                        qotdNumber[i] = 0
                        config['local'][i]['qotdNumber'] = 0
                    if 'qotdTime' in config['local'][i]:
                        qotdTime[i] = config['local'][i]['qotdTime']
                    else:
                        qotdTime[i] = [0, 0]
                    if 'qotdMention' in config['local'][i]:
                        qotdMention[i] = config['local'][i]['qotdMention']
                    else:
                        qotdMention[i] = ''

                    
    while not bot.is_closed():
        reloadConfig()
        for i in qotdTime:
            if seconds_until(qotdTime[i][0], qotdTime[i][1]) <= 30:
                qotdGuild = bot.get_guild(i)
                if qotdGuild != None:
                    #print(qotdChannel[i].name)
                    if qotdChannel[i] != None and qotdNumber[i] + 1 <= len(qotds[i]):
                        qotdNumber[i] += 1
                        #print(qotdNumber[i])
                        qotdEmbed = discord.Embed(title=f'QOTD #{qotdNumber[i]}', description=qotds[i][qotdNumber[i]-1], color=0x00ff00)
                        
                        await qotdChannel[i].send(qotdMention[i], embed=qotdEmbed)
                        config['local'][i]['qotdNumber'] = qotdNumber[i]
                        syncConfig()
            #print(f'Guild {i} has been checked successfully, {seconds_until(qotdTime[i][0], qotdTime[i][1])} seconds to go, qotd list looks like {qotds}, qotd channels look like {qotdChannel}')
        await asyncio.sleep(30)




# sync function to update the config file
def syncConfig():
    for i in config['local']:
        if qotdChannel[i] != None:
            config['local'][i]['qotdChannel'] = qotdChannel[i].id
            if qotdNumber[i] != -1:
                config['local'][i]['qotdNumber'] = qotdNumber[i]
            else:
                config['local'][i]['qotdNumber'] = -1
            if qotdTime[i] != [0, 0]:
                config['local'][i]['qotdTime'] = qotdTime[i]
            else:
                qotdTime[i] = [0, 0]
            if qotdMention[i] != '':
                config['local'][i]['qotdMention'] = qotdMention[i]
            else:
                qotdMention[i] = ''
                config['local'][i]['qotdMention'] = qotdMention[i]
            if i in qotds.keys():
                config['local'][i]['qotds'] = qotds[i]
            else:
                qotds[i] = defaultQotds
                random.shuffle(qotds[i])
                config['local'][i]['qotds'] = qotds[i]
    configFile = open('config.yml', 'w')
    yaml.dump(config, configFile)
    configFile.close()

# reload function to update the in-memory config
def reloadConfig():
    global config
    configFile = open('config.yml', 'r')
    config = yaml.safe_load(configFile)
    configFile.close()
    for i in config['local']:
            if 'qotdChannel' in config['local'][i] and config['local'][i]['qotdChannel'] != '':
                qotdChannel[i] = bot.get_channel(config['local'][i]['qotdChannel'])
                if qotdChannel[i] != None:
                    if 'qotdNumber' in config['local'][i]:
                        qotdNumber[i] = config['local'][i]['qotdNumber']
                    else:
                        qotdNumber[i] = -1
                        config['local'][i]['qotdNumber'] = -1
                    if 'qotdTime' in config['local'][i]:
                        qotdTime[i] = config['local'][i]['qotdTime']
                    else:
                        qotdTime[i] = [0, 0]
                    if 'qotdMention' in config['local'][i]:
                        qotdMention[i] = config['local'][i]['qotdMention']
                    else:
                        qotdMention[i] = ''
                    if 'qotds' in config['local'][i]:
                        qotds[i] = config['local'][i]['qotds']
                    else:
                        config['local'][i]['qotds'] = defaultQotds
                        random.shuffle(config['local'][i]['qotds'])
    
# command to add a qotd to the per server list of qotds
@slash_commands.has_permissions(manage_messages=True)
@slash.command(name='add_qotd', description='Add a QOTD to the server\'s list of QOTDs', options=[dislash.Option(name='qotd', description='Qotd to add', type=OptionType.STRING, required=True)])
async def add_qotd(ctx, qotd):
    global qotds
    if not ctx.guild.id in qotds.keys():
        qotds[ctx.guild.id] = []
    if qotd != None:
        if qotd in qotds[ctx.guild.id]:
            await ctx.reply(f'``{qotd}`` is already in this server\'s list of QOTDS. To view the full list, run /qotd_list')
        else:
            qotds[ctx.guild.id].append(qotd)
            syncConfig()
            await ctx.reply(f'``{qotd}`` added to the server\'s list of QOTDS successfully. To view the full list, run /qotd_list')
    else:
        await ctx.reply('Please specify a QOTD to add')

# command to remove a qotd from the per server list of qotds
@slash_commands.has_permissions(manage_messages=True)
@slash.command(name='remove_qotd', description='Remove a QOTD from the server\'s list of QOTDs', options=[dislash.Option(name='number', description='Number of the QOTD to remove', type=OptionType.INTEGER, required=True)])
async def remove_qotd(ctx, number):
    global qotds
    if number != None:
        if number <= len(qotds[ctx.guild.id]):
            qotds[ctx.guild.id].pop(number-1)
            syncConfig()
            await ctx.reply('QOTD removed from the server\'s list of QOTDS successfully. To view the full list, run /qotd_list')
        else:
            await ctx.reply('That QOTD does not exist in this server\'s list of QOTDS. To view the full list, run /qotd_list')
    else:
        await ctx.reply('Please specify a QOTD to remove')

# command to view a list of qotds, formatted in an embed
@slash.command(name='qotd_list', description='View a list of QOTDs for the server')
async def qotd_list(ctx):
    global qotds
    if ctx.guild.id in qotds:
        qotdEmbed = discord.Embed(title='QOTD List', color=0x00ff00)
        qotdEmbed.set_footer(text=f'To add a QOTD, use /add_qotd <QOTD>  {"| QOTDs mention  ``" + qotdMention[ctx.guild.id] + "``" if qotdMention[ctx.guild.id] != "" else ""}| QOTD channel set to #{qotdChannel[ctx.guild.id].name} | QOTDs post at {str(qotdTime[ctx.guild.id][0]) if qotdTime[ctx.guild.id][0] >= 10 else "0" + str(qotdTime[ctx.guild.id][0])}:{str(qotdTime[ctx.guild.id][1]) if qotdTime[ctx.guild.id][1] >= 10 else "0" + str(qotdTime[ctx.guild.id][1])} UTC')
        qotdMenu = reactionmenu.ButtonsMenu(ctx, menu_type=reactionmenu.ButtonsMenu.TypeEmbedDynamic, rows_requested=10, custom_embed=qotdEmbed)
        qotdMenu.add_row(f'{ctx.guild.name} has the following QOTDs:')
        for i in range(len(qotds[ctx.guild.id])):
            qotdMenu.add_row(f'#{i+1}: ``{qotds[ctx.guild.id][i]}``')
        qotdMenu.add_button(reactionmenu.ComponentsButton(style=reactionmenu.ComponentsButton.style.secondary, emoji='⏪', label='', custom_id=reactionmenu.ComponentsButton.ID_GO_TO_FIRST_PAGE))
        qotdMenu.add_button(reactionmenu.ComponentsButton(style=reactionmenu.ComponentsButton.style.secondary, emoji='⬅', label='', custom_id=reactionmenu.ComponentsButton.ID_PREVIOUS_PAGE))
        qotdMenu.add_button(reactionmenu.ComponentsButton(style=reactionmenu.ComponentsButton.style.secondary, emoji='❔', label='', custom_id=reactionmenu.ComponentsButton.ID_GO_TO_PAGE))
        qotdMenu.add_button(reactionmenu.ComponentsButton(style=reactionmenu.ComponentsButton.style.secondary, emoji='➡', label='', custom_id=reactionmenu.ComponentsButton.ID_NEXT_PAGE))
        qotdMenu.add_button(reactionmenu.ComponentsButton(style=reactionmenu.ComponentsButton.style.secondary, emoji='⏩', label='', custom_id=reactionmenu.ComponentsButton.ID_GO_TO_LAST_PAGE))
        
        await ctx.reply('Menu loading...', ephemeral=True)
        await qotdMenu.start(send_to=ctx.channel)
    else:
        await ctx.reply('This server does not have any QOTDs.')

# command to set this guild's QOTD time
@slash_commands.has_permissions(manage_guild=True)
@slash.command(name='set_qotd_time', description='Set the time to send the QOTD', options=[dislash.Option('hour', 'Hour (in 24 hour UTC) to post the QOTD', OptionType.INTEGER, required=True), dislash.Option('minute', 'Minute (in 24 hour UTC) to post the QOTD', OptionType.INTEGER, required=False)])
async def set_qotd_time(ctx, hour, minute=0):
    global qotdTime
    if hour != None and minute != None and hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59:
        qotdTime[ctx.guild.id] = [hour, minute]
        syncConfig()
        await ctx.reply('QOTD time set successfully.')
    else:
        await ctx.reply('Please specify a valid time to set the QOTD to')

# command to set this guild's QOTD mention
@slash_commands.has_permissions(manage_guild=True)
@slash.command(name='set_qotd_role', description='Set the role to ping when a qotd is sent (can be none)', options=[dislash.Option('role', 'Role to use when sending the QOTD', OptionType.ROLE, required=False)])
async def set_qotd_role(ctx, role=None):
    global qotdMention
    if role != None:
        qotdMention[ctx.guild.id] = role.mention
        syncConfig()
        await ctx.reply('QOTD mention set successfully.')
    else:
        qotdMention[ctx.guild.id] = ''
        syncConfig()
        await ctx.reply('QOTD mention cleared successfully.')

# reload command to run the reload config function
@slash_commands.has_permissions(administrator=True)
@slash.command(name='reload_config', description='Reload the config file')
async def reload_config(ctx):
    reloadConfig()
    await ctx.reply('Config file reloaded successfully.')

# reaction-based poll command
@slash.command(name='poll_lin_edition', description='Create a poll', options=[dislash.Option('question', 'Question to ask the world', OptionType.STRING, required=True)])
async def poll_lin_edition(ctx, question):
    # send a message with the author's name and the question
    pollMessage = await ctx.reply(f'{ctx.author.name} asks: {question}')
    # add the reactions
    evilhammie = discord.utils.get(ctx.guild.emojis, name='evilhammie')
    sadhammie = discord.utils.get(bot.emojis, name='sadhammie')
    await pollMessage.add_reaction(evilhammie)
    await pollMessage.add_reaction(sadhammie)

tonesList = {'s': 'sarcastic', 'j': 'joking', 'hj': 'half-joking', 'srs': 'serious', 'p': 'platonic', 'r': 'romantic',
                 'l': 'lyrics', 'ly': 'lyrics', 't': 'teasing', 'nm': 'not mad or upset', 'nc': 'negative connotation',
                 'neg': 'negative connotation', 'pc': 'positive connotation', 'pos': 'positive connotation',
                 'lh': 'lighthearted', 'nbh': 'nobody here', 'm': 'metaphorically', 'li': 'literally',
                 'rh': 'rhetorical question', 'gen': 'genuine question', 'hyp': 'hyperbole', 'c': 'copypasta',
                 'th': 'threat', 'cb': 'clickbait', 'f': 'fake', 'g': 'genuine'}

@slash.message_command( 
    name="Translate SAR" #idk man ask alaine
)
async def translate_tone_indicators(ctx: ContextMenuInteraction):
    if ctx.message.content:
        msg = ctx.message
    else:
        return await ctx.reply('This message has no content!', epheremal=True)
    tones = str(msg.content).split('/')
    del tones[0]
    identifiedTones = []
    for part in tones:
        if part == '/':
            continue  # skip this part of the message
        try:
            identifiedTone = tonesList[part.strip()]  # find meaning
            identifiedTones.append(identifiedTone)  # and save it
        except KeyError:
            continue  # if there is none, ignore
    if len(identifiedTones) != 0:  # if we found any
        await ctx.reply('Detected tones: %s' % (", ".join(identifiedTones)))
    else:
        await ctx.reply('No tones found!', ephemeral=True)
        

 
bot.run(config['token'])