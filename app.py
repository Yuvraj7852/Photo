from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import razorpay
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RAZORPAY_KEY_ID'] = 'rzp_test_YourKeyHere'
app.config['RAZORPAY_KEY_SECRET'] = 'your_secret_here'

client = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.files['photo']
    filename = secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', files=files, key_id=app.config['RAZORPAY_KEY_ID'])

@app.route('/pay', methods=['POST'])
def pay():
    amount = 1000  # ₹10 in paisa
    order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return order

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render को ये चाहिए
    app.run(host="0.0.0.0", port=port)
