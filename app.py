from flask import Flask
from backend.routes.home_page_routes import home_page_routes

app = Flask(__name__, template_folder='backend/templates')

app.register_blueprint(home_page_routes)

if __name__ == '__main__':
    app.run(debug=True)
