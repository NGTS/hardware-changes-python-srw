import datetime

class DatabaseIntegrityError(RuntimeError):
    pass

def get_id(cursor, table_name, name_value):
    '''
    Retrieve the id of the piece of hardware given in `table_name` with the "name"
    attribute of the object is given in `name_value`.
    '''
    name_name = '{}_name'.format(table_name)
    cursor.execute('''select id from {table_name} where {name_name} = %s limit 1'''.format(
        table_name=table_name, name_name=name_name), (name_value, ))
    query_results = cursor.fetchone()
    if query_results:
        return query_results[0]
    else:
        raise DatabaseIntegrityError("Invalid camera {} supplied".format(name_value))

def update(cursor, camera_name, telescope_name, update_time=datetime.datetime.now):
    '''
    Move the camera known as `camera_name` to the telescope known as `telescope_name`.

    The update time defaults to now, but can be specified e.g.

    update_time = lambda: datetime.datetime(2020, 10, 2, 15, 13, 2)
    '''
    camera_id = get_id(cursor, 'camera', camera_name)
    telescope_id = get_id(cursor, 'telescope', telescope_name)

    cursor.execute('''update camera_telescope_history set end_date = %s
    where camera_id = %s
    and telescope_id = %s
    and end_date is null''', (update_time(), camera_id, telescope_id))

    cursor.execute('''insert into camera_telescope_history (camera_id, telescope_id, start_date)
    values (%s, %s, %s)''', (camera_id, telescope_id, update_time()))

