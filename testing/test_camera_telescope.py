import datetime
import pytest

from test_helper import DatabaseTester
from hardware_changes.datastore import (UpdateHardware,
        NGTSDatabaseIntegrityError)

class TestCameraTelescope(DatabaseTester):
    def test_with_one_update(self, cursor):
        start_date = datetime.datetime(2013, 10, 5, 0, 0, 0)
        camera = self.random_camera()
        telescope = self.random_telescope()

        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: start_date)

        cursor.execute('''select camera_name, telescope_name, start_date
        from camera_telescope
        join camera on camera.id = camera_telescope.camera_id
        join telescope on telescope.id = camera_telescope.telescope_id
        order by start_date asc''')

        assert cursor.fetchall() == (
                (camera, telescope, start_date),
                )

    def test_with_two_updates(self, cursor):
        start_date_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        start_date_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)
        camera = self.random_camera()
        telescope = self.random_telescope()

        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: start_date_1)
        UpdateHardware(cursor).update(camera, telescope,
                update_time=lambda: start_date_2)

        cursor.execute('''select camera_name, telescope_name, start_date
        from camera_telescope
        join camera on camera.id = camera_telescope.camera_id
        join telescope on telescope.id = camera_telescope.telescope_id
        order by start_date asc''')

        assert cursor.fetchall() == (
                (camera, telescope, start_date_2),
                )

    def test_two_updates_with_different_telescopes(self, cursor):
        start_date_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        start_date_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)
        camera = self.random_camera()
        telescope_1 = self.random_telescope()
        telescope_2 = (telescope_1 + 1) % len(self.telescope_names)

        UpdateHardware(cursor).update(camera, telescope_1,
                update_time=lambda: start_date_1)
        UpdateHardware(cursor).update(camera, telescope_2,
                update_time=lambda: start_date_2)

        cursor.execute('''select camera_name, telescope_name, start_date
        from camera_telescope
        join camera on camera.id = camera_telescope.camera_id
        join telescope on telescope.id = camera_telescope.telescope_id
        order by start_date asc''')

        assert cursor.fetchall() == (
                (camera, telescope_2, start_date_2),
                )

    def test_multiple_cameras(self, cursor):
        start_date_1 = datetime.datetime(2013, 10, 5, 0, 0, 0)
        start_date_2 = datetime.datetime(2013, 10, 6, 0, 0, 0)
        camera_1 = min(self.camera_names)
        camera_2 = max(self.camera_names)
        telescope_1 = min(self.telescope_names)
        telescope_2 = max(self.telescope_names)

        UpdateHardware(cursor).update(camera_1, telescope_1,
                update_time=lambda: start_date_1)
        UpdateHardware(cursor).update(camera_2, telescope_2,
                update_time=lambda: start_date_2)

        cursor.execute('''select camera_name, telescope_name, start_date
        from camera_telescope
        join camera on camera.id = camera_telescope.camera_id
        join telescope on telescope.id = camera_telescope.telescope_id
        order by start_date asc''')

        assert cursor.fetchall() == (
                (camera_1, telescope_1, start_date_1),
                (camera_2, telescope_2, start_date_2),
                )

