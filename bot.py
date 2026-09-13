import os
from flask import Flask, request, jsonify
from license import generate_license

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json
    
    # OVO SMO DODALI: Štampamo ceo JSON paket u logove da vidiš strukturu
    print("CEO JSON PAKET SA SELLAPPA:", data)
    
    if not data:
        return jsonify({'success': True, 'message': 'Prazan zahtev primljen'}), 200
        
    try:
        # Proveravamo da li je ovo testni webhook sa SellApp-a (koji nema custom_fields)
        custom_fields = data.get('custom_fields')
        if not custom_fields or 'hardware_id' not in custom_fields:
            print("Primljen testni webhook sa SellApp-a - sve radi!")
            return jsonify({'success': True, 'message': 'Test webhook uspesno primljen'}), 200

        # Pravi podaci od kupovine
        hardware_id = int(custom_fields.get('hardware_id', 0))
        customer_email = data.get('customer_email', 'Nepoznat email')
        
        if not hardware_id:
            return jsonify({'error': 'Hardware ID nedostaje'}), 400
            
        # Generisanje licence pomoću formule iz license.py
        license_code = generate_license(hardware_id)
        
        print(f'{customer_email} je kupio licencu. Generisan kod: {license_code}')
        
        # Vraćamo licencu nazad SellApp-u da je on uruči kupcu
        return jsonify({'success': True, 'license': license_code}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
