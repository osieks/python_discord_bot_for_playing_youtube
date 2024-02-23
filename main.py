from discord.ext import commands
import discord
from pytube import YouTube
import vlc
from time import sleep

BOT_TOKEN = "MTIxMDY2MDk5NjQ3Mzk0NjEyNA.G5Zpju.R1OE39xl7tnqjSgYEXwt3YKbCLSiG-QFPjYlmg"
CHANNEL_ID = 700787041243496519

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
voice_client = None
play_next = []

@bot.event
async def on_ready():
    print("Bot is ready")
    channel = bot.get_channel(CHANNEL_ID)
    #await channel.send("Bot is ready")
   
@bot.command()
async def play(ctx, url):
    global voice_client, play_next
    if voice_client is None or ctx.message.guild.voice_client is None:
        await ctx.send("najpierw !join")
        return
    else:
        #await ctx.send("NIE")
        
        play_next.append(url)
        print(play_next)
        if ctx.voice_client.is_playing():
            await ctx.reply("Dodano do kolejki")
            s = ", ".join(str(x) for x in play_next) 
            await ctx.send("Kolejka: "+s)
        else:
            await ctx.reply("Zaczynam")
            play_queue(ctx, voice_client)

def play_queue(ctx, voice_client):
    global play_next
    
    print(play_next)
    if len(play_next) > 0 and ctx.voice_client.is_playing() == False:
        url = play_next[0]
        
        #await ctx.send("Playing " + url)
        
        yt = YouTube(url)
        # Get the highest quality audio stream
        audio_stream = yt.streams.get_audio_only()

        # Download the audio stream
        audio_stream.download(filename='audio.mp4')
        
        voice_client.play(discord.FFmpegPCMAudio(executable=r"C:\Users\mateu\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-6.1.1-full_build\bin\ffmpeg.exe",source="audio.mp4"), after=lambda e: play_queue(ctx,voice_client))

        play_next.pop(0)
        
        #await ctx.send("Kolejka: " + play_next)
    else:
        ctx.send("Nic w kolejce")
  
@bot.command()
async def skip(ctx):
    global voice_client
    global play_next
    
    if voice_client is None:
        await ctx.send("najpierw !join")
        return
    else:
        if len(play_next) > 0:
            await ctx.send("skipping")
            voice_client.stop()
            s = ", ".join(str(x) for x in play_next) 
            await ctx.send("Kolejka: "+s)
        else:
            await ctx.send("nic w kolejce")


@bot.command()
async def join(ctx):
    global voice_client
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send("No hej")
    
@bot.command()
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