from flask import Flask, render_template, request, redirect

from hardware_changes.models import Camera, Pillar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_form/', methods=['POST'])
def add_new_form():
    form_id = request.form['form_id']
    return render_template("form_template.html", form_id=form_id,
            camera=Camera(form_id), pillar=Pillar(form_id))

@app.route('/add_change/', methods=['POST'])
def add_change():
    return redirect('/')

@app.route('/submit_changes/', methods=['GET', 'POST'])
def submit_changes():
    if request.method == 'POST':
        form = request.form
        return render_template("results.html", results=form)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
