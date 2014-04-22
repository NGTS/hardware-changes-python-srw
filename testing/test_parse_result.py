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

@pytest.fixture
def camera1(parsed):
    return sorted(parsed)[0]

@pytest.fixture
def camera2(parsed):
    return sorted(parsed)[1]

def test_camera_correct_length(parsed):
    assert len(parsed) == 2

def test_correct_response_types(parsed):
    for every in parsed:
        assert isinstance(every, Camera)

def test_correct_ids(parsed):
    assert sorted([c.camera_id.value for c in parsed]) == [13342, 14028]

def test_camera_one(camera1):
    assert 'dismounted_camera' in camera1.form_keys
    assert camera1.form_keys['dismounted_camera'] == True
    assert camera1.form_id == 0
    assert camera1.camera_id == 14028

def test_camera_two(camera2):
    assert camera2.form_id == 1
    assert camera2.camera_id == 13342

