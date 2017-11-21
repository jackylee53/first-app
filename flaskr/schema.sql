drop table if exists entries;
create table entries (
  id integer PRIMARY KEY AUTOINCREMENT ,
  title string not NULL ,
  text string not NULL
)