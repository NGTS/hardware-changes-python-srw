import pytest
import pymysql
import datetime
import os
import random

DB_HOST = 'sirius.astro.warwick.ac.uk'
DB_NAME = 'ngts_hwlog'
DB_USER = 'sw'

def connect_to_test_database():
    return pymysql.connect(host=DB_HOST, db=DB_NAME, user=DB_USER)

def initialise_database():
    '''
    Function to remove the database data, and build it up again from scratch.

    This is stored in the sql script `hardware_changes/data/schema.sql`
    '''
    print("Cleaning database")
    os.system("mysql -u {user} -h {host} -t < hardware_changes/data/schema.sql".format(
        user=DB_USER, host=DB_HOST))
    print("Done")

class DatabaseTester(object):
    @classmethod
    def setup_class(cls):
        cls.connection = connect_to_test_database()

        cls.camera_names = [800 + value for value in xrange(1, 14)]
        cls.telescope_names = range(1, 13)

        initialise_database()

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

    def camera_telescope_history_contents(self, cursor):
        cursor.execute('''select camera_name, telescope_name, start_date, end_date
                from camera_telescope_history
                join camera on camera.id = camera_telescope_history.camera_id
                join telescope on telescope.id = camera_telescope_history.telescope_id
                order by start_date asc''')
        return cursor.fetchall()


