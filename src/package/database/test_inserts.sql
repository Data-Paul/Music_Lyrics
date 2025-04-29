-- Insert test artist
INSERT INTO Artist (artist_name, artist_url, additional_info)
VALUES ('Test Artist', 'https://example.com/artist', '{"formed": "2020", "country": "US"}'::jsonb)
RETURNING artist_id;

-- Insert test genres
INSERT INTO Genre (genre_name)
VALUES ('Rock'), ('Pop'), ('Electronic')
RETURNING genre_id;

-- Insert test song (using the artist_id from above)
INSERT INTO Song (artist_id, song_name, song_url, additional_info)
VALUES (1, 'Test Song', 'https://example.com/song', '{"duration": "3:45", "release_date": "2024-01-01"}'::jsonb)
RETURNING song_id;

-- Insert test lyrics
INSERT INTO Lyrics (song_id, lyrics_text)
VALUES (1, 'This is a test song lyric line 1
This is a test song lyric line 2
This is a test song lyric line 3');

-- Link song to genres
INSERT INTO SongGenre (song_id, genre_id)
VALUES (1, 1), (1, 2);  -- Linking to Rock and Pop genres

-- Verify the inserts
SELECT 
    a.artist_name,
    s.song_name,
    string_agg(g.genre_name, ', ') as genres,
    l.lyrics_text
FROM Artist a
JOIN Song s ON a.artist_id = s.artist_id
JOIN Lyrics l ON s.song_id = l.song_id
LEFT JOIN SongGenre sg ON s.song_id = sg.song_id
LEFT JOIN Genre g ON sg.genre_id = g.genre_id
GROUP BY a.artist_name, s.song_name, l.lyrics_text; 