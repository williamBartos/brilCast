drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    'temp' text not null,
	'inTemp' text not null,
	'inHum' text not null,
	'time' text not null
   );