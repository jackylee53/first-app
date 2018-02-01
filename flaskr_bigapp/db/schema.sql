drop table if exists playbooks_record;
create table playbooks_record (
  id integer PRIMARY KEY AUTOINCREMENT ,
  playbooks string not NULL ,
  ssh_user string not NULL ,
  project_name string not NULL ,
  extra_vars string not NULL ,
  forks string not NULL ,
  tags string not NULL
) ;