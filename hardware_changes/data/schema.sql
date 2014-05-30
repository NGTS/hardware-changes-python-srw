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

-- Create views
create view camera_telescope 
(id, camera_id, telescope_id, start_date)
as select id, camera_id, telescope_id, start_date
from camera_telescope_history
where end_date is null;

create view camera_mount 
(id, camera_id, mount_id, start_date)
as select id, camera_id, mount_id, start_date
from camera_mount_history
where end_date is null;

create view camera_focuser 
(id, camera_id, focuser_id, start_date)
as select id, camera_id, focuser_id, start_date
from camera_focuser_history
where end_date is null;

-- Create validations
delimiter $$
create trigger ensure_valid_camera_telescope_id
    before insert on camera_telescope_history for each row
    begin
        if new.camera_id not in (select distinct id from camera) or
            new.telescope_id not in (select distinct id from telescope)
        then
            signal sqlstate '45000' set message_text = 'Invalid camera id or telescope id given';
        end if;
    end;
$$

create trigger ensure_valid_camera_mount_id
    before insert on camera_mount_history for each row
    begin
        if new.camera_id not in (select distinct id from camera) or
            new.mount_id not in (select distinct id from mount)
        then
            signal sqlstate '45000' set message_text = 'Invalid camera id or mount id given';
        end if;
    end;
$$

create trigger ensure_valid_camera_focuser_id
    before insert on camera_focuser_history for each row
    begin
        if new.camera_id not in (select distinct id from camera) or
            new.focuser_id not in (select distinct id from focuser)
        then
            signal sqlstate '45000' set message_text = 'Invalid camera id or focuser id given';
        end if;
    end;
$$
delimiter ;
