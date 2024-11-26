import os
from flask import Flask, render_template_string, request, redirect, url_for
import qrcode
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Define the CSV file path
CSV_FILE = 'student_data.csv'
FEEDBACK_FILE = 'feedback_data.csv'

if not os.path.exists(FEEDBACK_FILE):
    feedback_df = pd.DataFrame(columns=["Student ID", "Feedback", "Timestamp"])
    feedback_df.to_csv(FEEDBACK_FILE, index=False)

# Create CSV file with header if it does not exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Student ID", "Timestamp"])
    df.to_csv(CSV_FILE, index=False)

# Ensure the 'static' folder exists for saving QR codes
if not os.path.exists('static'):
    os.makedirs('static')

# HTML template for the homepage (QR code page)
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code for Student Data Entry</title>
</head>
<body>
    <h1>Scan the QR Code to Enter Your Details</h1>

    <!-- Display QR Code Image -->
    <img src="{{ url_for('static', filename=qr_code_filename) }}" alt="QR Code" width="200">

    <p>Scan the QR code or click <a href="{{ url_for('form') }}">here</a> to enter your details manually.</p>
</body>
</html>
'''

# HTML template for the student data entry form
form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Data Entry</title>
</head>
<body>
    <h1>Enter Your Details</h1>

    <form action="{{ url_for('form') }}" method="POST">
        <label for="name">Name:</label>
        <input type="text" name="name" required><br><br>

        <label for="student_id">Student ID:</label>
        <input type="text" name="student_id" required><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

# HTML template for the feedback form
feedback_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Form</title>
</head>
<body>
    <h1>We Value Your Feedback!</h1>

    <form action="{{ url_for('feedback') }}" method="POST">
        <label for="student_id">Student ID:</label>
        <input type="text" name="student_id" required><br><br>

        <label for="feedback">Feedback:</label><br>
        <textarea name="feedback" rows="4" cols="50" required></textarea><br><br>

        <button type="submit">Submit Feedback</button>
    </form>
</body>
</html>
'''
# HTML template for the thank you page
thank_you_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You</title>
</head>
<body>
    <h1>Thank You for Submitting Your Details!</h1>
    <p>Your data has been successfully saved.</p>
    <a href="/">Go back to the homepage</a>
    <a href="/feedback">Submit Your Feedback</a>

</body>
</html>
'''

# HTML template for the thank you page after feedback
thank_you_feedback_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You</title>
</head>
<body>
    <h1>Thank You for Your Feedback!</h1>
    <p>Your feedback has been successfully saved.</p>
    <a href="/">Go back to the homepage</a>
</body>
</html>
'''

@app.route('/')
def index():
    # Generate the QR code that links to the form page
    form_url = "https://25c00628-ed16-4b87-8909-37f01bcf3a98-00-2cxdzekuet8g4.kirk.replit.dev/form"
    qr_code = qrcode.make(form_url)
    qr_code_filename = 'qrcode.png'

    # Ensure the 'static' directory is empty and doesn't have a file with the same name
    qr_code_path = os.path.join('static', qr_code_filename)
    if os.path.exists(qr_code_path):
        os.remove(qr_code_path)

    # Save the QR code in the 'static' folder
    qr_code.save(qr_code_path)

    return render_template_string(index_html, qr_code_filename = qr_code_filename)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Debugging: print form data to the console to check what is coming from the form
        print(f"Form Data: {request.form}")

        # Ensure the form has 'name' and 'student_id' fields
        if 'name' not in request.form or 'student_id' not in request.form:
            return 'Missing form data', 400  # Return a Bad Request error if any key is missing

        # Get the form data
        name = request.form['name']
        student_id = request.form['student_id']
        # Load the current CSV data
        df = pd.read_csv(CSV_FILE)

        # Check if the student ID already exists for the current session
        if ((df['Name'] == name) & (df['Student ID'] == student_id)).any():
            # If an entry with the same name and student ID exists, return a duplicate message
            return 'Duplicate entry detected. You have already submitted your details.', 400

        # If no duplicate entry exists, add the new data
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_data = pd.DataFrame({"Name": [name], "Student ID": [student_id], "Timestamp": [timestamp]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        # Redirect to thank you page after saving data
        return redirect(url_for('thank_you'))

    return render_template_string(form_html)

@app.route('/thank_you')
def thank_you():
    return render_template_string(thank_you_html)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Get the feedback form data
        student_id = request.form['student_id']
        feedback_text = request.form['feedback']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save the feedback to CSV
        feedback_df = pd.read_csv(FEEDBACK_FILE)
        new_feedback = pd.DataFrame({"Student ID": [student_id], "Feedback": [feedback_text], "Timestamp": [timestamp]})
        feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
        feedback_df.to_csv(FEEDBACK_FILE, index=False)

        # Redirect to thank you page after saving feedback
        return render_template_string(thank_you_feedback_html)

    return render_template_string(feedback_html)

if __name__ == '__main__':
    app.run(debug=True)
