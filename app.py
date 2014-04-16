from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

class SafeHTML(object):
    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class RenderView(object):
    env = Environment(autoescape=False, loader=PackageLoader(__name__))

class DatabaseStore(object):
    pass

class Camera(RenderView, DatabaseStore):

    IDS = range(14440, 14440+13)

    def __init__(self, form_id):
        self.form_id = form_id

    def render(self):
        template = self.env.get_template("camera_settings.html")
        return SafeHTML(template.render(camera=self))


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_form/', methods=['POST'])
def add_new_form():
    print request
    form_id = request.form['form_id']
    print "Form id {}".format(form_id)
    return render_template("form_template.html", form_id=form_id,
            camera=Camera(form_id))

@app.route('/add_change/', methods=['POST'])
def add_change():
    return redirect('/')

@app.route('/submit_changes/', methods=['POST'])
def submit_changes():
    print "Parsing changes"
    form = request.form
    return str(form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
