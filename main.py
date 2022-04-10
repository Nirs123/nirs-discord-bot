from ssl import CHANNEL_BINDING_TYPES
import discord
import os
import requests
import json
import time
import random

client = discord.Client()

def blague():
    tmp = requests.get("https://blague.xyz/api/joke/random")
    json_data = json.loads(tmp.text)
    q = json_data['joke']['question']
    r = json_data['joke']['answer']
    return [q,r]

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!test"):
        await message.channel.send("tg")

    if message.content.startswith("!launch lost Ark"):
        await message.channel.send("Suite a plusieurs problèmes techniques, nous reportons le lancement de Lost Ark au 18 Mars 2024")
    ''''
    if "pseudo" in message.content:
        await message.channel.send(f"{message.author.mention} tg")
    '''

    '''
    if "cringe" in message.content:
        await message.channel.send(file=discord.File('img/cringe.gif'))
    '''

    if "cringe" in message.content:
        if random.randint(0,1) == 0:
            await message.channel.send("a-t-on parlé de ppo ?")
        else:
            await message.channel.send("a-t-on parlé de shuttoo ?")

    if message.content.startswith("!blague"):
        tmp = blague()
        await message.channel.send(tmp[0])
        time.sleep(2)
        await message.channel.send(tmp[1])

    if message.content.startswith("!commandes"):
        await message.channel.send("oquiysdfrpiqgt")

    if message.content.startswith("!123test"):
        await message.channel.send(message.author)
    
    if message.author.name == '🥩SkLopee🥩':
        '''await message.add_reaction("<:pp0:839219763573948416>")'''
    

client.run(os.getenv("TOKEN"))