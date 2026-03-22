select * from reviews limit 10;
select * from review_history limit 10;
select * from places;
select * from place_aliases;
select * from schema_version;
select * from sync_checkpoints; 
select * from sqlite_sequence;
select * from scrape_sessions;

CREATE TABLE name_place(name,URL)