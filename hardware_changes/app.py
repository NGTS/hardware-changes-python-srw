from flask import Flask, render_template, request, redirect

from hardware_changes.models import Camera, Pillar, Mount, Focuser, Telescope

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_form/', methods=['POST'])
def add_new_form():
    form_id = request.form['form_id']
    return render_template("form_template.html",
            form_id=form_id,
            camera=Camera.with_form_id(form_id),
            pillar=Pillar.with_form_id(form_id),
            mount=Mount.with_form_id(form_id),
            focuser=Focuser.with_form_id(form_id),
            telescope=Telescope.with_form_id(form_id)
            )

def to_json(form):
    """
    Given form parameters as a dictionary, convert to a nested JSON structure for easier parsing
    """
    n_pillars = len(Pillar.IDS)

    out = {}
    for i in range(n_pillars):
        included_keys = [(key, form[key]) for key in form if key.endswith(str(i))]
        if len(included_keys):
            out[i] = included_keys

    def is_valid_integer(char):
        try:
            out = int(char)
        except ValueError:
            return False
        else:
            return True

    out['meta'] = []
    for key in form:
        if not is_valid_integer(key[-1]):
            out['meta'].append((key, form[key]))
    return out

@app.route('/add_change/', methods=['POST'])
def add_change():
    return redirect('/')

@app.route('/submit_changes/', methods=['GET', 'POST'])
def submit_changes():
    if request.method == 'POST':
        form = request.form
        converted = to_json(form)
        return render_template("results.html", results=converted)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
