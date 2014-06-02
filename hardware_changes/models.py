from jinja2 import Environment, PackageLoader
from .form_types import Boolean, Integer
from functools import total_ordering

class SafeHTML(object):

    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class RenderView(object):

    env = Environment(autoescape=False, loader=PackageLoader(__name__))

    def render(self):
        template = self.env.get_template(self.TEMPLATE)
        return SafeHTML(template.render(subject=self))

    @classmethod
    def with_form_id(cls, form_id):
        subject = cls()
        subject.form_id = form_id
        return subject

@total_ordering
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
    TEMPLATE = "camera_settings.html"

    FORM_TYPES = {
            'dismounted_camera': Boolean,
            'camera_id': Integer,
            'form_id': Integer,
            }

    def __init__(self):
        self.form_keys = {}

    @classmethod
    def parse_response(cls, response):
        out = []
        camera_keys = [key for key in response if 'camera' in key]

        for camera_index in range(len(cls.IDS)):
            current_camera = []
            for key in camera_keys:
                if str(camera_index) in key:
                    current_camera.append((key[:-2], response[key]))

            if len(current_camera) > 0:
                camera = cls.build_camera(camera_index, current_camera)
                out.append(camera)

        return out

    @classmethod
    def build_camera(cls, form_id, current_camera):
        camera = cls.with_form_id(form_id)
        for (key, value) in current_camera:
            camera.form_keys[key] = cls.FORM_TYPES[key](value)

        camera.camera_id = camera.form_keys['camera_id']
        return camera

    def __le__(self, other):
        return self.form_id < other.form_id


    def __str__(self):
        return "<Camera id: {0}>".format(self.camera_id)

    def __repr__(self):
        return str(self)



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
    TEMPLATE = "pillar_settings.html"

class Mount(RenderView):

    TEMPLATE = "mount_settings.html"

class Focuser(RenderView):

    TEMPLATE = "focuser_settings.html"

class Telescope(RenderView):

    TEMPLATE = "telescope_settings.html"
