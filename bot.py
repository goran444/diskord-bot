import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json or {}
    
    print("=== PRIMLJEN PODATAK SA SELLAPPA ===")
    print("CEO JSON PAKET:", data)
    
    # Fiksni licencni kod za v1.0 skriptu
    LICENSE_CODE = "6432"
    
    try:
        # 1. Čitamo iz additional_information ili custom_fields polja
        hardware_id = None
        
        # Provera kroz additional_information
        add_info = data.get('additional_information', [])
        if isinstance(add_info, list):
            for item in add_info:
                if isinstance(item, dict) and item.get('label') == 'Zen Hardware Id':
                    hardware_id = item.get('value')
                    break

        # Rezervna provera ako je u custom_fields
        if not hardware_id and 'custom_fields' in data:
            hardware_id = data.get('custom_fields', {}).get('hardware_id')

        # Čitamo email kupca
        customer_email = data.get('email') or data.get('customer_email', 'Nepoznat email')
            
        print(f"=== USPEH: Kupac ({customer_email}) | Hardware ID: {hardware_id} ===")
        print(f"=== ŠALJEM LICENCNI KOD NA SELLAPP: {LICENSE_CODE} ===")
        
        # Vraćamo odgovor u više formata radi kompatibilnosti sa SellApp-om
        return jsonify({
            'success': True,
            'status': 'success',
            'license': LICENSE_CODE,
            'key': LICENSE_CODE,
            'code': LICENSE_CODE,
            'deliverable': LICENSE_CODE
        }), 200
        
    except Exception as e:
        print(f"Greška u obradi webhooka: {str(e)}")
        # Vraćamo 200 sa kodom 6432 čak i ako izbije greška u parsiranju
        return jsonify({
            'success': True, 
            'license': LICENSE_CODE, 
            'key': LICENSE_CODE
        }), 200

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
