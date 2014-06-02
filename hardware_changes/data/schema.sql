drop database if exists ngts_hwlog;
create database ngts_hwlog;

use ngts_hwlog;

drop table if exists camera;
create table camera (
    id integer primary key auto_increment,
    camera_name integer not null,
    unique index unique_camera_name (camera_name)
);

drop table if exists telescope;
create table telescope (
    id integer primary key auto_increment,
    telescope_name integer not null,
    unique index unique_telescope_name (telescope_name)
);

drop table if exists mount;
create table mount (
    id integer primary key auto_increment,
    mount_name integer not null,
    unique index unique_mount_name (mount_name)
);

drop table if exists focuser;
create table focuser (
    id integer primary key auto_increment,
    focuser_name integer not null,
    unique index unique_focuser_name (focuser_name)
);

drop table if exists camera_telescope_history;
create table camera_telescope_history (
    id integer primary key auto_increment,
    camera_id integer not null,
    telescope_id integer not null,
    start_date datetime not null,
    end_date datetime,
    foreign key (camera_id)
    references camera(id)
    on delete cascade,
    foreign key (telescope_id)
    references telescope(id)
    on delete cascade
);

drop table if exists camera_mount_history;
create table camera_mount_history (
    id integer primary key auto_increment,
    camera_id integer not null,
    mount_id integer not null,
    start_date datetime not null,
    end_date datetime,
    foreign key (camera_id)
    references camera(id),
    foreign key (mount_id)
    references mount(id)
);


drop table if exists camera_focuser_history;
create table camera_focuser_history (
    id integer primary key auto_increment,
    camera_id integer not null,
    focuser_id integer not null,
    start_date datetime not null,
    end_date datetime,
    foreign key (camera_id)
    references camera(id),
    foreign key (focuser_id)
    references focuser(id)
);

-- Simple tables holding the most up to date state
drop table if exists camera_telescope;
create table camera_telescope (
    id integer primary key auto_increment,
    camera_id integer not null,
    telescope_id integer not null,
    start_date datetime not null,
    foreign key (camera_id)
    references camera(id),
    foreign key (telescope_id)
    references telescope(id),
    unique index unique_camera_id (camera_id)
);
