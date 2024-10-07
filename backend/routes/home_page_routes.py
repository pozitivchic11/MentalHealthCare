from flask import Blueprint, render_template, request, redirect, url_for

home_page_routes = Blueprint('api', __name__)

@home_page_routes.route('/')

def home_page():
    return render_template('index.html')
