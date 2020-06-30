import argparse
import discord
import mysql.connector
import requests
import re
from discord.utils import get

mydb = mysql.connector.connect(
  host="localhost",
  database="omhauth",
  user="hubz",
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

class MyClient(discord.Client):
    async def on_ready(self):
        print('bot logged in')
        channel = client.get_channel(724765865631023105)
        embed = discord.Embed(title="A new authentication request has been submitted.", description="osu! link: https://osu.ppy.sh/users/" + str(o) + "\ndiscord tag: <@" + str(d) + ">", color=0xaaaa00) # make green embed
        await channel.send(embed=embed)
        user = client.get_user(int(d))
        
        if(osres == 0):
            print("osu! id not signed up")
            
            if(dires == 0):
                print("discord id not signed up")
                guild = client.get_guild(639515567233171476)
                
                if guild.get_member(int(d)) is not None:
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
                        
                        user = guild.get_member(int(d))
                        
                        print("applying roles")
                        if(medals > 117 and medals < 177):
                            print("50%")
                            await user.add_roles(r50c)
                        if(medals > 176 and medals < 212):
                            print("75%")
                            await user.add_roles(r75c)
                        if(medals > 211 and medals < 224):
                            print("90%")
                            await user.add_roles(r90c)
                        if(medals > 223):
                            print("95%")
                            await user.add_roles(r95c)
                            
                        mhr = 639516052056965130
                        rmhr = get(guild.roles, id=mhr)
                        await user.add_roles(rmhr)
                        
                        print("setting username")
                        uname = re.search('Everything you ever wanted to know about (.*?)!', content).group(1)
                        
                        await user.edit(nick=uname)

                        print("adding to database...")
                        mySql_insert_query = 'INSERT INTO users (osuid, discordid, medals) VALUES (' + str(o) + ', ' + str(d) + ', ' + str(medals) + ')';
                        cursor = mydb.cursor()
                        cursor.execute(mySql_insert_query)
                        mydb.commit()
                        embed = discord.Embed(title="Request accepted. All checks have passed.", description="osu! link: https://osu.ppy.sh/users/" + str(o) + "\ndiscord tag: <@" + str(d) + ">", color=0x00aa00) # make green embed
                        await channel.send(embed=embed)
                        print("quitting\n\n")
                        
                    else:
                        print("has roles")
                        await user.send("ERROR : We're not 100% sure what went wrong here, all we know is you have roles on the discord, but ain't signed up. Please contact me at @Hubz#6283 with a screenshot of this message.")
                        await MyClient.logout(self)
                        
                else:
                    print("user is not in server")
                    await user.send('ERROR : You do not seem to be in the osu! medal hunters discord. Please join here. https://discord.gg/8qpNTs6\nIf you think this is incorrect, please contact me at @Hubz#6283')
                    await MyClient.logout(self)
                    
            else:
                print("discord id taken")
                await user.send('ERROR : This discord account is already signed up!\nIf you think this is incorrect, please contact me at @Hubz#6283')
                await MyClient.logout(self)
                
        else:
            print("osu! id taken")
            await user.send('ERROR : This osu! account is already signed up!\nIf you think this is incorrect, please contact me at @Hubz#6283')
            await MyClient.logout(self)

        await MyClient.logout(self)

client = MyClient()
client.run('token')