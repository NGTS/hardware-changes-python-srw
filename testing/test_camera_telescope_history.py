import datetime
import pytest
import MySQLdb

from test_helper import DatabaseTester
from hardware_changes.datastore import UpdateHardware, NGTSDatabaseIntegrityError

class TestCameraTelescopeHistory(DatabaseTester):
    def test_update_succeeds(self, cursor):
        camera = self.random_camera()
        telescope = self.random_telescope()
        update_time = datetime.datetime(2013, 10, 5, 0, 0, 0)

        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: update_time)

        assert self.camera_telescope_history_contents(cursor) == (
                (camera, telescope, update_time, None),
                )

    def test_second_update_is_correct(self, cursor):
        camera = self.random_camera()
        telescope = self.random_telescope()
        update_time_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        update_time_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)

        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: update_time_1)
        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: update_time_2)

        results = self.camera_telescope_history_contents(cursor)
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

        UpdateHardware(cursor).update(camera, telescope_1,
                update_time=lambda: update_time_1)
        UpdateHardware(cursor).update(camera, telescope_2,
                update_time=lambda: update_time_2)

        results = self.camera_telescope_history_contents(cursor)

        assert results == (
                (camera, telescope_1, update_time_1, None),
                (camera, telescope_2, update_time_2, None),
                )

    def test_inserting_bad_camera_check_in_interface(self, cursor):
        bad_camera_id = 10101
        assert bad_camera_id not in self.camera_names
        with pytest.raises(NGTSDatabaseIntegrityError):
            UpdateHardware(cursor).update(bad_camera_id, self.random_telescope())

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
