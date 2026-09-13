import os
from flask import Flask, request, jsonify
from license import generate_license

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json
    
    # Ovde SellApp šalje podatke (prilagođena polja gde kupac upisuje Hardware/Serial ID)
    # Primer: preuzimamo hardware_id iz podataka koje je SellApp poslao
    try:
        # Prilagodi naziv polja u zavisnosti kako si ga nazvao u SellApp-u
        hardware_id = int(data.get('custom_fields', {}).get('hardware_id', 0))
        customer_email = data.get('customer_email')
        
        if not hardware_id:
            return jsonify({'error': 'Hardware ID nedostaje'}), 400
            
        # Generisanje licence pomoću formule iz license.py
        license_code = generate_license(hardware_id)
        
        # Ovde možeš dodati kod da se license_code pošalje kupcu na e-mail ili Discord
        print(T'{customer_email} je kupio licencu. Generisan kod: {license_code}')
        
        return jsonify({'success': True, 'license': license_code}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
