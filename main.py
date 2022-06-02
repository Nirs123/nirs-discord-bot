from ssl import CHANNEL_BINDING_TYPES
import discord
import os
import requests
import json
import time
import random
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

def blague():
    tmp = requests.get("https://blague.xyz/api/joke/random")
    json_data = json.loads(tmp.text)
    q = json_data['joke']['question']
    r = json_data['joke']['answer']
    return [q,r]

def mmr(pseudo):
    tmp = requests.get(f"https://euw.whatismymmr.com/api/v1/summoner?name={pseudo}")
    json_data = json.loads(tmp.text)
    try:
        m = json_data['ranked']['avg']
        r = json_data['ranked']['closestRank']
        return [m,r]
    except:
        return None

def status_serv_mc():
    tmp = requests.get("https://mcapi.us/server/status?ip=90.78.10.90&port=25565")
    json_data = json.loads(tmp.text)
    status = json_data["online"]
    return status

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!launch lost Ark"):
        await message.channel.send("Suite a plusieurs problèmes techniques, nous reportons le lancement de Lost Ark au 18 Mars 2024")

    if "cringe" in message.content:
        await message.channel.send("a-t-on parlé de ppo ?")

    if message.content.startswith("!blague"):
        tmp = blague()
        await message.channel.send(tmp[0])
        time.sleep(2)
        await message.channel.send(tmp[1])

    if message.content.startswith("!serveur"):
        tmp = status_serv_mc()
        if tmp == True:
            await message.channel.send("Le serveur est en ligne ✅")
        elif tmp == False:
            await message.channel.send("Le serveur est hors-ligne ❌")

    if message.content.startswith("!mmr"):
        tmp = str(message.content[5:len(message.content)])
        rep = mmr(tmp)
        if rep == None:
            await message.channel.send("Erreur: le joueur n'est pas trouvé/n'a pas de rank")
        else:
            await message.channel.send("MMR: "+str(rep[0])+"\nRank: "+str(rep[1]))

    if message.content.startswith("!commandes"):
        await message.channel.send("**You can use the following commands:**\n!blague \n!serveur (disponible cet été a l'ouverture du serveur MC)\n!mmr")

client.run(os.getenv('TOKEN'))