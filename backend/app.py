from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from flask_bcrypt import Bcrypt
from stegano import embed_data, extract_data, calculate_capacity
from auth import create_user, verify_user, init_db
from PIL import Image
import io
import os

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB limit
bcrypt = Bcrypt(app)
init_db()

# ========== Routes ==========
@app.route('/')
def index():
    return redirect(url_for('register_page'))

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return "Username/password cannot be empty", 400

    if create_user(username, password):
        return redirect(url_for('login_page'))
    return "Username already exists", 409

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if verify_user(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return "Invalid credentials", 401

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('home.html', username=session['username'])

@app.route('/embed', methods=['GET', 'POST'])
def embed():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        return render_template('embed.html')

    try:
        image = request.files['image']
        message = request.form.get('message', '')
        password = request.form.get('password', '')

        img = Image.open(image.stream).convert('RGB')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        stego_img = embed_data(img_bytes, message, password)

        output = io.BytesIO()
        stego_img.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png', download_name='secret.png')
    except Exception as e:
        return str(e), 400

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        return render_template('extract.html')

    try:
        image = request.files['image']
        password = request.form.get('password', '')
        message = extract_data(image.stream, password)
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/capacity', methods=['POST'])
def capacity():
    try:
        image = request.files['image']
        img_bytes = io.BytesIO(image.read())
        capacity = calculate_capacity(img_bytes)
        return jsonify({'capacity': capacity})
    except:
        return jsonify({'error': 'Invalid image'}), 400

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)