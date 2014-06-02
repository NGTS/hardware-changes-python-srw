import datetime

class NGTSError(RuntimeError): pass
class NGTSDatabaseIntegrityError(NGTSError): pass

class UpdateHardware(object):
    def __init__(self, cursor):
        self.cursor = cursor

    def get_id(self, table_name, name_value):
        '''
        Retrieve the id of the piece of hardware given in `table_name`
        with the "name" attribute of the object is given in `name_value`.
        '''
        name_name = '{0}_name'.format(table_name)
        self.cursor.execute('''select id from {table_name}
                where {name_name} = %s limit 1'''.format(
            table_name=table_name, name_name=name_name), (name_value, ))
        query_results = self.cursor.fetchone()
        if query_results:
            return query_results[0]
        else:
            raise NGTSDatabaseIntegrityError(
                    "Invalid camera {0} supplied".format(name_value)
                    )

    def update(self, camera_name, telescope_name,
            update_time=datetime.datetime.now):
        '''
        Move the camera known as `camera_name` to the telescope known as
        `telescope_name`.

        The update time defaults to now, but can be specified e.g.

        update_time = lambda: datetime.datetime(2020, 10, 2, 15, 13, 2)
        '''
        camera_id = self.get_id('camera', camera_name)
        telescope_id = self.get_id('telescope', telescope_name)

        self.update_history_table(camera_id, telescope_id, update_time)
        self.update_current_table(camera_id, telescope_id, update_time)

    def update_history_table(self, camera_id, telescope_id, update_time):
        self.cursor.execute('''update camera_telescope_history
        set end_date = %s
        where camera_id = %s
        and telescope_id = %s
        and end_date is null''', (update_time(), camera_id, telescope_id))

        self.cursor.execute('''insert into camera_telescope_history
        (camera_id, telescope_id, start_date)
        values (%s, %s, %s)''', (camera_id, telescope_id, update_time()))

    def update_current_table(self, camera_id, telescope_id, update_time):
        self.cursor.execute('''insert into camera_telescope
        (camera_id, telescope_id, start_date)
        values (%s, %s, %s)
        on duplicate key update
        telescope_id=%s,
        start_date=%s''',
        (camera_id, telescope_id, update_time(),
            telescope_id, update_time()))
