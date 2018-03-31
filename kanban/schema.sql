create table if not exists users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);

create table if not exists tasks (
  id integer primary key autoincrement,
  task text not null,
  username text not null,
  state text, 
  foreign key username references users(username)
  );
