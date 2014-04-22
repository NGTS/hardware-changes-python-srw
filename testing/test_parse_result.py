from werkzeug import ImmutableMultiDict
from hardware_changes.models import Camera
import pytest

@pytest.fixture
def response():
    return ImmutableMultiDict([
        ('dismounted_camera_0', u'1'),
        ('username', u'Simon'),
        ('pillar_1', u'S3'),
        ('pillar_0', u'N4'),
        ('comments', u'Comment'),
        ('submit-time', u'2014-04-22T14:56:27.993Z'),
        ('change-date', u'2014-04-22'),
        ('camera_id_1', u'13342'),
        ('camera_id_0', u'14028'),
        ])

@pytest.fixture
def parsed(response):
    return Camera.parse_response(response)

def test_camera_correct_length(parsed):
    assert len(parsed) == 2

def test_correct_response_types(parsed):
    for every in parsed:
        assert isinstance(every, Camera)

