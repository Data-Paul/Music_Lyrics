-- Create the Artist table
CREATE TABLE Artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name TEXT NOT NULL,
    artist_url TEXT,
    additional_info JSONB
);

-- Create the Genre table
CREATE TABLE Genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name TEXT NOT NULL UNIQUE
);

-- Create the Song table
CREATE TABLE Song (
    song_id SERIAL PRIMARY KEY,
    artist_id INTEGER NOT NULL,
    song_name TEXT NOT NULL,
    song_url TEXT,
    additional_info JSONB,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id) ON DELETE CASCADE
);

-- Create the Lyrics table
CREATE TABLE Lyrics (
    lyrics_id SERIAL PRIMARY KEY,
    song_id INTEGER NOT NULL,
    lyrics_text TEXT NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES Song(song_id) ON DELETE CASCADE
);

-- Create the SongGenre junction table for many-to-many relationship
CREATE TABLE SongGenre (
    song_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (song_id, genre_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_artist_name ON Artist(artist_name);
CREATE INDEX idx_song_name ON Song(song_name);
CREATE INDEX idx_genre_name ON Genre(genre_name);
CREATE INDEX idx_lyrics_song_id ON Lyrics(song_id);
CREATE INDEX idx_songgenre_song_id ON SongGenre(song_id);
CREATE INDEX idx_songgenre_genre_id ON SongGenre(genre_id); 