from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        security = request.form.get('security', "WPA")

        if not ssid:
            return render_template('index.html', error='SSID is required')
        
        #create Wifi QR code String
        wifi_info = f"WIFI:T:{security};S:{ssid};P:{password};;"

        #create QR code instance
        qr = qrcode.QRCode(version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(wifi_info)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="wifi_qr_code.png")

    return render_template('index.html')

# Add this if block to run the app
if __name__ == '__main__':
    app.run(debug=True)