import requests
from flask import Flask, send_from_directory, render_template_string, request
import importlib.util
import os

# Load API_KEY from defaults.cfg
app = Flask(__name__)
app.config.from_pyfile('default.cfg', silent=True)
app.config['API_KEY'] = os.environ.get('API_KEY', app.config.get('API_KEY', ''))
api_key = app.config['API_KEY']

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/swagger.json')
def swagger_json():
    return send_from_directory('.', 'swagger.json')

@app.route('/docs')
def swagger_ui():
    # Embed Swagger UI from CDN and point it to /swagger.json
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Swagger UI</title>
      <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
      <script>
        window.onload = function() {
          SwaggerUIBundle({
            url: '/swagger.json',
            dom_id: '#swagger-ui',
          });
        };
      </script>
    </body>
    </html>
    ''')

@app.route('/exchanges')
def exchanges():
    url = "https://live.trading212.com/api/v0/equity/metadata/exchanges"
    headers = {"Authorization": api_key}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        exchanges = resp.json()
    except Exception as e:
        return f"Error fetching exchanges: {e}", 500
    # Render a simple HTML table
    return render_template_string('''
    <h1>Exchange List</h1>
    {% if exchanges %}
    <table border="1" cellpadding="5">
      <tr><th>ID</th><th>Name</th></tr>
      {% for ex in exchanges %}
        <tr><td>{{ ex.id }}</td><td>{{ ex.name }}</td></tr>
      {% endfor %}
    </table>
    {% else %}
      <p>No exchanges found.</p>
    {% endif %}
    ''', exchanges=exchanges)

if __name__ == '__main__':
    app.run(debug=True)