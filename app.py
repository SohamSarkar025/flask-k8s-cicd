from flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, generate_latest
import socket

app = Flask(__name__)

# Prometheus custom metric counter
REQUEST_COUNT = Counter('request_count', 'Total HTTP Requests', ['endpoint'])

# Modern HTML Template for the Dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Pipeline Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #e2e8f0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #1e293b;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            max-width: 600px;
            text-align: center;
            border-top: 4px solid #38bdf8;
        }
        h1 {
            color: #38bdf8;
            margin-bottom: 5px;
        }
        h3 {
            color: #94a3b8;
            margin-top: 0;
            margin-bottom: 30px;
            font-weight: normal;
        }
        .card {
            background-color: #334155;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: left;
        }
        .card p {
            margin: 10px 0;
            font-size: 1.1em;
        }
        .card span.label {
            font-weight: bold;
            color: #cbd5e1;
            display: inline-block;
            width: 140px;
        }
        .status-badge {
            background-color: rgba(74, 222, 128, 0.2);
            color: #4ade80;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .btn-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 25px;
        }
        .btn {
            background-color: #0284c7;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #0369a1;
        }
        .footer {
            margin-top: 35px;
            font-size: 0.85em;
            color: #64748b;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Kubernetes CI/CD Pipeline</h1>
        <h3>Live Web Application Deployment</h3>
        
        <div class="card">
            <p><span class="label">Infrastructure:</span> AWS EC2 + Minikube</p>
            <p><span class="label">Pod Hostname:</span> {{ hostname }}</p>
            <p><span class="label">System Status:</span> <span class="status-badge">Online & Healthy</span></p>
        </div>

        <div class="btn-container">
            <a href="/health" class="btn">🩺 View Health</a>
            <a href="/metrics" class="btn">📊 View Metrics</a>
        </div>
        
        <div class="footer">
            System Operations & Verification Panel<br>
            Prepared for Linsa Chechi's review.
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    REQUEST_COUNT.labels(endpoint='/').inc()
    # Renders the HTML template and dynamically injects the container's hostname
    return render_template_string(HTML_TEMPLATE, hostname=socket.gethostname())

@app.route('/health')
def health():
    return jsonify(status="healthy", message="Application is running smoothly."), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
