from flask import Flask, render_template, request, jsonify, session
from services.browser_automation import BrowserAutomation
from services.data_extractor import DataExtractor
from services.encryption_analyzer import EncryptionAnalyzer
import json
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global instances
browser_automation = BrowserAutomation()
data_extractor = DataExtractor()
encryption_analyzer = EncryptionAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-collection', methods=['POST'])
def start_collection():
    try:
        data = request.json
        target_url = data.get('target_url')
        collection_interval = data.get('interval', 10)
        
        # Start browser automation in a separate thread
        def collect_data():
            with app.app_context():
                driver = browser_automation.init_driver()
                browser_automation.navigate_to_url(driver, target_url)
                
                while session.get('collection_active', True):
                    # Extract visible data
                    visible_data = data_extractor.extract_visible_data(driver)
                    
                    # Analyze network requests
                    network_data = data_extractor.capture_network_requests(driver)
                    
                    # Analyze potential encryption
                    encryption_analysis = encryption_analyzer.analyze_encryption(driver)
                    
                    # Store results
                    results = {
                        'visible_data': visible_data,
                        'network_data': network_data,
                        'encryption_analysis': encryption_analysis,
                        'timestamp': time.time()
                    }
                    
                    session['latest_data'] = results
                    time.sleep(collection_interval)
        
        session['collection_active'] = True
        collection_thread = threading.Thread(target=collect_data)
        collection_thread.daemon = True
        collection_thread.start()
        
        return jsonify({'status': 'success', 'message': 'Data collection started'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop-collection', methods=['POST'])
def stop_collection():
    session['collection_active'] = False
    browser_automation.cleanup()
    return jsonify({'status': 'success', 'message': 'Data collection stopped'})

@app.route('/get-data')
def get_data():
    data = session.get('latest_data', {})
    return jsonify(data)

@app.route('/analyze-encryption', methods=['POST'])
def analyze_encryption():
    try:
        target_url = request.json.get('target_url')
        analysis = encryption_analyzer.deep_analysis(target_url)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)