CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    topic TEXT,
    description TEXT,
    date DATE,
    start_time TIME,
    end_time TIME,
    user_id INTEGER REFERENCES users
);
