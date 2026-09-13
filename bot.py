import os
import discord
from discord.ext import commands
from aiohttp import web
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Bot je uspešno ulogovan kao {client.user}')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Webhook deo za SellApp uplate
async def handle_payment(request):
    try:
        data = await request.json()
        buyer_discord_id = data.get('discord_id')
        product_code = "TVOJ-TAJNI-KOD-12345"
        
        if buyer_discord_id:
            user = await client.fetch_user(int(buyer_discord_id))
            if user:
                await user.send(f"Hvala na uplati! Tvoj kod je: {product_code}")
                
        return web.Response(text="Uplata uspešno obrađena!")
    except Exception as e:
        print(f"Greška sa webhook-om: {e}")
        return web.Response(text=str(e), status=500)

@client.event
async def on_member_join(member):
    # Zamenite ovaj ID broj sa ID-jem vašeg general kanala
    channel = client.get_channel(123858712838708820)
    if channel:
        await channel.send(f"Dobrodošao na server, {member.mention}!")

async def start_web_server():
    app = web.Application()
    app.router.add_post('/webhook', handle_payment)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # KLJUČNO ZA RENDER: Čita dodeljeni port iz okruženja ili koristi 10000
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server uspešno pokrenut na portu {port}")

async def main():
    # Unesi svoj token ovde ili kroz Environment Variables na Renderu
    token = os.environ.get("DISCORD_TOKEN", "TVOJ_DISCORD_BOT_TOKEN")
    
    await start_web_server()
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
