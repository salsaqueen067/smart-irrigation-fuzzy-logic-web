from flask import Flask, render_template, jsonify, request
import numpy as np
from datetime import datetime
import random

app = Flask(__name__)

# Kelas Fuzzy Logic untuk Smart Irrigation
class FuzzyIrrigationController:
    def __init__(self):
        pass
    
    # Fungsi keanggotaan untuk Kelembaban Tanah (0-100%)
    def soil_moisture_low(self, x):
        if x <= 20:
            return 1
        elif 20 < x < 40:
            return (40 - x) / 20
        else:
            return 0
    
    def soil_moisture_medium(self, x):
        if x <= 20:
            return 0
        elif 20 < x <= 40:
            return (x - 20) / 20
        elif 40 < x <= 60:
            return (60 - x) / 20
        else:
            return 0
    
    def soil_moisture_high(self, x):
        if x <= 40:
            return 0
        elif 40 < x < 60:
            return (x - 40) / 20
        else:
            return 1
    
    # Fungsi keanggotaan untuk Suhu (0-50°C)
    def temperature_cold(self, x):
        if x <= 15:
            return 1
        elif 15 < x < 25:
            return (25 - x) / 10
        else:
            return 0
    
    def temperature_normal(self, x):
        if x <= 15:
            return 0
        elif 15 < x <= 25:
            return (x - 15) / 10
        elif 25 < x <= 35:
            return (35 - x) / 10
        else:
            return 0
    
    def temperature_hot(self, x):
        if x <= 25:
            return 0
        elif 25 < x < 35:
            return (x - 25) / 10
        else:
            return 1
    
    # Fungsi keanggotaan untuk Kelembaban Udara (0-100%)
    def humidity_low(self, x):
        if x <= 30:
            return 1
        elif 30 < x < 50:
            return (50 - x) / 20
        else:
            return 0
    
    def humidity_medium(self, x):
        if x <= 30:
            return 0
        elif 30 < x <= 50:
            return (x - 30) / 20
        elif 50 < x <= 70:
            return (70 - x) / 20
        else:
            return 0
    
    def humidity_high(self, x):
        if x <= 50:
            return 0
        elif 50 < x < 70:
            return (x - 50) / 20
        else:
            return 1
    
    # Fungsi keanggotaan untuk Output Durasi Penyiraman (0-60 menit)
    def duration_short(self, x):
        if x <= 10:
            return 1
        elif 10 < x < 20:
            return (20 - x) / 10
        else:
            return 0
    
    def duration_medium(self, x):
        if x <= 10:
            return 0
        elif 10 < x <= 20:
            return (x - 10) / 10
        elif 20 < x <= 40:
            return (40 - x) / 20
        else:
            return 0
    
    def duration_long(self, x):
        if x <= 20:
            return 0
        elif 20 < x < 40:
            return (x - 20) / 20
        else:
            return 1
    
    def calculate_irrigation(self, soil_moisture, temperature, humidity):
        # Fuzzifikasi
        sm_low = self.soil_moisture_low(soil_moisture)
        sm_med = self.soil_moisture_medium(soil_moisture)
        sm_high = self.soil_moisture_high(soil_moisture)
        
        temp_cold = self.temperature_cold(temperature)
        temp_norm = self.temperature_normal(temperature)
        temp_hot = self.temperature_hot(temperature)
        
        hum_low = self.humidity_low(humidity)
        hum_med = self.humidity_medium(humidity)
        hum_high = self.humidity_high(humidity)
        
        # Aturan Fuzzy (27 aturan)
        rules = []
        
        # Rule 1-9: Soil Moisture Low
        rules.append(min(sm_low, temp_cold, hum_low))   # Long
        rules.append(min(sm_low, temp_cold, hum_med))   # Long
        rules.append(min(sm_low, temp_cold, hum_high))  # Medium
        rules.append(min(sm_low, temp_norm, hum_low))   # Long
        rules.append(min(sm_low, temp_norm, hum_med))   # Long
        rules.append(min(sm_low, temp_norm, hum_high))  # Medium
        rules.append(min(sm_low, temp_hot, hum_low))    # Long
        rules.append(min(sm_low, temp_hot, hum_med))    # Long
        rules.append(min(sm_low, temp_hot, hum_high))   # Long
        
        # Rule 10-18: Soil Moisture Medium
        rules.append(min(sm_med, temp_cold, hum_low))   # Medium
        rules.append(min(sm_med, temp_cold, hum_med))   # Medium
        rules.append(min(sm_med, temp_cold, hum_high))  # Short
        rules.append(min(sm_med, temp_norm, hum_low))   # Medium
        rules.append(min(sm_med, temp_norm, hum_med))   # Medium
        rules.append(min(sm_med, temp_norm, hum_high))  # Short
        rules.append(min(sm_med, temp_hot, hum_low))    # Long
        rules.append(min(sm_med, temp_hot, hum_med))    # Medium
        rules.append(min(sm_med, temp_hot, hum_high))   # Medium
        
        # Rule 19-27: Soil Moisture High
        rules.append(min(sm_high, temp_cold, hum_low))  # Short
        rules.append(min(sm_high, temp_cold, hum_med))  # Short
        rules.append(min(sm_high, temp_cold, hum_high)) # Short
        rules.append(min(sm_high, temp_norm, hum_low))  # Short
        rules.append(min(sm_high, temp_norm, hum_med))  # Short
        rules.append(min(sm_high, temp_norm, hum_high)) # Short
        rules.append(min(sm_high, temp_hot, hum_low))   # Medium
        rules.append(min(sm_high, temp_hot, hum_med))   # Short
        rules.append(min(sm_high, temp_hot, hum_high))  # Short
        
        # Mapping rules ke output
        rule_outputs = [
            40, 40, 30, 40, 40, 30, 50, 50, 40,  # SM Low
            30, 30, 15, 30, 30, 15, 40, 30, 30,  # SM Medium
            15, 15, 10, 15, 15, 10, 30, 15, 10   # SM High
        ]
        
        # Defuzzifikasi menggunakan metode Centroid (Weighted Average)
        numerator = sum(rules[i] * rule_outputs[i] for i in range(len(rules)))
        denominator = sum(rules)
        
        if denominator == 0:
            duration = 15  # Default jika tidak ada aturan yang aktif
        else:
            duration = numerator / denominator
        
        return round(duration, 2)

# Inisialisasi Fuzzy Controller
fuzzy_controller = FuzzyIrrigationController()

# Simulasi data sensor
sensor_data = {
    'soil_moisture': 35,
    'temperature': 28,
    'humidity': 55,
    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

irrigation_status = {
    'is_active': False,
    'duration': 0,
    'remaining_time': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    # Simulasi pembacaan sensor (dalam aplikasi nyata, baca dari IoT device)
    sensor_data['soil_moisture'] = max(0, min(100, sensor_data['soil_moisture'] + random.uniform(-5, 5)))
    sensor_data['temperature'] = max(0, min(50, sensor_data['temperature'] + random.uniform(-2, 2)))
    sensor_data['humidity'] = max(0, min(100, sensor_data['humidity'] + random.uniform(-3, 3)))
    sensor_data['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify(sensor_data)

@app.route('/api/calculate-fuzzy', methods=['POST'])
def calculate_fuzzy():
    data = request.json
    soil_moisture = float(data.get('soil_moisture', sensor_data['soil_moisture']))
    temperature = float(data.get('temperature', sensor_data['temperature']))
    humidity = float(data.get('humidity', sensor_data['humidity']))
    
    duration = fuzzy_controller.calculate_irrigation(soil_moisture, temperature, humidity)
    
    return jsonify({
        'duration': duration,
        'recommendation': get_recommendation(duration)
    })

@app.route('/api/start-irrigation', methods=['POST'])
def start_irrigation():
    data = request.json
    duration = float(data.get('duration', 0))
    
    irrigation_status['is_active'] = True
    irrigation_status['duration'] = duration
    irrigation_status['remaining_time'] = duration
    
    return jsonify({'status': 'success', 'message': f'Penyiraman dimulai selama {duration} menit'})

@app.route('/api/stop-irrigation', methods=['POST'])
def stop_irrigation():
    irrigation_status['is_active'] = False
    irrigation_status['remaining_time'] = 0
    
    return jsonify({'status': 'success', 'message': 'Penyiraman dihentikan'})

@app.route('/api/irrigation-status')
def get_irrigation_status():
    if irrigation_status['is_active'] and irrigation_status['remaining_time'] > 0:
        irrigation_status['remaining_time'] = max(0, irrigation_status['remaining_time'] - 0.1)
        if irrigation_status['remaining_time'] == 0:
            irrigation_status['is_active'] = False
    
    return jsonify(irrigation_status)

def get_recommendation(duration):
    if duration < 15:
        return "Penyiraman singkat - Tanah cukup lembab"
    elif duration < 30:
        return "Penyiraman sedang - Kondisi normal"
    else:
        return "Penyiraman lama - Tanah kering, butuh banyak air"

if __name__ == '__main__':
    app.run(debug=True, port=5000)