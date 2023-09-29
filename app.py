from flask import Flask, render_template, request, jsonify
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('pdf_files')
    result_messages = []

    for file in files:
        try:
            pdf = PyPDF2.PdfFileReader(file)
            num_pages = pdf.getNumPages()
            result_messages.append(f'File: {file.filename}, Pages: {num_pages}')
        except PyPDF2.PdfFileReaderError:
            result_messages.append(f'Error reading {file.filename}')

    return jsonify({'message': '<br>'.join(result_messages)})

if __name__ == '__main__':
    app.run(debug=True)
