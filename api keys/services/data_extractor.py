from selenium.webdriver.common.by import By
import json
import time
import re

class DataExtractor:
    def __init__(self):
        self.extracted_data = []
    
    def extract_visible_data(self, driver):
        """Extract visible data from the webpage"""
        data = {
            'text_content': [],
            'numeric_data': [],
            'game_elements': [],
            'timestamps': []
        }
        
        try:
            # Extract all text content
            elements = driver.find_elements(By.XPATH, "//*[text()]")
            for element in elements:
                text = element.text.strip()
                if text and len(text) < 1000:  # Avoid large text blocks
                    data['text_content'].append(text)
            
            # Look for numeric data (potential betting data)
            numeric_pattern = r'\b\d+\.?\d*\b'
            for text in data['text_content']:
                numbers = re.findall(numeric_pattern, text)
                if numbers:
                    data['numeric_data'].extend(numbers)
            
            # Look for common betting/game elements
            game_keywords = ['bet', 'stake', 'win', 'multiplier', 'cashout', 'aviator', 'flight']
            for text in data['text_content']:
                if any(keyword in text.lower() for keyword in game_keywords):
                    data['game_elements'].append(text)
            
            data['timestamps'].append(time.time())
            
        except Exception as e:
            print(f"Error extracting visible data: {e}")
        
        return data
    
    def capture_network_requests(self, driver):
        """Capture and analyze network requests"""
        network_data = {
            'requests': [],
            'api_calls': [],
            'websocket_messages': []
        }
        
        try:
            # Get performance logs
            logs = driver.get_log('performance')
            
            for log in logs[-50:]:  # Last 50 requests
                message = json.loads(log['message'])
                message_info = message.get('message', {})
                
                if message_info.get('method') == 'Network.requestWillBeSent':
                    request = message_info.get('params', {})
                    url = request.get('request', {}).get('url', '')
                    
                    request_data = {
                        'url': url,
                        'method': request.get('request', {}).get('method', ''),
                        'headers': request.get('request', {}).get('headers', {}),
                        'timestamp': time.time()
                    }
                    
                    network_data['requests'].append(request_data)
                    
                    # Identify API calls
                    if any(api_indicator in url.lower() for api_indicator in 
                          ['api', 'json', 'data', 'ws', 'socket']):
                        network_data['api_calls'].append(request_data)
                
                # Capture WebSocket messages
                elif message_info.get('method') in ['Network.webSocketFrameSent', 
                                                   'Network.webSocketFrameReceived']:
                    ws_data = {
                        'type': message_info['method'],
                        'data': message_info.get('params', {}),
                        'timestamp': time.time()
                    }
                    network_data['websocket_messages'].append(ws_data)
        
        except Exception as e:
            print(f"Error capturing network data: {e}")
        
        return network_data
    
    def extract_specific_element(self, driver, css_selector):
        """Extract data from specific CSS selector"""
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
            return [element.text for element in elements if element.text]
        except:
            return []