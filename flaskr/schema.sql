drop table if exists entries;
create table entries (
  id integer PRIMARY KEY AUTOINCREMENT ,
  title string not NULL ,
  text string not NULL
) ;
drop table if exists logins;
drop table if EXISTS users;
create table users (
  id integer PRIMARY KEY AUTOINCREMENT ,
  user string not NULL ,
  password string not NULL
) ;