from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ssid = request.form.get("ssid")
        password = request.form.get("password")
        security = request.form.get("security", "WPA")  # Default to WPA

        if not ssid:
            return render_template("index.html", error="SSID is required.")

        # Create Wi-Fi QR code string
        wifi_info = f"WIFI:T:{security};S:{ssid};P:{password};H:;"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=10,
            border=4,
        )
        qr.add_data(wifi_info)
        qr.make(fit=True)

        # Generate a styled QR code with rounded modules and a radial gradient
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                back_color=(255, 255, 255),
                center_color=(0, 0, 255),
                edge_color=(0, 255, 0),
            ),
        )

        # Save QR code to BytesIO
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="wifi_qr_code.png")

    return render_template("index.html")

# Add this if block to run the app
if __name__ == '__main__':
    app.run(debug=True)