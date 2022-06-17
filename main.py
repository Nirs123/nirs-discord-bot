import discord
from discord.ext import commands
import os
import googletrans
import requests
import json
import time
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
import googletrans
from riotwatcher import LolWatcher
import os

load_dotenv()

#FUNCTIONS
#Date
def date_now():
    rep_date = str(date.today().strftime("%d/%m/%Y")+" at "+datetime.now().strftime("%H:%M:%S"))
    return rep_date
#Translate
def f_translate(text):
    translator = googletrans.Translator()
    return (translator.translate(text,dest="fr"))
#API Blague
def api_blague():
    tmp = requests.get("https://blague.xyz/api/joke/random")
    json_data = json.loads(tmp.text)
    q = json_data['joke']['question']
    r = json_data['joke']['answer']
    return [q,r]
#API mmr
lol_watcher = LolWatcher(str(os.getenv('RIOT_API_KEY')))
region = "euw1"
ranks=["MASTER","GRANDMASTER","CHALLENGER"]
def api_mmr(pseudo):
    tmp = requests.get(f"https://euw.whatismymmr.com/api/v1/summoner?name={pseudo}&apiKey={str(os.getenv('MMR_API_KEY'))}")
    player = lol_watcher.summoner.by_name(region,pseudo)
    ranked_stats = lol_watcher.league.by_summoner(region,player['id'])
    try:
        if ranked_stats[0]['queueType'] == "RANKED_FLEX_SR":
            index = 1
        elif ranked_stats[0]['queueType'] == "RANKED_SOLO_5x5":
            index = 0
    except:
        return None
    json_data = json.loads(tmp.text)
    try:
        m = json_data['ranked']['avg']
        r_t = json_data['ranked']['closestRank']

        if ranked_stats[index]["tier"] in ranks:
            r_r = ranked_stats[index]["tier"].title()
        else:
            r_r = ranked_stats[index]["tier"].title()+" "+ranked_stats[index]["rank"]
        wins = ranked_stats[index]["wins"]
        losses = ranked_stats[index]["losses"]
        wr_b = (wins * 100) / (wins+losses)
        wr = round(wr_b,1)
        return [m,r_t,r_r,wins,losses,wr]
    except:
        return None
#API Status serveur MC
def api_status_serv_mc():
    tmp = requests.get("https://mcapi.us/server/status?ip=90.78.10.90&port=25565")
    json_data = json.loads(tmp.text)
    status = json_data["online"]
    return status


#Initialisation du bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents,activity = discord.Game(name="Type !help"),help_command=None)


#EVENTS
#Connection du bot
@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

#Check de tout les messages
@bot.event
async def on_message(message):
    if "cringe" in message.content:
        await message.channel.send("a-t-on parlé de ppo ?")
    await bot.process_commands(message)


#COMMANDS
#Commandes help
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='You can use the following commands:',color = 0x992d22,description="!blague\n   !mmr\n   !serveur\n   !translate\n\n\
You can also type !help [command] to show help for the command")
    await ctx.send(embed = em)

#Commande help blague
@help.command()
async def blague(ctx):
    em = discord.Embed(title="Commande !blague",description="Renvoie une blague déterminée aléatoirement",color= 0x992d22)
    em.add_field(name ="**Syntax**", value = "!blague")
    await ctx.send(embed = em)

rank_colors = []
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
    em1 = discord.Embed(title=rep_blague[0],color= 0x992d22)
    await ctx.send(embed = em1)
    time.sleep(2)
    em2 = discord.Embed(title=rep_blague[1],color= 0x992d22)
    await ctx.send(embed = em2)

#Commande serveur
@bot.command()
async def serveur(ctx):
    rep_serv = api_status_serv_mc()
    if rep_serv == True:
        em = discord.Embed(title="Le serveur est en ligne ✅",color=0x2ecc71)
        await ctx.send(embed = em)
    elif rep_serv == False:
        em = discord.Embed(title="Le serveur est hors-ligne ❌",color=0x992d22)
        await ctx.send(embed = em)

dico_rank = {"Iron":0x992d22,"Bronze": 0xa84300,"Silver": 0x979c9f,"Gold": 0xf1c40f,"Platinum": 0x1abc9c,"Diamond": 0x206694,"Master": 0x71368a,"Grandmaster": 0xad1457,"Challenger": 0x7289da}
#Commande mmr
@bot.command()
async def mmr(ctx, Pseudo):
    rep_mmr = api_mmr(Pseudo)
    if rep_mmr == None:
        em = discord.Embed(title="Erreurs possibles:",description="Le joueur n'est pas trouvé\nLe joueur n'a pas de rank\nLe service n'est pas disponible",color= 0x992d22)
        await ctx.send(embed = em)
    else:
        em = discord.Embed(title=f"Stats du joueur: {Pseudo}",description=str("**MMR:** "+str(rep_mmr[0])+" qui correspond a "+str(rep_mmr[1])+"\n**Rank actuel:** "+str(rep_mmr[2])+"\n**Wins:** "+str(rep_mmr[3])+"\n**Losses:** "+str(rep_mmr[4])+"\n**Winrate:** "+str(rep_mmr[5])+"%"),color=dico_rank[rep_mmr[2].split()[0]])
        file = discord.File(f'ranks/{rep_mmr[2].split()[0]}.png') 
        em.set_thumbnail(url=f"attachment://{rep_mmr[2].split()[0]}.png")
        await ctx.send(file=file,embed = em)

#Commande translate
lang = googletrans.LANGUAGES
@bot.command()
async def translate(ctx, *Texte):
    rep_translate = f_translate(" ".join(Texte))
    em = discord.Embed(title=f"Traduction en Français depuis {f_translate(lang[rep_translate.src.lower()]).text}",description=rep_translate.text,color=0x992d22)
    await ctx.send(embed = em)


#Lancement du Bot
bot.run(os.getenv('TOKEN'))