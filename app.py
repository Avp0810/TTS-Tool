from flask import Flask, render_template, request, redirect, url_for, flash
import os
import PyPDF2
import pdfplumber

app = Flask(__name__)

# Secret key for session management (used for flashing messages)
app.secret_key = 'your_secret_key'

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Home route that renders the upload form
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        flash('No file part in the request.')
        return redirect(url_for('index'))

    file = request.files['pdf_file']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('index'))

    if file and file.filename.lower().endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_path)

        # Remove the uploaded file after processing
        os.remove(file_path)

        # Pass the extracted text to the result page
        return render_template('result.html', extracted_text=extracted_text)
    else:
        flash('Invalid file type. Please upload a PDF file.')
        return redirect(url_for('index'))


# Function to extract text from the uploaded PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text


if __name__ == '__main__':
    app.run(debug=True)


git remote add origin https://github.com/Avp0810/TTS-Tool
git push -u origin master
