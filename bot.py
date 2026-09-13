import os
from flask import Flask, request, jsonify
from license import generate_license

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json
    
    print("CEO JSON PAKET SA SELLAPPA:", data)
    
    if not data:
        return jsonify({'success': True, 'message': 'Prazan zahtev primljen'}), 200
        
    try:
        # 1. Čitamo iz additional_information ili custom_fields polja
        hardware_id = None
        
        # Provera kroz additional_information (SellApp format sa slike)
        add_info = data.get('additional_information', [])
        if isinstance(add_info, list):
            for item in add_info:
                if isinstance(item, dict) and item.get('label') == 'Zen Hardware Id':
                    hardware_id = item.get('value')
                    break

        # Rezervna provera ako je u custom_fields
        if not hardware_id and 'custom_fields' in data:
            hardware_id = data.get('custom_fields', {}).get('hardware_id')

        # Provera da li je ovo samo testni webhook
        if not hardware_id:
            print("Primljen testni webhook sa SellApp-a - sve radi!")
            return jsonify({'success': True, 'message': 'Test webhook uspesno primljen'}), 200

        # Čitamo email kupca
        customer_email = data.get('email') or data.get('customer_email', 'Nepoznat email')
            
        # Generisanje licence (zahvaljujući v1.0 logici uvek vraća 6432)
        license_code = generate_license(hardware_id)
        
        print(f'{customer_email} je kupio licencu. Generisan kod: {license_code}')
        
        # Vraćamo uspešan odgovor SellApp-u
        return jsonify({'success': True, 'license': license_code}), 200
        
    except Exception as e:
        print(f"Greška u obradi webhooka: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
