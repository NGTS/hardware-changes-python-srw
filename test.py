import MySQLdb
import datetime
import random
import time
import os

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

def get_id(cursor, table_name, name_value):
    '''
    Retrieve the id of the piece of hardware given in `table_name` with the "name"
    attribute of the object is given in `name_value`.
    '''
    name_name = '{}_name'.format(table_name)
    cursor.execute('''select id from {table_name} where {name_name} = %s limit 1'''.format(
        table_name=table_name, name_name=name_name), (name_value, ))
    return cursor.fetchone()[0]

def update(cursor, camera_name, telescope_name, update_time=datetime.datetime.now,
        interrupt=False):
    '''
    Move the camera known as `camera_name` to the telescope known as `telescope_name`.

    The update time defaults to now, but can be specified e.g.

    update_time = lambda: datetime.datetime(2020, 10, 2, 15, 13, 2)
    '''
    with connection as cursor:
        camera_id = get_id(cursor, 'camera', camera_name)
        telescope_id = get_id(cursor, 'telescope', telescope_name)

        cursor.execute('''update camera_telescope_history set end_date = %s
        where camera_id = %s
        and telescope_id = %s
        and end_date is null''', (update_time(), camera_id, telescope_id))

        if interrupt:
            raise RuntimeError("INTERRUPT")

        cursor.execute('''insert into camera_telescope_history (camera_id, telescope_id, start_date)
        values (%s, %s, %s)''', (camera_id, telescope_id, update_time()))

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

def main():
    clean_database()

    # Insert all of the cameras
    with connection as cursor:
        cursor.executemany('''insert into camera (camera_name) values (%s)''',
                [(c, ) for c in camera_names])
        cursor.executemany('''insert into telescope (telescope_name) values (%s)''',
                [(t, ) for t in telescope_names])

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


if __name__ == '__main__':
    main()
