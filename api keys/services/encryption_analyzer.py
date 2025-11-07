import re
import json
import base64
from selenium.webdriver.common.by import By

class EncryptionAnalyzer:
    def __init__(self):
        self.encryption_patterns = {
            'aes': r'AES|CBC|ECB|CTR|GCM',
            'rsa': r'RSA|PKCS|OAEP',
            'base64': r'[A-Za-z0-9+/]{20,}={0,2}',
            'hex': r'[0-9A-Fa-f]{16,}',
            'json_web_token': r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9._-]*\.[A-Za-z0-9._-]*'
        }
    
    def analyze_encryption(self, driver):
        """Analyze potential encryption in the page"""
        analysis = {
            'encryption_indicators': [],
            'suspicious_strings': [],
            'javascript_analysis': {},
            'potential_keys': []
        }
        
        try:
            # Analyze JavaScript files for encryption patterns
            scripts = driver.find_elements(By.TAG_NAME, 'script')
            
            for i, script in enumerate(scripts):
                script_src = script.get_attribute('src')
                script_content = script.get_attribute('innerHTML')
                
                if script_content:
                    js_analysis = self.analyze_javascript_content(script_content)
                    if js_analysis:
                        analysis['javascript_analysis'][f'script_{i}'] = js_analysis
            
            # Analyze page source
            page_source = driver.page_source
            analysis.update(self.analyze_page_source(page_source))
            
        except Exception as e:
            print(f"Error in encryption analysis: {e}")
        
        return analysis
    
    def analyze_javascript_content(self, content):
        """Analyze JavaScript content for encryption patterns"""
        findings = {}
        
        for pattern_name, pattern in self.encryption_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                findings[pattern_name] = list(set(matches))[:5]  # Limit to 5 unique matches
        
        # Look for potential API keys and secrets
        key_patterns = {
            'api_key': r'api[_-]?key["\']?\s*:\s*["\']([^"\']+)["\']',
            'secret': r'secret["\']?\s*:\s*["\']([^"\']+)["\']',
            'token': r'token["\']?\s*:\s*["\']([^"\']+)["\']'
        }
        
        for key_type, key_pattern in key_patterns.items():
            matches = re.findall(key_pattern, content, re.IGNORECASE)
            if matches:
                findings[key_type] = matches[:3]  # Limit to 3 matches
        
        return findings if findings else None
    
    def analyze_page_source(self, page_source):
        """Analyze HTML page source for encryption indicators"""
        analysis = {
            'encryption_indicators': [],
            'suspicious_strings': []
        }
        
        # Look for base64 encoded data
        base64_pattern = r'["\']([A-Za-z0-9+/]{20,}={0,2})["\']'
        base64_matches = re.findall(base64_pattern, page_source)
        
        for match in base64_matches[:10]:  # Limit to 10 matches
            try:
                # Try to decode to verify it's valid base64
                decoded = base64.b64decode(match)
                if len(decoded) > 5:  # Meaningful data
                    analysis['suspicious_strings'].append({
                        'type': 'base64',
                        'encoded': match[:50] + '...' if len(match) > 50 else match,
                        'decoded_length': len(decoded)
                    })
            except:
                pass
        
        return analysis
    
    def deep_analysis(self, target_url):
        """Perform deep encryption analysis"""
        # This would involve more sophisticated analysis
        # including dynamic JavaScript execution analysis
        return {
            'status': 'deep_analysis_required',
            'message': 'Use browser devtools for detailed encryption analysis',
            'recommended_steps': [
                "1. Open Chrome DevTools (F12)",
                "2. Go to Network tab and reload page",
                "3. Look for XHR/Fetch requests with encrypted payloads",
                "4. Check Sources tab for JavaScript encryption functions",
                "5. Search for 'encrypt', 'decrypt', 'CryptoJS' in source code"
            ]
        }