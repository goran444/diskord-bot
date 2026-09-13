import discord
from discord.ext import commands
from aiohttp import web
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Bot je uspešno ulogovan kao {client.user}')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

async def handle_payment(request):
    data = await request.json()
    buyer_discord_id = data.get('discord_id')
    product_code = "TVOJ-TAJNI-KOD-12345"
    
    user = await client.fetch_user(int(buyer_discord_id))
    if user:
        await user.send(f"Hvala na uplati! Tvoj kod je: {product_code}")
        
    return web.Response(text="Uplata uspešno obrađena!")

async def web_server():
    app = web.Application()
    app.router.add_post('/webhook', handle_payment)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

async def main():
    await web_server()
    await client.start('MTU0Mzc2NjE0OTg4NjUxMzE4Mg.GKsbEz.RrNf3DUYtbwT1hKJkE4lgHI6X3hBls6a_r6Z0Y')

asyncio.run(main())
@bot.event
async def on_member_join(member):
    # Zamenite ovaj ID broj sa ID-jem vašeg #general kanala
    channel = bot.get_channel(1238507128248078428) 
    if channel:
        await channel.send(f"Dobrodošao na server, {member.mention}!")
