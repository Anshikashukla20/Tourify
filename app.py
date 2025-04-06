from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import os

app = Flask(__name__)  # Corrected here
app.secret_key = 'your_secret_key'  # Change this in production

# Dummy course data
certificates = [
    "Sustainable Tourism Management",
    "Cultural and Heritage Tourism",
    "Eco-Tourism and Nature Guide",
    "Hospitality and Customer Service in Tourism",
    "Adventure and Recreational Tourism"
]

# Database setup
def init_db():
    conn = sqlite3.connect('tourism.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 email TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Home Route
@app.route('/')
def home():
    return redirect('/login')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conn = sqlite3.connect('tourism.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = sqlite3.connect('tourism.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = user[0]
            return redirect('/dashboard')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', certificates=certificates)

# Certificate Detail Page
@app.route('/certificate/<name>')
def certificate(name):
    if 'username' not in session:
        return redirect('/login')
    return render_template('certificate.html', name=name)

# Quiz Page
@app.route('/quiz/<name>', methods=['GET', 'POST'])
def quiz(name):
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer and answer.strip() == '10':  # Dummy correct answer
            return redirect(url_for('certificate_result', name=name))
        else:
            return "Incorrect answer. Try again."
    return render_template('quiz.html', name=name)

# ✅ Certificate Result Page
@app.route('/certificate-result/<name>')
def certificate_result(name):
    if 'username' not in session:
        return redirect('/login')
    return render_template('certificate-result.html', name=name, username=session['username'])

# ✅ Certificate Download (Dummy)
@app.route('/download-certificate/<name>')
def download_certificate(name):
    dummy_path = 'certificate.txt'
    with open(dummy_path, 'w') as f:
        f.write(f"Certificate of Completion\n\nThis is to certify that {session['username']} has completed the course: {name}.")
    return send_file(dummy_path, as_attachment=True, download_name=f"{name}_certificate.txt")

# Run App
if __name__ == '__main__':
    app.run(debug=True)
