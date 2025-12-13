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

CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE meeting_class (
    id INTEGER PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings,
    title TEXT,
    value TEXT
);
