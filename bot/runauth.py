import argparse
import discord
import mysql.connector
import requests
import re
from discord.utils import get
from discord.ext import commands
import base64

mydb = mysql.connector.connect(
  host="localhost",
  database="c0omhauth",
  user="c0auth",
  password="pass"
)

print(mydb)

parser = argparse.ArgumentParser(description='discord id')
parser.add_argument("-d")
parser.add_argument("-o")

args = parser.parse_args()
d = args.d
o = args.o
print("discord: " + d + "\nosu: " + o)

sql_select_Query = "SELECT * FROM users WHERE discordid = '" + str(d) + "'"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
dires = cursor.rowcount

sql_select_Query = "SELECT * FROM users WHERE osuid = '" + str(o) + "'"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
osres = cursor.rowcount

aintents = discord.Intents.all()

client = discord.Client(intents=aintents)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="ab>", intents=intents) # someone said i needed this

@bot.event
async def on_ready():
    print('bot logged in')
    
    
    guild = bot.get_guild(639515567233171476)
    channel = bot.get_channel(724765865631023105)
    embed = discord.Embed(title="A new authentication request has been submitted.", description="osu! link: https://osu.ppy.sh/users/" + str(o) + "\ndiscord tag: <@" + str(d) + ">", color=0xaaaa00) # make green embed
    await channel.send(embed=embed)
    user = bot.get_user(int(d))
    member = guild.get_member(int(d))

    
    if(osres == 0):
        print("osu! id not signed up")
        
        if(dires == 0):
            print("discord id not signed up")
            guild = bot.get_guild(639515567233171476)
            
            if guild.get_member(int(d)) is not None:
                print("osu! id: " + o);
                print("discord id: " + d);
                print("user is in server")
                roles = guild.get_member(int(d)).roles
                amount = len(roles)
                rolesstr = str(roles)
                if "Server Booster" in rolesstr:
                    amount -= 1;
                
                
                if amount == 1:
                    print("user has no roles")
                    await user.send('Authentication Successful! You will receive your roles soon!')
                    print("getting medal count")
                    url = 'https://osu.ppy.sh/users/' + str(o)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
                    }
                    cookies = requests.head(url)
                    r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
                    content = str(r.content)
                    medals = content.count("achievement_id")
                    print("getting roles")
                    r50cid = 667130931617988610
                    r50c = get(guild.roles, id=r50cid)
                    r75cid = 667130932406255647
                    r75c = get(guild.roles, id=r75cid)
                    r90cid = 639517663990906910
                    r90c = get(guild.roles, id=r90cid)
                    r95cid = 643262553681559593
                    r95c = get(guild.roles, id=r95cid)
   
                    print("applying roles")
                    if(medals >= 129 and medals < 193):
                        print("50%")
                        await member.add_roles(r50c)
                    if(medals >= 193 and medals < 232):
                        print("75%")
                        await member.add_roles(r75c)
                    if(medals >= 232 and medals < 245):
                        print("90%")
                        await member.add_roles(r90c)
                    if(medals > 245):
                        print("95%")
                        await member.add_roles(r95c)
    
                        
                    mhr = 639516052056965130
                    rmhr = get(guild.roles, id=mhr)
                    await member.add_roles(rmhr)
                    
                    print("setting username")
                    uname = re.search('<title>(.*?) ', content).group(1)
                    uname = uname.replace("&nbsp;", " ") 
                    uname = uname.replace("\u2665", " ")
                    print("setting up user info with this info:")
                    print("osuid: " + str(o))
                    print("discordid: " + str(o))
                    print("osuname: " + uname)
                    string_bytes = user.name.encode("utf-8")
                    base64_bytes = base64.b64encode(string_bytes) 
                    base64_string = base64_bytes.decode("ascii") 
                    dname = base64_string;
                    print("discordname: " + dname + "#" + user.discriminator)
                    pfp = str(user.avatar_url)
                    if pfp is None:
                        pfp = "none";
                    print("discordpfp: " + pfp)
                    mycursor = mydb.cursor()
                    print("INSERT INTO users (`id`, `discordname`, `osuname`, `pfp`, `discordtag`, `medals`, `osuid`, `discordid`) VALUES (NULL, '" + dname + "', '" + uname + "', '" + pfp + "', " + str(user.discriminator) + ", " + str(medals) + ", " + str(o) + ", " + str(d) + ");")
                    sql = "INSERT INTO users (`id`, `discordname`, `osuname`, `pfp`, `discordtag`, `medals`, `osuid`, `discordid`) VALUES (NULL, '" + dname + "', '" + uname + "', '" + pfp + "', " + str(user.discriminator) + ", " + str(medals) + ", " + str(o) + ", " + str(d) + ");"
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) affected") 

                    embed = discord.Embed(title="Request accepted. All checks have passed.", description="osu! link: https://osu.ppy.sh/users/" + str(o) + "\ndiscord tag: <@" + str(d) + ">", color=0x00aa00) # make green embed
                    await channel.send(embed=embed)
                    
                    print("quitting\n\n")
                else:
                    print("has roles")
                    await user.send("ERROR : We're not 100% sure what went wrong here, all we know is you have roles on the discord, but ain't signed up. Please contact me at @Hubz#6283 with a screenshot of this message.")
                    await bot.logout()
                    
            else:
                print("user is not in server")
                await user.send('ERROR : You do not seem to be in the osu! medal hunters discord. Please join here. https://discord.gg/8qpNTs6\nIf you think this is incorrect, please contact me at @Hubz#6283')
                await bot.logout()
                
        else:
            print("discord id taken")
            await user.send('ERROR : This discord account is already signed up!\nIf you think this is incorrect, please contact me at @Hubz#6283')
            await bot.logout()
            
    else:
        print("osu! id taken")
        await user.send('ERROR : This osu! account is already signed up!\nIf you think this is incorrect, please contact me at @Hubz#6283')
        await bot.logout()
    await bot.logout()


bot.run('no')
