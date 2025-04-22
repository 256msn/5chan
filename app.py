from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_threads():
    try:
        with open('threads.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_threads(threads):
    with open('threads.json', 'w') as f:
        json.dump(threads, f, indent=4)

@app.route('/')
def index():
    threads = load_threads()
    return render_template('index.html', threads=threads)

@app.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    threads = load_threads()
    thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread:
        return render_template('thread.html', thread=thread)
    return redirect(url_for('index'))

@app.route('/new_thread', methods=['GET', 'POST'])
def new_thread():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        image = request.files['image']
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"image_{timestamp}"
        image_path = None

        if image and allowed_file(image.filename):
            ext = image.filename.rsplit('.', 1)[1].lower()
            filename = f"{filename}.{ext}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        threads = load_threads()
        new_thread_id = len(threads) + 1
        new_thread = {
            'id': new_thread_id,
            'subject': subject,
            'posts': [{
                'author': 'Anonymous',
                'content': content,
                'image': filename if image_path else None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }],
            'last_bump': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        threads.append(new_thread)
        save_threads(threads)
        return redirect(url_for('view_thread', thread_id=new_thread_id))
    return render_template('post_form.html')

if __name__ == '__main__':
    app.run(debug=True)