import datetime
import discord
import r6sapi as r6
import os
import psycopg2 as sql
from discord.ext import commands

operatorImg ={
    "hibana": "https://thumbs.gfycat.com/SeveralLeafyBlesbok-small.gif",
    "smoke": "https://i.pinimg.com/originals/50/8c/91/508c91273d9cadd223116f8fdab1d17a.gif",
    "kapkan": "https://i.redd.it/vtvmde989y6y.gif",
    "tachanka": "https://thumbs.gfycat.com/InnocentDesertedCrane-size_restricted.gif",
    "thermite": "https://i.redd.it/i30e9mwwaj7y.gif",
    "thatcher": "https://i.pinimg.com/originals/07/47/cd/0747cd5abe82df6e90eac9224892a6ba.gif",
    "glaz": "https://i.redd.it/csh7pynckn7y.gif",
    "bandit": "https://thumbs.gfycat.com/AdventurousSpiritedAfricanaugurbuzzard-size_restricted.gif",
    "rook": "https://thumbs.gfycat.com/SpectacularUntidyAmericanbadger-size_restricted.gif",
    "iq": "https://thumbs.gfycat.com/DirtyLinearHoverfly-size_restricted.gif",
    "pulse": "https://thumbs.gfycat.com/CoordinatedAthleticIndianhare-size_restricted.gif",
    "mute": "https://i.pinimg.com/originals/db/05/8b/db058bf3632a98dc3db2f2b929cf40e5.gif",
    "valkyrie": "https://marcopixel.eu/r6-operatoricons/assets/png/valkyrie.png",
    "frost": "https://thumbs.gfycat.com/LongIllinformedBlacklemur-size_restricted.gif",
    "doc": "https://thumbs.gfycat.com/RashLegalIbadanmalimbe-max-1mb.gif",
    "sledge": "https://i.imgur.com/9ItT0aQ.gifv",
    "jager": "https://thumbs.gfycat.com/DifficultPotableIberianmidwifetoad-size_restricted.gif",
    "blackbeard": "https://thumbs.gfycat.com/AffectionateSourBlackandtancoonhound-max-1mb.gif",
    "fuze": "https://thumbs.gfycat.com/BeautifulCautiousAfricanelephant-size_restricted.gif",
    "echo": "http://pa1.narvii.com/6935/8f669bc13357207e3b27ab62fe1cb4caec522a12r1-482-538_00.gif",
    "caveira": "https://i.pinimg.com/originals/5a/a3/37/5aa3378906542849876688d2ad23571e.gif",
    "blitz": "https://thumbs.gfycat.com/MasculinePerkyBufflehead-small.gif",
    "montagne": "https://thumbs.gfycat.com/SoggyBraveFly-small.gif",
    "ash": "https://i.pinimg.com/originals/2f/17/12/2f1712fb7da4654b4de29132c6cf702c.gif",
    "twitch": "https://marcopixel.eu/r6-operatoricons/assets/png/twitch.png",
    "castle": "https://i.redd.it/yx9glfk1ls7y.gif",
    "buck": "https://marcopixel.eu/r6-operatoricons/icons/png/buck.png",
    "capitao": "https://thumbs.gfycat.com/InconsequentialEmotionalHind-size_restricted.gif",
    "jackal": "https://thumbs.gfycat.com/GreenLimpingInexpectatumpleco-max-1mb.gif",
    "mira": "https://i.imgur.com/ztYA0kP.gif",
    "ela": "https://thumbs.gfycat.com/LiveWarpedGharial-size_restricted.gif",
    "lesion": "https://thumbs.gfycat.com/MiniatureUnfortunateIrrawaddydolphin-size_restricted.gif",
    "ying": "https://marcopixel.eu/r6-operatoricons/assets/png/ying.png",
    "dokkaebi": "https://i.redd.it/a6zjy16cr2701.gif",
    "vigil": "https://i.redd.it/syrlum4so9j01.gif",
    "zofia": "https://thumbs.gfycat.com/UnhappyPerfumedJumpingbean-max-1mb.gif",
    "alibi": "https://marcopixel.eu/r6-operatoricons/assets/png/alibi.png",
    "maestro":"https://marcopixel.eu/r6-operatoricons/assets/png/maestro.png",
    "clash": "https://marcopixel.eu/r6-operatoricons/assets/png/clash.png",
    "kaid" : "https://marcopixel.eu/r6-operatoricons/assets/png/kaid.png",
    "mozzie": "https://marcopixel.eu/r6-operatoricons/assets/png/mozzie.png",
    "lion": "https://i.pinimg.com/originals/67/80/a9/6780a9553bc83816dfa92a947d73abec.gif",
    "finka": "https://marcopixel.eu/r6-operatoricons/assets/png/finka.png",
    "maverick": "https://marcopixel.eu/r6-operatoricons/assets/png/maverick.png",
    "nomad": "https://marcopixel.eu/r6-operatoricons/assets/png/nomad.png",
    "gridlock": "https://marcopixel.eu/r6-operatoricons/assets/png/gridlock.png"
}

auth = r6.Auth(os.getenv("R6-ACCOUNT",None), os.getenv("R6-PASSWORD",None))
bot = commands.Bot(command_prefix='d.')
bot.remove_command('help')

##機器人啟動完成
@bot.event
async def on_ready():
    game = discord.Game("d.help")
    await bot.change_presence(activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

##幹員資訊
@bot.command()
async def operator(ctx,user,operator):
    try:
        operator = operator.lower()
        player = await auth.get_player(user, r6.Platforms.UPLAY)
        
        data = await player.load_operator(operator)
        
        imgUrl = operatorImg[operator]
        
        if(data.wins == 0 and data.losses == 0):
            await ctx.send("此角色無資料可顯示")
        else:
            win_ratio = str(round((data.wins/(data.wins+data.losses))*100,2))+"%"
            kd = str(round(data.kills/data.deaths,2))
            time = str(datetime.timedelta(seconds=data.time_played))
        
        
        embed = discord.Embed(title=data.name.upper()+"資訊",colour=discord.Colour.teal())
        embed.set_author(name=player.name, url=player.url, icon_url=player.icon_url)
        embed.set_thumbnail(url=imgUrl)
        embed.add_field(name=bold("勝/敗"), value=bold(str(data.wins))+"/"+bold(str(data.losses))+" | "+bold(win_ratio))
        embed.add_field(name=bold("殺/死"), value=bold(str(data.kills))+"/"+bold(str(data.deaths))+" | "+bold(kd), inline=True)
        embed.add_field(name=bold("爆頭"), value=bold(str(data.headshots)))
        embed.add_field(name=bold("近戰"), value=bold(str(data.melees)), inline=True)
        embed.add_field(name=bold("被拉起"), value=bold(str(data.dbnos)))
        embed.add_field(name=bold(data.statistic_name), value=bold(str(data.statistic)), inline=True)
        embed.add_field(name=bold("經驗值"),value=bold(str(data.xp)))
        embed.add_field(name=bold("遊玩時間"),value=bold(time))
        
        await ctx.send(embed=embed)
    except Exception as error:
        if(str(error) == "No results"):
            await ctx.send("找不到用戶，請檢查用戶名是否正確")
        elif(len(str(error))>16):
            if(str(error)[0:16] == "invalid operator"):
                await ctx.send("找不到幹員，請檢查幹員名稱是否正確")
        else:
            await ctx.send(error)
    
##幹員比較
@bot.command()
async def vsoperator(ctx,user1,user2,operator):
    errorFlag = False
    operator = operator.lower()
    try:
        player1 = await auth.get_player(user1, r6.Platforms.UPLAY)
    except Exception as error:
        errorFlag = True
        await ctx.send("找不到用戶1，請檢查用戶名是否正確")
    try:
        player2 = await auth.get_player(user2, r6.Platforms.UPLAY)
    except Exception as error:
        errorFlag = True
        await ctx.send("找不到用戶2，請檢查用戶名是否正確")
    try:
        data1 = await player1.load_operator(operator)
        data2 = await player2.load_operator(operator)
    except Exception as error:
        errorFlag = True
        await ctx.send("找不到幹員，請檢查幹員名稱是否正確")
    
    if(not errorFlag):
    
        imgUrl = operatorImg[operator]    
        
        if(data1.wins == 0 and data1.losses == 0):
            errorFlag = True
            await ctx.send("用戶1此角色無資料無法比較")
        else:
            win_ratio1 = str(round((data1.wins/(data1.wins+data1.losses))*100,2))+"%"
            kd1 = str(round(data1.kills/data1.deaths,2))
            time1 = str(datetime.timedelta(seconds=data1.time_played))
        
        if(data2.wins == 0 and data2.losses == 0):
            errorFlag = True
            await ctx.send("用戶2此角色無資料無法比較")
        else:
            win_ratio2 = str(round((data2.wins/(data2.wins+data2.losses))*100,2))+"%"
            kd2 = str(round(data2.kills/data2.deaths,2))
            time2 = str(datetime.timedelta(seconds=data2.time_played))
        
        if(not errorFlag):
            embed = discord.Embed(title=player1.name+" vs "+player2.name,description=operator.upper()+"比較",colour=discord.Colour.green())
            embed.set_thumbnail(url=imgUrl)
            embed.add_field(name=bold("勝/敗"), value=bold(player1.name+": ")+str(data1.wins)+"/"+str(data1.losses)+"  |  "+win_ratio1+newLine()+bold(player2.name+": ")+str(data2.wins)+"/"+str(data2.losses)+"  |  "+win_ratio2)
            embed.add_field(name=bold("殺/死"), value=bold(player1.name+": ")+str(data1.kills)+"/"+str(data1.deaths)+"  |  "+kd1+newLine()+bold(player2.name+": ")+str(data2.kills)+"/"+str(data2.deaths)+"  |  "+kd2, inline=True)
            embed.add_field(name=bold("爆頭"), value=bold(player1.name+": ")+str(data1.headshots)+newLine()+bold(player2.name+": ")+str(data2.headshots))
            embed.add_field(name=bold("近戰"), value=bold(player1.name+": ")+str(data1.melees)+newLine()+bold(player2.name+": ")+str(data2.melees), inline=True)
            embed.add_field(name=bold("被拉起"), value=bold(player1.name+": ")+str(data1.dbnos)+newLine()+bold(player2.name+":")+str(data2.dbnos))
            embed.add_field(name=bold(data1.statistic_name), value=bold(player1.name+": ")+str(data1.statistic)+newLine()+bold(player2.name+": ")+str(data2.statistic), inline=True)
            embed.add_field(name=bold("經驗值"),value=bold(player1.name+": ")+str(data1.xp)+newLine()+bold(player2.name+": ")+str(data2.xp))
            embed.add_field(name=bold("遊玩時間"),value=bold(player1.name+": ")+time1+newLine()+bold(player2.name+": ")+time2)
            
            await ctx.send(embed=embed)
    
##玩家資訊
@bot.command()
async def player(ctx,user):
    try:
        player = await auth.get_player(user,r6.Platforms.UPLAY)
        await player.load_general()
        
        kd = str(round(player.kills/player.deaths,2))
        headshot_ratio = str(round((player.headshots/player.bullets_hit)*100,2))+"%"
        win_ratio = str(round((player.matches_won/player.matches_played)*100,2))+"%"
        time = str(datetime.timedelta(seconds=player.time_played))
        
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=player.name, url=player.url, icon_url=player.icon_url)
        embed.add_field(name=bold("擊殺資訊"),value=bold("擊殺:")+str(player.kills)+" | "+bold("死亡:")+str(player.deaths)+" | "+bold("KD:")+kd+newLine()+bold("近戰:")+str(player.melee_kills)+" | "+bold("穿透擊殺:")+str(player.penetration_kills)+newLine()+bold("自殺:")+str(player.suicides)+" | "+bold("盲殺:")+str(player.blind_kills),inline=False)
        embed.add_field(name=bold("射擊資訊"),value=bold("擊中:")+str(player.bullets_hit)+" | "+bold("爆頭:")+str(player.headshots)+newLine()+bold("爆頭率:")+headshot_ratio,inline=False)
        embed.add_field(name=bold("場次資訊"),value=bold("勝場:")+str(player.matches_won)+" | "+bold("敗場:")+str(player.matches_lost)+newLine()+bold("總場數:")+str(player.matches_played)+" | "+bold("勝率:")+win_ratio,inline=False)
        embed.add_field(name=bold("團隊貢獻"),value=bold("助攻:")+str(player.kill_assists)+" | "+bold("擊倒:")+str(player.dbnos)+newLine()+bold("協助擊倒:")+str(player.dbno_assists)+" | "+bold("破壞:")+str(player.gadgets_destroyed)+newLine()+bold("拉起:")+str(player.revives)+" | "+bold("拉起失敗:")+str(player.revives_denied),inline=False)
        embed.add_field(name=bold("遊玩資訊"),value=bold("經驗值:")+str(player.total_xp)+" | "+bold("時數:")+time,inline=False)
        
        await ctx.send(embed=embed)
    except Exception as error:
        #await ctx.send("找不到用戶，請檢查用戶名是否正確")
        await ctx.send(error)

##查詢玩家排位
@bot.command()
async def ranked(ctx,user):
    try:
        player = await auth.get_player(user,r6.Platforms.UPLAY)
        await player.load_general()
        await player.load_queues()
        
        data = player.ranked
        
        if(data.wins == 0 and data.losses == 0):
            await ctx.send("此玩家無RANK資料")
        else:
            win_ratio = str(round((data.won/(data.won+data.lost))*100,2))+"%"
            kd = str(round(data.kills/data.deaths,2))
            time = str(datetime.timedelta(seconds=data.time_played))
            
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name=player.name, url=player.url, icon_url=player.icon_url)
            embed.add_field(name=bold("遊玩資訊"),value=bold("勝場:")+str(data.won)+" | "+bold("敗場:")+str(data.lost)+newLine()+bold("場數:")+str(data.played)+newLine()+bold("勝率:")+win_ratio+newLine()+bold("遊玩時間:")+time)
            embed.add_field(name=bold("擊殺資訊"),value=bold("擊殺:")+str(data.kills)+" | "+bold("死亡:")+str(data.deaths)+newLine()+bold("KD:")+kd)
            
            await ctx.send(embed=embed)
        
    except Exception as error:
        await ctx.send(error)

##結算歷史戰績
@bot.command()
async def count(ctx,user):
    try:
        conn = sql.connect(database="dafjeikpmmlbso", user="kzwxmrqfzvjiff", password="7833b1bd34bc84051542bfddc2638bf8581444943150a510a1ad74355860e4f1", host="ec2-174-129-238-192.compute-1.amazonaws.com", port="5432")
        cur = conn.cursor()

        player = await auth.get_player(user,r6.Platforms.UPLAY)
        await player.load_general()
        await player.load_queues()

        rankData = player.ranked
        casualData = player.casual

        sqlQryCasual = "SELECT \"KILL\",\"DEATH\",\"WIN\",\"LOSS\" FROM \"USER_INFO\" WHERE \"USER_NAME\" LIKE %s AND \"GAME_MODE\" = 'Casual' ORDER BY \"QUERY_TIME\" DESC LIMIT 1"
        sqlQryRank = "SELECT \"KILL\",\"DEATH\",\"WIN\",\"LOSS\" FROM \"USER_INFO\" WHERE \"USER_NAME\" LIKE %s AND \"GAME_MODE\" = 'Rank' ORDER BY \"QUERY_TIME\" DESC LIMIT 1"
        sqlInsert = "INSERT INTO \"USER_INFO\" VALUES (%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP+ interval '8 hours')"
        sqlQryData = "SELECT * FROM \"USER_INFO\" WHERE \"USER_NAME\" LIKE %s ORDER BY \"QUERY_TIME\" DESC LIMIT 10"

        ##休閒戰績區塊       
        cur.execute(sqlQryCasual,(player.name,))
        casualRows = cur.fetchall()
        if(len(casualRows)==0):
            cur.execute(sqlInsert,(player.name,'Casual',casualData.won,casualData.lost,casualData.kills,casualData.deaths))
        else:
            for row in casualRows:
                if(row[0]!=casualData.kills or row[1]!=casualData.deaths):
                    cur.execute(sqlInsert,(player.name,'Casual',casualData.won-row[2],casualData.lost-row[3],casualData.kills-row[0],casualData.deaths-row[1]))

        ##排名戰績區塊
        cur.execute(sqlQryRank,(player.name,))
        rankRows = cur.fetchall()
        if(len(rankRows)==0):
            cur.execute(sqlInsert,(player.name,'Rank',rankData.won,rankData.lost,rankData.kills,rankData.deaths))
        else:
            for row in rankRows:
                if(row[0]!=rankData.kills or row[1]!=rankData.deaths):
                    cur.execute(sqlInsert,(player.name,'Rank',rankData.won-row[2],rankData.lost-row[3],rankData.kills-row[0],rankData.deaths-row[1]))
        
        ##製作訊息區塊
        cur.execute(sqlQryData,(player.name,))
        dataRows = cur.fetchall()
        embed = discord.Embed(title="近日戰績",colour=discord.Colour.orange())
        casualStr = ""
        rankStr = ""
        for row in dataRows:
            if(row[1]=='Casual'):
                casualStr += "時間:"+str(row[6])[:19]+bold("|")+"勝/負:"+str(row[2])+"/"+str(row[3])+"殺/死:"+str(row[4])+"/"+str(row[5])+newLine()
            else:
                rankStr += "時間:"+str(row[6])[:19]+bold("|")+"勝/負:"+str(row[2])+"/"+str(row[3])+"殺/死:"+str(row[4])+"/"+str(row[5])+newLine()

        embed.add_field(name=bold("休閒"),value=casualStr)
        embed.add_field(name=bold("排名"),value=rankStr)

        await ctx.send(embed=embed)
        conn.commit()
        conn.close()

    except Exception as error:
        conn.close()
        await ctx.send(error)
        
        
##自定義說明
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="指令說明",description="[]為必要參數",colour=discord.Colour.gold())
    embed.add_field(name= bold("d.operator [user] [operator]"),value= "查詢各幹員資訊",inline=False)
    embed.add_field(name= bold("d.vsoperator [user1] [user2] [operator]"),value= "比較各幹員資訊",inline=False)
    embed.add_field(name= bold("d.player [user]"),value="查詢玩家資訊",inline=False)
    embed.add_field(name= bold("d.ranked [user]"),value="查詢玩家排位",inline=False)
    
    await ctx.send(embed=embed)

##粗體字
def bold(text):
    return "**"+str(text)+"**"
##換行
def newLine():
    return "\r\n"
    
bot.run(os.getenv("DISCORD-KEY",None))
