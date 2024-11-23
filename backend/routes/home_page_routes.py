from groq import Groq
from backend.src.login import login_user
from backend.src.signup import register_user
from flask import Blueprint, render_template, request, jsonify, Response, session, redirect, url_for

home_page_routes = Blueprint('api', __name__)

# API Key and Available Models
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

MODELS = {
    'Llama3 70B': 'llama3-70b-8192',
    'Llama3 8B': 'llama3-8b-8192',
    'Mixtral': 'mixtral-8x7b-32768',
    'Gemma2': 'gemma2-9b-it'
}

@home_page_routes.before_request
def make_session_permanent():
    session.permanent = True

@home_page_routes.route('/')
def home_page():
    """Render the homepage."""
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    return render_template('index.html', user_email=user_email, user_name=user_name)

@home_page_routes.before_request
def make_session_permanent():
    session.permanent = True

@home_page_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    user_name = login_user(email, password)

    if user_name:
        session['user_email'] = email
        session['user_name'] = user_name
        return jsonify({'message': 'User logged in successfully!'}), 200
    else:
        return jsonify({'message': 'Login failed!'}), 401

@home_page_routes.before_request
def make_session_permanent():
    session.permanent = True

@home_page_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')

    http_status = register_user(name, surname, email, password)
    if http_status == 201:
        session['user_email'] = email
        session['user_name'] = name
        return jsonify({'message': 'User created successfully!'}), 201
    else:
        return jsonify({'message': 'Signup failed!'}), http_status

@home_page_routes.before_request
def make_session_permanent():
    session.permanent = True

@home_page_routes.route('/logout', methods=['POST'])
def logout():
    """Log out the user by clearing their session."""
    session.clear()
    return redirect(url_for('api.home_page'))

@home_page_routes.before_request
def make_session_permanent():
    session.permanent = True

@home_page_routes.route('/ai_assistant', methods=['GET', 'POST'])
def ai_assistant_page():
    """Handle chatbot interaction."""
    user_email = session.get('user_email')
    user_name = session.get('user_name')

    if 'user_email' not in session:
        return redirect(url_for('api.home_page'))

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

    return render_template('chatbot.html', models=MODELS, user_email=user_email, user_name=user_name)
