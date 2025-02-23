from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required

from app.config import Config
from app.controllers.auth import auth_bp
from app.controllers.flight import flight_bp

app = Flask(__name__, static_folder='templates/static', template_folder='templates')
app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'jwt'


jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')


app.register_blueprint(flight_bp, url_prefix='/api/')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
