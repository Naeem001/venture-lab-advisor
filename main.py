#!/usr/bin/env python3
"""
Venture Lab AI Founder Advisor
Durham University

Hosted on Replit — Flask version
"""

from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import urllib.error
import json
import os

app = Flask(__name__, static_folder='static')

# API key from Replit environment variable (set in Replit Secrets)
API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')


@app.route('/')
def index():
    """Serve the main HTML app"""
    return send_from_directory('static', 'index.html')


@app.route('/api', methods=['POST', 'OPTIONS'])
def proxy():
    """Proxy requests to Anthropic API — keeps key secure on server"""

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return resp

    if not API_KEY:
        return jsonify({
            'error': {
                'message': 'API key not configured. Add ANTHROPIC_API_KEY in Replit Secrets.'
            }
        }), 500

    body = request.get_data()

    try:
        req = urllib.request.Request(
            url='https://api.anthropic.com/v1/messages',
            data=body,
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-api-key', API_KEY)
        req.add_header('anthropic-version', '2023-06-01')

        with urllib.request.urlopen(req, timeout=30) as response:
            result = response.read()

        resp = app.response_class(
            response=result,
            status=200,
            mimetype='application/json'
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except urllib.error.HTTPError as e:
        err_body = e.read()
        resp = app.response_class(
            response=err_body,
            status=e.code,
            mimetype='application/json'
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 500


if __name__ == '__main__':
    # Replit uses port 5000 by default
    port = int(os.environ.get('PORT', 5000))
    print(f'\n  ✓ Venture Lab Advisor running on port {port}')
    print(  '  ✓ Open the Replit webview to see your app\n')
    app.run(host='0.0.0.0', port=port, debug=False)
