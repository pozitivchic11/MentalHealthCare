from flask import Blueprint, render_template, request, jsonify
from backend.src.signup import register_user
from backend.src.login import login_user

home_page_routes = Blueprint('api', __name__)


@home_page_routes.route('/')
def home_page():
    return render_template('index.html')


@home_page_routes.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    http_status = login_user(data.get('email'), data.get('password'))

    return jsonify({'message': 'User logged in successfully!'}), http_status

@home_page_routes.route('/signup', methods=['POST'])

def signup():
    data = request.get_json()
    http_status = register_user(data.get('name'), data.get('surname'), data.get('email'), data.get('password'))

    return jsonify({'message': 'User created successfully!'}), http_status

@home_page_routes.route('/test')

def test_page():
    return render_template('test.html')
