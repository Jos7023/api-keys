class DataCollectorApp {
    constructor() {
        this.isCollecting = false;
        this.dataInterval = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('collectionForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startCollection();
        });

        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopCollection();
        });
    }

    async startCollection() {
        const targetUrl = document.getElementById('targetUrl').value;
        const interval = document.getElementById('collectionInterval').value;

        try {
            const response = await fetch('/start-collection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    target_url: targetUrl,
                    interval: parseInt(interval)
                })
            });

            const result = await response.json();

            if (result.status === 'success') {
                this.isCollecting = true;
                document.getElementById('startBtn').disabled = true;
                document.getElementById('stopBtn').disabled = false;
                
                this.startDataPolling();
                this.updateOutput('Data collection started successfully...');
            } else {
                this.updateOutput(`Error: ${result.message}`);
            }
        } catch (error) {
            this.updateOutput(`Error starting collection: ${error}`);
        }
    }

    async stopCollection() {
        try {
            const response = await fetch('/stop-collection', {
                method: 'POST'
            });

            this.isCollecting = false;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            
            clearInterval(this.dataInterval);
            this.updateOutput('Data collection stopped.');
        } catch (error) {
            this.updateOutput(`Error stopping collection: ${error}`);
        }
    }

    startDataPolling() {
        this.dataInterval = setInterval(async () => {
            if (this.isCollecting) {
                await this.fetchLatestData();
            }
        }, 2000);
    }

    async fetchLatestData() {
        try {
            const response = await fetch('/get-data');
            const data = await response.json();
            
            if (Object.keys(data).length > 0) {
                this.displayData(data);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    displayData(data) {
        const output = document.getElementById('dataOutput');
        const timestamp = new Date().toLocaleTimeString();
        
        let html = `
            <div class="data-item">
                <strong>Timestamp:</strong> ${timestamp}<br>
                <strong>Visible Data Points:</strong> ${data.visible_data?.text_content?.length || 0}<br>
                <strong>Numeric Values:</strong> ${data.visible_data?.numeric_data?.slice(0, 10).join(', ') || 'None'}<br>
                <strong>Network Requests:</strong> ${data.network_data?.requests?.length || 0}<br>
                <strong>API Calls:</strong> ${data.network_data?.api_calls?.length || 0}
            </div>
        `;

        // Add encryption analysis if available
        if (data.encryption_analysis && data.encryption_analysis.encryption_indicators.length > 0) {
            html += `
                <div class="data-item encryption-warning">
                    <strong>Encryption Indicators Found:</strong><br>
                    ${data.encryption_analysis.encryption_indicators.join(', ')}
                </div>
            `;
        }

        output.innerHTML = html + output.innerHTML;
        
        // Limit output length
        const items = output.getElementsByClassName('data-item');
        if (items.length > 20) {
            items[items.length - 1].remove();
        }
    }

    updateOutput(message) {
        const output = document.getElementById('dataOutput');
        const timestamp = new Date().toLocaleTimeString();
        output.innerHTML = `<div class="data-item"><strong>[${timestamp}]</strong> ${message}</div>` + output.innerHTML;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DataCollectorApp();
});