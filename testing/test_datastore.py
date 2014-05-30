import MySQLdb
import datetime
import random
import time
import os
import unittest
import pytest

from hardware_changes.datastore import get_id, update, NGTSDatabaseIntegrityError

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


class TestDataStore(object):
    @classmethod
    def setup_class(cls):
        cls.connection = MySQLdb.connect(host='sirius.astro.warwick.ac.uk', db='ngts_hwlog', user='sw')

        cls.camera_names = [800 + value for value in xrange(1, 14)]
        cls.telescope_names = range(1, 13)

        clean_database()

        # Insert all of the cameras
        with cls.connection as cursor:
            cursor.executemany('''insert into camera (camera_name) values (%s)''',
                    [(c, ) for c in cls.camera_names])
            cursor.executemany('''insert into telescope (telescope_name) values (%s)''',
                    [(t, ) for t in cls.telescope_names])
            cls.connection.commit()

    @pytest.fixture
    def cursor(self):
        '''
        Fixture to build a cursor object, to allow for test rollback
        '''
        return self.connection.cursor()

    def teardown_method(self, method):
        '''
        Ensure no data remains for the next test
        '''
        print("Rolling back database state")
        self.connection.rollback()


    def random_camera(self):
        return random.choice(self.camera_names)

    def random_telescope(self):
        return random.choice(self.telescope_names)

    def camera_telescope_history_contents(self, cursor=None):
        cursor = cursor if cursor else self.connection.cursor()
        cursor.execute('''select camera_name, telescope_name, start_date, end_date
                from camera_telescope_history
                join camera on camera.id = camera_telescope_history.camera_id
                join telescope on telescope.id = camera_telescope_history.telescope_id
                order by start_date asc''')
        return cursor.fetchall()

    def test_update_succeeds(self, cursor):
        camera = self.random_camera()
        telescope = self.random_telescope()
        update_time = datetime.datetime(2013, 10, 5, 0, 0, 0)

        update(cursor, camera, telescope,
                update_time=lambda: update_time)

        assert self.camera_telescope_history_contents() == (
                (camera, telescope, update_time, None),
                )

    def test_second_update_is_correct(self, cursor):
        camera = self.random_camera()
        telescope = self.random_telescope()
        update_time_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        update_time_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)

        update(cursor, camera, telescope,
                update_time=lambda: update_time_1)
        update(cursor, camera, telescope,
                update_time=lambda: update_time_2)

        results = self.camera_telescope_history_contents(cursor=cursor)
        assert results == (
                (camera, telescope, update_time_1, update_time_2),
                (camera, telescope, update_time_2, None),
                )

    def test_different_telescopes(self, cursor):
        camera = self.random_camera()
        telescope_1 = self.random_telescope()
        telescope_2 = telescope_1

        while telescope_2 == telescope_1:
            telescope_2 = self.random_telescope()

        assert telescope_1 != telescope_2

        update_time_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        update_time_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)

        update(cursor, camera, telescope_1,
                update_time=lambda: update_time_1)
        update(cursor, camera, telescope_2,
                update_time=lambda: update_time_2)

        results = self.camera_telescope_history_contents(cursor=cursor)

        assert results == (
                (camera, telescope_1, update_time_1, None),
                (camera, telescope_2, update_time_2, None),
                )

    def test_inserting_bad_camera_check_in_interface(self, cursor):
        bad_camera_id = 10101
        assert bad_camera_id not in self.camera_names
        with pytest.raises(NGTSDatabaseIntegrityError):
            update(cursor, bad_camera_id, self.random_telescope())

    def test_database_validations(self, cursor):
        '''
        This test has to bypass the interface, and checks the triggers from the database
        validations
        '''
        start_date = datetime.datetime.now()
        bad_id = 10101
        assert bad_id not in self.telescope_names and bad_id not in self.camera_names

        for (camera_id, telescope_id) in zip(
                [bad_id, self.random_telescope()],
                [self.random_camera(), bad_id]):

            with pytest.raises(MySQLdb.IntegrityError) as err:
                cursor.execute('''insert into camera_telescope_history
                (camera_id, telescope_id, start_date)
                values (%s, %s, %s)''',
                (camera_id, telescope_id, start_date))

            assert 'foreign key' in str(err)
