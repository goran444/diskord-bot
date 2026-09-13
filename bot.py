import os
import asyncio
import discord
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot je uspešno ulogovan kao {client.user}')

# Dodajemo root rutu da Render i Cloudflare vide da je sajt živ
async def handle_root(request):
    return web.Response(text="Bot je aktivan i web server radi!", status=200)

async def handle_webhook(request):
    try:
        data = await request.json()
        print("Primljen webhook sa SellApp-a:", data)
        return web.Response(text="Webhook primljen uspešno", status=200)
    except Exception as e:
        print(f"Greška u webhook-u: {e}")
        return web.Response(text="Greška", status=400)

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_root)  # <-- Ova linija rešava Render health check
    app.router.add_post('/webhook', handle_webhook)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server sluša na portu {port}")

async def main():
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("Greška: DISCORD_TOKEN nije podešen!")
        return

    await start_web_server()
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
