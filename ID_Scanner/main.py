from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

# Example admin ID (you can change this to any string you want)
ADMIN_ID = "admin123"

# Initialize Flask app
app = Flask(__name__, template_folder='Templates', static_folder='Static')

# Set the upload folder for storing files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Example data (would normally be stored in a database or similar persistent storage)
data = [
    ['112251', 'item123.jpg', 'item456.png'],
    ['123456', 'item789.pdf'],
    ['789101', 'item234.jpg', 'item567.png']
]

# Route for the admin login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Get the admin ID from the form
        admin_id = request.form.get('admin_id')

        # Check if the admin ID is correct
        if admin_id == ADMIN_ID:
            # Redirect to the admin page with the correct ID as a query parameter
            return redirect(url_for('admin', id=admin_id))  # Pass admin ID in the query string
        else:
            return "Invalid admin ID. Please try again.", 403

    return render_template('admin_login.html')

# Route for the admin page
@app.route('/admin')
def admin():
    # Get the admin ID from the query parameters
    admin_id = request.args.get('id')  # This retrieves the 'id' query parameter

    # Check if the admin ID is correct
    if admin_id == ADMIN_ID:
        # Return admin page with current data
        return render_template('admin.html', data=data)
    else:
        return "Unauthorized access. Please provide a valid admin ID.", 403

# Route for the home page (public access)
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle file submission (student borrowing or returning)
@app.route('/borrow_return', methods=['POST'])
def borrow_return():
    student_id = request.form['student_id']
    action = request.form['action']
    item_file = request.files['item_id']

    # Save the uploaded file to the UPLOAD_FOLDER
    if item_file:
        filename = item_file.filename
        item_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Update the data (this would normally interact with a database)
    if action == 'b':  # Borrow
        data.append([student_id, filename])
    elif action == 'r':  # Return
        for student in data:
            if student[0] == student_id and filename in student:
                student.remove(filename)

    return redirect(url_for('home'))

# Route to serve the uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)