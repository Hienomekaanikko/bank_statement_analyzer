from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF

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
            pdf_document = fitz.open(file.stream)
            num_pages = pdf_document.page_count
            text = ""

            # Extract text from each page and concatenate it
            for page_num in range(num_pages):
                page = pdf_document[page_num]
                text += page.get_text()

            result_messages.append(f'File: {file.filename}, Pages: {num_pages}')
            result_messages.append(f'Text from {file.filename}:\n{text}')
        except Exception as e:
            result_messages.append(f'Error reading {file.filename}: {str(e)}')

    return jsonify({'message': '<br>'.join(result_messages)})

if __name__ == '__main__':
    app.run(debug=True)
