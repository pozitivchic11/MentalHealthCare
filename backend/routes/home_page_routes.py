import os
from flask import Blueprint, render_template, request, jsonify, Response
from backend.src.signup import register_user
from backend.src.login import login_user
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

home_page_routes = Blueprint('api', __name__)

# API Key and Available Models
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

MODELS = {
    'Llama3 70B': 'llama3-70b-8192',
    'Llama3 8B': 'llama3-8b-8192',
    'Mixtral': 'mixtral-8x7b-32768',
    'Gemma2': 'gemma2-9b-it'
}


@home_page_routes.route('/')
def home_page():
    """Render the homepage."""
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


@home_page_routes.route('/ai_assistant', methods=['GET', 'POST'])
def test_page():
    """Handle chatbot interaction."""
    if request.method == 'POST':
        selected_model = request.form.get('model')
        input_text = request.form.get('input_text')

        if not selected_model or not input_text:
            return "Please select a model and provide input text.", 400

        model_id = MODELS[selected_model]

        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a mental health assistant."},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9,
                stream=True
            )

            def generate_response():
                """Stream the response from Groq API."""
                result = ""
                for chunk in completion:
                    content = chunk.choices[0].delta.content or ""
                    result += content
                    yield content

            return Response(generate_response(), content_type='text/plain')

        except Exception as e:
            return f"An error occurred: {e}", 500

    return render_template('chatbot.html', models=MODELS)
