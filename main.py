from discord.ext import commands
import discord
import vlc
from time import sleep


from pytube import YouTube
from youtube_search import YoutubeSearch

#pytube fix for age restriction
from pytube.innertube import _default_clients 
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID"]


from secret_bot_token import BOT_TOKEN
CHANNEL_ID = 700787041243496519

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
voice_client = None
play_next = []
play_search = []

@bot.event
async def on_ready():
    print("Bot is ready")
    channel = bot.get_channel(CHANNEL_ID)
    #await channel.send("Bot is ready")
  
@bot.command(help='wyswietlenie pomoc')
async def helpme(ctx):
    await ctx.send("""
!helpme -> pomoc
!github -> github repo

!join -> dołączenie do kanału
!leave -> wyjście z kanału

!play link-> odtwarzanie linku
!play (...) -> wyszukiwanie
!play (1-5) -> odtwarzanie numeru z wyszukiwania
!skip -> odtwarzanie kolejnego utworu w kolejce

!pause -> zatrzymanie odtwarzania
!unpause -> wznowienia odtwarzania

!queue -> kolejka odtwarzania""")
    return

@bot.command(help='wyświetlenie github repo')
async def github(ctx):
    await ctx.send("https://github.com/osieks/python_discord_bot_for_playing_youtube")
    return

@bot.command(help='wznowienia odtwarzania')
async def unpause(ctx):
    global voice_client
    voice_client.resume()
    return

@bot.command(help='link -> odtwarzanie linku\n (...) -> wyszukiwanie\n (1-5) -> odtwarzanie numeru z wyszukiwania\n')
async def play(ctx,* , url):
    global voice_client, play_next, play_search
    
    if voice_client is None or ctx.message.guild.voice_client is None:
        await ctx.send("najpierw !join")
        return
    else:
        #await ctx.send("NIE")
        if url == "":
            play_queue(ctx, voice_client)
            return
        try:
            print(int(url))
            if 1 <= int(url) <= len(play_search):
                print(url+" to liczba")
                print(play_search[int(url)-1]['url_suffix'])
                play_next.append('https://www.youtube.com' + play_search[int(url)-1]['url_suffix'])
                play_queue(ctx, voice_client)
                return
            else:
                await ctx.send("Zly numer")
                return
            
        except ValueError as e:
            print(e)
            if "https://www.youtube.com/watch" in url:
                pass        
                play_next.append(url)
                print(play_next)
                
                if ctx.voice_client.is_playing():
                    await ctx.reply("Dodano do kolejki")
                    s = ", ".join(str(x) for x in play_next) 
                    await ctx.send("Kolejka: "+s)
                else:
                    await ctx.reply("Zaczynam")
                    play_queue(ctx, voice_client)
                return
            
            await ctx.send("Wyszukiwanie...")
            results = YoutubeSearch(url, max_results=5).to_dict()
            print(results)
            iterator = 1
            propozycje = ''
            for v in results:
                print(iterator ,v)
                propozycje=propozycje+(str(iterator)+'. '+ v['title']+'\n')
                #await ctx.reply('https://www.youtube.com' + v['url_suffix'])
                iterator+=1
            
            await ctx.reply(propozycje)
            play_search=results
            return


def play_queue(ctx, voice_client):
    global play_next,play_search
    
    print(play_next)
    if len(play_next) > 0 and ctx.voice_client.is_playing() == False:
        url = play_next[0]
        
        #await ctx.send("Playing " + url)
        print(url)
        if "https://www.youtube.com/watch" not in url: 
            print("bad link")
            play_next.pop(0)
            return
        
        yt = YouTube(url)
            
        # Get the highest quality audio stream
        audio_stream = yt.streams.get_audio_only()

        # Download the audio stream
        audio_stream.download(filename='audio.mp4')
        try:
            voice_client.play(discord.FFmpegPCMAudio(executable=r"C:\Users\mateu\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-6.1.1-full_build\bin\ffmpeg.exe",source="audio.mp4"), after=lambda e: play_queue(ctx,voice_client))
        except:
           # ctx.send("Występil blad")
            print("wystapił błąd")
        play_next.pop(0)
        
        #await ctx.send("Kolejka: " + play_next)
    else:
        print("nic w kolejce")
  
@bot.command(help='zatrzymanie odtwarzania')
async def pause(ctx):
        global voice_client
        # Checks if music is playing and pauses it, otherwise sends the player a message that nothing is playing
        try:
            voice_client.pause()
        except:
            await ctx.send(f"{ctx.author.mention} i'm not playing!")
    
@bot.command(help='odtwarzanie kolejnego utworu w kolejce')
async def skip(ctx):
    global voice_client
    global play_next
    
    if voice_client is None:
        await ctx.send("najpierw !join")
        return
    else:
        await ctx.send("skipping")
        if ctx.voice_client.is_playing():
            voice_client.stop()
        else:
            play_next.pop(0)
        s = ", ".join(str(x) for x in play_next) 
        await ctx.send("Kolejka: "+s)

@bot.command(help='wyświetlenie kolejki odtwarzania')
async def queue(ctx):
    global play_next
    
    if len(play_next)>0:
        s = ", ".join(str(x) for x in play_next) 
        await ctx.send("Kolejka: "+s)
    else:
        await ctx.send("Nic w kolejce")

@bot.command(help='dołączenie do kanału głosowego')
async def join(ctx):
    global voice_client
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send("No hej")
    
@bot.command(help='wyjście z kanału głosowego')
async def leave(ctx):
    global voice_client
    if voice_client is None:
        await ctx.send("najpierw !join")
        return
    else:
        server = ctx.message.guild.voice_client
        await ctx.send("No to cześć")
        await server.disconnect() 
        
bot.run(BOT_TOKEN)