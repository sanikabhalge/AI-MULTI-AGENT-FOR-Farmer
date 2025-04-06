from flask import Flask, request, redirect, render_template
import subprocess
import json
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-agent', methods=['POST'])
def run_agent():
    # Get form data
    ph = request.form['ph']
    moisture = request.form['moisture']
    temp = request.form['temperature']
    rain = request.form['rainfall']
    

    # Trigger the agent using subprocess
    subprocess.Popen(['python3', 'main.py', ph, moisture, temp, rain])

    # Wait for the agent to finish and recommendation to be generated
    timeout = 10  # seconds
    waited = 0
    while waited < timeout:
        if os.path.exists('/data/recommendation.json'):
            break
        time.sleep(1)
        waited += 1

    return redirect('/result')

@app.route('/result')
def result():
    if os.path.exists('data/recommendation.json'):
        with open('data/recommendation.json') as f:
            data = json.load(f)
        if 'error' in data:
            return f"<h2>❌ {data['error']}</h2>"
        return render_template('result.html', crop=data['crop'], price=data['price'])
    else:
        return "<h2>⚠️ Recommendation not ready yet.</h2>"

if __name__ == '__main__':
    app.run(debug=True)
