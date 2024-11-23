import secrets
from flask import Flask
from datetime import timedelta
from backend.routes.home_page_routes import home_page_routes

app = Flask(__name__, template_folder='backend/templates', static_folder='frontend')

app.secret_key = secrets.token_hex(32)
app.permanent_session_lifetime = timedelta(days=1)

app.register_blueprint(home_page_routes)

if __name__ == '__main__':
    app.run(debug=True)
