import os
import pandas as pd
from flask import Flask, request, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Analyze CSV
    df = pd.read_csv(filepath)
    summary = df.describe().round(2)

    # Create PDF report
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf')
    generate_pdf(summary, pdf_path)

    return send_file(pdf_path, as_attachment=True)

def generate_pdf(summary, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "CSV Data Summary Report")
    y = 720

    for col in summary.columns:
        c.drawString(30, y, f"Column: {col}")
        y -= 20
        for stat in summary.index:
            val = summary[col][stat]
            c.drawString(50, y, f"{stat}: {val}")
            y -= 15
        y -= 10

    c.save()

if __name__ == '__main__':
    app.run(debug=True)
