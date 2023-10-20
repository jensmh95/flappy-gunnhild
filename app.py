from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_script', methods=['POST'])
def run_python_script():
    try:
        subprocess.run(['python', 'gunnhild.py'])
        return 'Python script executed successfully'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run()
