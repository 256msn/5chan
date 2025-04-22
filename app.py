from flask import Flask, request, redirect, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

threads = []
replies = {}

@app.route('/')
def index():
    return render_template('index.html', threads=threads)

@app.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    thread = next((t for t in threads if t['id'] == thread_id), None)
    if not thread:
        return "Thread not found", 404
    thread_replies = replies.get(thread_id, [])
    return render_template('thread.html', thread=thread, replies=thread_replies)

@app.route('/post_thread', methods=['POST'])
def post_thread():
    title = request.form['title']
    message = request.form['message']
    image = request.files['image']
    filename = ''
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    thread_id = len(threads) + 1
    threads.append({'id': thread_id, 'title': title, 'message': message, 'image': filename})
    return redirect('/')

@app.route('/post_reply/<int:thread_id>', methods=['POST'])
def post_reply(thread_id):
    message = request.form['message']
    image = request.files['image']
    filename = ''
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if thread_id not in replies:
        replies[thread_id] = []
    replies[thread_id].append({'message': message, 'image': filename})
    return redirect(f'/thread/{thread_id}')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
