from jinja2 import Environment, PackageLoader

class SafeHTML(object):

    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class RenderView(object):

    env = Environment(autoescape=False, loader=PackageLoader(__name__))

    def __init__(self, form_id):
        self.form_id = form_id


class Camera(RenderView):

    BLANK_CAMERA_ID = "blank-camera"
    IDS = sorted([
            13338,
            13339,
            13340,
            13341,
            13342,
            14028,
            14029,
            14030,
            14031,
            14032,
            14033,
            14034,
            14035,
            ])

    def __init__(self, form_id):
        super(Camera, self).__init__(form_id)

    def render(self):
        template = self.env.get_template("camera_settings.html")
        return SafeHTML(template.render(camera=self))

class Pillar(RenderView):

    BLANK_PILLAR_ID = "blank-pillar"
    IDS = sorted(map(lambda s: s.upper(), [
        "N1",
        "N2",
        "N3",
        "N4",
        "N5",
        "N6",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
        ]))

    def __init__(self, form_id):
        super(Pillar, self).__init__(form_id)

    def render(self):
        template = self.env.get_template("pillar_settings.html")
        return SafeHTML(template.render(pillar=self))

class Mount(RenderView):
    def __init__(self, form_id):
        super(Mount, self).__init__(form_id)

    def render(self):
        template = self.env.get_template("mount_settings.html")
        return SafeHTML(template.render(pillar=self))

