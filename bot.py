import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def sellapp_webhook():
    data = request.json or {}
    
    print("=== PRIMLJEN WEBHOOK SA SELLAPPA ===")
    LICENSE_CODE = "6432"
    
    try:
        # Izvlačimo Hardware ID samo radi logova
        add_info = data.get('additional_information', [])
        hw_id = "Nepoznat"
        if isinstance(add_info, list):
            for item in add_info:
                if isinstance(item, dict) and item.get('label') == 'Zen Hardware Id':
                    hw_id = item.get('value')
                    break
                    
        print(f"=== USPEH: Hardware ID: {hw_id} | Vraćam kod: {LICENSE_CODE} ===")
        
        # SellApp kod dinamičkih webhook-ova ponekad očekuje čist tekst (plain text) kao odgovor
        return Response(LICENSE_CODE, mimetype='text/plain', status=200)
        
    except Exception as e:
        print(f"Greška: {str(e)}")
        return Response(LICENSE_CODE, mimetype='text/plain', status=200)

@app.route('/')
def home():
    return "Bot i webhook server su aktivni!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
