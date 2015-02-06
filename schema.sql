drop table if exists urls;
create table urls (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL
);
