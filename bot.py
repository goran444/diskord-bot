import os
import threading
from flask import Flask, request, jsonify
from license import generate_license
import discord
from discord.ext import commands

# --- DEO 1: FLASK WEB SERVER ZA SELLAPP ---
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json
    if not data:
        return jsonify({'success': True, 'message': 'Prazan zahtev primljen'}), 200
        
    try:
        custom_fields = data.get('custom_fields')
        if not custom_fields or 'hardware_id' not in custom_fields:
            return jsonify({'success': True, 'message': 'Test webhook uspesno primljen'}), 200

        hardware_id = int(custom_fields.get('hardware_id', 0))
        customer_email = data.get('customer_email', 'Nepoznat email')
        
        if not hardware_id:
            return jsonify({'error': 'Hardware ID nedostaje'}), 400
            
        license_code = generate_license(hardware_id)
        print(f'{customer_email} je kupio licencu. Generisan kod: {license_code}')
        
        return jsonify({'success': True, 'license': license_code}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200


# --- DEO 2: DISCORD BOT (PING-PONG I DOBRODOŠLICA) ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Discord bot je ulogovan kao {bot.user}')

@bot.event
async def on_member_join(member):
    # Automatska poruka kada neko uđe na server
    try:
        await member.send(f"Dobrodošao na Gameness server, {member.name}! Drago nam je što si tu.")
    except Exception as e:
        print(f"Greška pri slanju dobrodošlice: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Ping-pong provera
    if message.content.lower() == 'ping':
        await message.channel.send('pong')

    await bot.process_commands(message)

def run_discord_bot():
    TOKEN = os.environ.get('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Upozorenje: DISCORD_TOKEN nije pronađen u environment varijablama!")


# --- POKRETANJE SVEGA ZAJEDNO ---
if __name__ == '__main__':
    # Pokrećemo Discord bota u pozadinskoj nitu (background thread)
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.daemon = True
    discord_thread.start()

    # Pokrećemo Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
