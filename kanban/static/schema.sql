create table if not exists users (
    username text not null,
    password text not null
);

create table if not exists tasks (
  id integer primary key autoincrement,
  title text not null,
  state text, 
  date_added date, 
  date_started date,
  date_completed date
  );
