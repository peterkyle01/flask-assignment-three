import base64
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
uploaded_files = []  # List to store base64 encoded files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode('utf-8')
            uploaded_files.append({'filename': filename, 'base64': base64_encoded})
            return redirect(url_for('index'))
    return render_template('index.html', files=uploaded_files)

@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    if 0 <= index < len(uploaded_files):
        file_data = uploaded_files[index]
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_content = file.read()
                base64_encoded = base64.b64encode(file_content).decode('utf-8')
                uploaded_files[index] = {'filename': filename, 'base64': base64_encoded}
                return redirect(url_for('index'))
        return render_template('update.html', file=file_data, index=index)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(uploaded_files):
        del uploaded_files[index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)