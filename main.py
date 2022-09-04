import nextcord
from nextcord.ext import commands
import wavelink
intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "?", intents=intents)
@bot.event
async def on_ready():
  print("Bot is ready")
  bot.loop.create_task(node_connect())

@bot.event
async def on_wavelink_node_ready(node = wavelink.Node):
  print(f'Node {node.identifier} is ready!')

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="lavalink.oops.wtf", port=443, password="www.freelavalink.ga", https=True)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        await ctx.send(f"Playing \"`{track.title}`\"")
        return await vc.play(track)
    
    # if vc.queue.is_empty:
    #     return await vc.disconnect()

    if not vc.queue.is_empty:
        next_song =  vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Playing \"`{next_song.title}`\", {get_comment()}")

@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a vc")
    elif not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and (not vc.track):
        await vc.play(search)
        await ctx.send(f"Playing \"`{search.title}`\"")
    else:
        await vc.queue.put_wait(search)
        await ctx.send(f"\"`{search.title}`\" added to queue")
    
    vc.ctx = ctx
    setattr(vc, "loop", False)
    
@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I'm not connected to a vc yet")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a vc")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.pause()
    await ctx.send("Music has been paused")

@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Can't resume")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("JOIN A VC")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.resume()
    await ctx.send("The music will resume")

@bot.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Can't stop music")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a vc first")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.stop()
    await ctx.send("The music has been stopped")

@bot.command()
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("I'm not in a vc")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("JOIN A VC FIRST")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await vc.disconnect()
    await ctx.send("Bye")

@bot.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Error")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Join a vc")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    try:
        vc.loop = not vc.loop
    except:
        setattr(vc, "loop", True)
    if vc.loop:
        return await ctx.send("Loop activated")
    else:
        return await ctx.send("Loop desactivated")
  
bot.run("MTAxNDk3NjYyMTI0MzAwNzA3OQ.GP-Dvn.GDXfC4vbu7kI6bz1iT0ebgMv96Bxa2jQqKumoY")
