-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



create TABLE player(id serial primary key,
                    name text);

create table match(id serial,winner integer references player(id),
        looser integer references player(id)) ;

create table matchRecord(id integer references player,totalMatch integer,
                        win integer);
