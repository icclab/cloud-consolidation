drop table if exists actions;
create table actions (
 id integer primary key autoincrement,
 consolidation_id integer,
 vm_id text,
 src_host text,
 dst_host text,
 phase text
);

drop table if exists consolidations;
create table consolidations (
  id integer primary key autoincrement,
  timestamp integer,
  username text,
  url text,
  tenant_name text
);

drop table if exists hypervisors;
create table hypervisors (
  id integer primary key autoincrement,
  hypervisor_id text,
  consolidation_id integer,
  consolidation_ts integer,
  cpu integer,
  cpu_util real,
  capacity real,
  memory_used int,
  memory_capacity int,
  power_consumption real,
  consumption_idle,
  consumption_max,
  phase text,
  ip text,
  no_vms integer
);
