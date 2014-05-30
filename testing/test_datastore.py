import MySQLdb
import datetime
import random
import time
import os
import unittest
import pytest

from hardware_changes.datastore import get_id, update, DatabaseIntegrityError

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
        self.connection = MySQLdb.connect(host='sirius.astro.warwick.ac.uk', db='ngts_hwlog', user='sw')

        self.camera_names = [800 + value for value in xrange(1, 14)]
        self.telescope_names = range(1, 13)

        clean_database()

        # Insert all of the cameras
        with self.connection as cursor:
            cursor.executemany('''insert into camera (camera_name) values (%s)''',
                    [(c, ) for c in self.camera_names])
            cursor.executemany('''insert into telescope (telescope_name) values (%s)''',
                    [(t, ) for t in self.telescope_names])

    def random_camera(self):
        return random.choice(self.camera_names)

    def random_telescope(self):
        return random.choice(self.telescope_names)

    def test_all_code(self):
        update(self.connection.cursor(), self.random_camera(), self.random_telescope(),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with self.connection as cursor:
            print_status(cursor)

        update(self.connection.cursor(), self.random_camera(), self.random_telescope(),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with self.connection as cursor:
            print_status(cursor)

        update(self.connection.cursor(), self.random_camera(), self.random_telescope(),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with self.connection as cursor:
            print_status(cursor)

        update(self.connection.cursor(), self.random_camera(), self.random_telescope(),
                update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0))
        with self.connection as cursor:
            print_status(cursor)

        print "Running interrupt"
        try:
            update(self.connection.cursor(), self.random_camera(), self.random_telescope(),
                    update_time = lambda: datetime.datetime(2013, 10, 5, 0, 0, 0),
                    interrupt=True)
        except RuntimeError:
            pass
        with self.connection as cursor:
            print_status(cursor)

        for i in xrange(100):
            update(self.connection.cursor(), self.random_camera(), self.random_telescope())

        with self.connection as cursor:
            print_status(cursor)

    def test_inserting_bad_camera_check_in_interface(self):
        bad_camera_id = 10101
        assert bad_camera_id not in self.camera_names
        with pytest.raises(DatabaseIntegrityError):
            update(self.connection.cursor(), bad_camera_id, self.random_telescope())

    def test_inserting_bad_camera_check_in_database(self):
        '''
        This test has to bypass the interface, and checks the triggers from the database
        validations
        '''
        with pytest.raises(MySQLdb.OperationalError) as err:
            with self.connection as cursor:
                cursor.execute('''insert into camera_telescope_history
                (camera_id, telescope_id, start_date)
                values (10101, 2, "2010-02-05 15:00:00")''')

            assert str(err) == 'Invalid camera id given'
