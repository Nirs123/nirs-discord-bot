import discord
from discord.ext import commands
import os
import requests
import json
import time
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from googletrans import Translator

load_dotenv()

#FUNCTIONS
#Date
def date_now():
    rep_date = str(date.today().strftime("%d/%m/%Y")+" at "+datetime.now().strftime("%H:%M:%S"))
    return rep_date
#Translate
def f_translate(text):
    translator = Translator()
    return (translator.translate(text,dest="fr"))
#API Blague
def api_blague():
    tmp = requests.get("https://blague.xyz/api/joke/random")
    json_data = json.loads(tmp.text)
    q = json_data['joke']['question']
    r = json_data['joke']['answer']
    return [q,r]
#API mmr
def api_mmr(pseudo):
    tmp = requests.get(f"https://euw.whatismymmr.com/api/v1/summoner?name={pseudo}")
    json_data = json.loads(tmp.text)
    try:
        m = json_data['ranked']['avg']
        r = json_data['ranked']['closestRank']
        return [m,r]
    except:
        return None
#API Status serveur MC
def api_status_serv_mc():
    tmp = requests.get("https://mcapi.us/server/status?ip=90.78.10.90&port=25565")
    json_data = json.loads(tmp.text)
    status = json_data["online"]
    return status


#Initialisation du bot
bot = commands.Bot(command_prefix="!",activity = discord.Game(name="Type !help"),help_command=None)


#EVENTS
#Connection du bot
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

#Check de tout les messages
@bot.event
async def on_message(message):
    if message.content.startswith("cringe"):
        await message.channel.send("a-t-on parlé de ppo ?")
    await bot.process_commands(message)
"""
#Check on deleted message
@bot.event
async def on_message_delete(message):
    await message.channel.send(f"```diff\n-MESSAGE DELETED\n+DATE: {date_now()}\n+AUTEUR: {message.author}\n+MESSAGE: {message.content}```")

#Check on message edit
@bot.event
async def on_message_edit(before,after):
    await before.channel.send(f"```diff\n-MESSAGE EDITED\n+DATE: {date_now()}\n+AUTEUR: {before.author}\n+MESSAGE BEFORE: {before.content}\n+MESSAGE AFTER: {after.content}```")

#Check on member join
@bot.event
async def on_member_join(member):
    pass

#Check on member leave
@bot.event
async def on_member_leave(member):
    pass
"""

#COMMANDS
#Commandes help
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='You can use the following commands:',color = 0x992d22,description="!blague\n   !mmr\n   !serveur\n   !translate\n\n\
You can also type !help [command] to Show help to the command")
    await ctx.send(embed = em)

#Commande help blague
@help.command()
async def blague(ctx):
    em = discord.Embed(title="Commande !blague",description="Renvoie une blague déterminée aléatoirement",color= 0x992d22)
    em.add_field(name ="**Syntax**", value = "!blague")
    await ctx.send(embed = em)

#Commande help mmr
@help.command()
async def mmr(ctx):
    em = discord.Embed(title="Commande !mmr",description="Renvoie le MMR et le Rank du joueur",color= 0x992d22)
    em.add_field(name ="**Syntax**", value = "!mmr [Pseudo]")
    await ctx.send(embed = em)

#Commande help serveur
@help.command()
async def serveur(ctx):
    em = discord.Embed(title="Commande !serveur",description="Renvoie le status (ON ou OFF) du serveur Minecraft  ⚠️DISPONIBLE CET ETE⚠️",color= 0x992d22)
    em.add_field(name ="**Syntax**", value = "!serveur")
    await ctx.send(embed = em)

#Commande help translate
@help.command()
async def translate(ctx):
    em = discord.Embed(title="Commande !translate",description="Renvoie en Francais la traduction d'un texte de n'importe quelle langue",color= 0x992d22)
    em.add_field(name ="**Syntax**", value = "!translate [Texte]")
    await ctx.send(embed = em)

#Commande blague
@bot.command()
async def blague(ctx):
    rep_blague = api_blague()
    await ctx.send(rep_blague[0])
    time.sleep(2)
    await ctx.send(rep_blague[1])

#Commande serveur
@bot.command()
async def serveur(ctx):
    rep_serv = api_status_serv_mc()
    if rep_serv == True:
        await ctx.send("Le serveur est en ligne ✅")
    elif rep_serv == False:
        await ctx.send("Le serveur est hors-ligne ❌")

#Commande mmr
@bot.command()
async def mmr(ctx, Pseudo):
    rep_mmr = api_mmr(Pseudo)
    if rep_mmr == None:
        await ctx.send("Erreur: le joueur n'est pas trouvé/n'a pas de rank")
    else:
        await ctx.send("MMR: "+str(rep_mmr[0])+"\nRank: "+str(rep_mmr[1]))

#Commande translate
@bot.command()
async def translate(ctx, *Texte):
    await ctx.send(f_translate(" ".join(Texte)).text)

#Lancement du Bot
bot.run(os.getenv('TOKEN'))