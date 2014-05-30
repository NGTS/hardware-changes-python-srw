import MySQLdb
import datetime
import random
import time
import os
import unittest
import pytest

from hardware_changes.datastore import get_id, update, DatabaseIntegrityError

connection = MySQLdb.connect(host='sirius.astro.warwick.ac.uk', db='ngts_hwlog', user='sw')
camera_names = [800 + value for value in xrange(1, 14)]
telescope_names = range(1, 13)

def clean_database():
    '''
    Function to remove the database data, and build it up again from scratch.

    This is stored in the sql script `hardware_changes/data/schema.sql`
    '''
    print("Cleaning database")
    os.system("mysql -u sw -h sirius.astro.warwick.ac.uk -t < hardware_changes/data/schema.sql")
    print("Done")

def print_status(cursor):
    '''
    Retrieve the history for the camera_telescope relation, and the current location
    '''
    cursor.execute('''select * from camera_telescope_history order by camera_id''')
    for row in cursor:
        print row

    print "Current information"
    cursor.execute('''select camera_name, telescope_name, camera_telescope.start_date
            from camera
            join camera_telescope on (camera.id = camera_telescope.camera_id)
            join telescope on (camera_telescope.telescope_id = telescope.id)
            order by camera_name''')
    for row in cursor:
        print "Camera {}, telescope {}, started {}".format(*row)
    print

class TestDataStore(unittest.TestCase):
    def setUp(self):
        clean_database()

        # Insert all of the cameras
        with connection as cursor:
            cursor.executemany('''insert into camera (camera_name) values (%s)''',
                    [(c, ) for c in camera_names])
            cursor.executemany('''insert into telescope (telescope_name) values (%s)''',
                    [(t, ) for t in telescope_names])

    def test_all_code(self):
        update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with connection as cursor:
            print_status(cursor)

        update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with connection as cursor:
            print_status(cursor)

        update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with connection as cursor:
            print_status(cursor)

        update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with connection as cursor:
            print_status(cursor)

        print "Running interrupt"
        try:
            update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names),
                    update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0),
                    interrupt=True)
        except RuntimeError:
            pass
        with connection as cursor:
            print_status(cursor)

        for i in xrange(100):
            update(connection.cursor(), random.choice(camera_names), random.choice(telescope_names))

        with connection as cursor:
            print_status(cursor)

    def test_inserting_bad_camera_check_in_interface(self):
        bad_camera_id = 10101
        assert bad_camera_id not in camera_names
        with pytest.raises(DatabaseIntegrityError):
            update(connection.cursor(), bad_camera_id, random.choice(telescope_names))

