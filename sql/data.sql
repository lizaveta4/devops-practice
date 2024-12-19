CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
    content TEXT NOT NULL, -- Content of the note
    date DATE NOT NULL     -- Date associated with the note
);