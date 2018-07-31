from flask import Flask
from flask import render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/CV')
def CV():
    return render_template('CV.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/sudoku_solver', methods=['GET', 'POST'])
def solve_sudoku():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+"/"+filename)
            return redirect(url_for('sudoku_solution', filename=filename))



    return render_template('Sudoku.html')


@app.route('/sudoku_solution/<filename>')
def sudoku_solution(filename):
    file = "uploads/"+filename
    render_template('Sudoku.html', file=filename, filepath=file, wait=True)
    time.sleep(20)
    return render_template('Sudoku.html', file=filename, filepath=file)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
