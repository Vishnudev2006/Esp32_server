from flask import Flask, request, jsonify

app = Flask(__name__)

# GLOBAL VARIABLES
# We store the latest sensor readings here.
# Initially set to 0.
sensor_data = {
    "ldr1": 0,
    "ldr2": 0
}

# ---------------------------------------------------------
# ROUTE 1: The API Endpoint (ESP32 sends data here)
# ---------------------------------------------------------
@app.route('/update', methods=['POST'])
def receive_data():
    global sensor_data
    
    # Check if the ESP32 sent the correct data fields
    if 'ldr1' in request.form and 'ldr2' in request.form:
        sensor_data['ldr1'] = request.form['ldr1']
        sensor_data['ldr2'] = request.form['ldr2']
        
        # Print to console so you can see it working in the terminal
        print(f"✅ Data Received -> Left: {sensor_data['ldr1']} | Right: {sensor_data['ldr2']}")
        
        return "Data Received", 200
    else:
        print("❌ Error: Invalid data format")
        return "Bad Request", 400

# ---------------------------------------------------------
# ROUTE 2: The Frontend Dashboard (You view this in Browser)
# ---------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    # This is a simple HTML page with CSS styling.
    # It auto-refreshes every 2 seconds to show new data.
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Sensor Dashboard</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; text-align: center; padding-top: 50px; }}
            .container {{ display: flex; justify-content: center; gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 200px; }}
            h1 {{ color: #333; }}
            h2 {{ margin: 0; color: #555; font-size: 18px; }}
            .value {{ font-size: 48px; font-weight: bold; color: #007bff; margin: 10px 0; }}
            .status {{ font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <h1>LIVE SENSOR DATA</h1>
        <div class="container">
            <div class="card">
                <h2>Sensor 1 (Left)</h2>
                <div class="value">{sensor_data['ldr1']}</div>
                <span class="status">Raw ADC Value</span>
            </div>
            <div class="card">
                <h2>Sensor 2 (Right)</h2>
                <div class="value">{sensor_data['ldr2']}</div>
                <span class="status">Raw ADC Value</span>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

if __name__ == '__main__':
    # Host='0.0.0.0' allows external devices (like your ESP32) to connect.
    # Port=5000 is the standard Flask port.
    app.run(host='0.0.0.0', port=5000, debug=True)