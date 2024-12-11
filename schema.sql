CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    language TEXT
);
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    exercise TEXT,
    DEADLINE DATE,
    language_id INTEGER REFERENCES languages,
    user_id INTEGER REFERENCES users
);
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES users,
    answer TEXT
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    exercise_id INTEGER REFERENCES exercises,
    answer_id INTEGER REFERENCES answers,
    user_id INTEGER REFERENCES users
);
