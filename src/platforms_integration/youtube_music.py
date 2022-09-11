from ytmusicapi import YTMusic

youtube_url_format = "https://music.youtube.com/watch?v={}"

def get_artist_songs(youtube_music_client, artist_name: str, n_songs: int) -> list[dict]:
    songs = youtube_music_client.search(query=artist_name, filter="songs")
    # NOTE: it appears like "limit" parameter in the API call "search" doesn't work (at least without the authentification)
    songs = songs[:n_songs]
    return songs

def get_artist_title_song(youtube_music_client, artist_name, song_name) -> dict:
    search_requst = artist_name + " - " + song_name
    songs = youtube_music_client.search(query=search_requst, filter="songs")
    if len(songs) > 0:
        return songs[0]
    return None

def get_song_url(song: dict):
    return youtube_url_format.format(song['videoId'])

def get_songs_titles_urls(songs: list[dict]) -> list[str]:
    titles = []
    urls = []
    for song in songs:
        titles.append(song['title'])
        urls.append(youtube_url_format.format(song['videoId']))
    return titles, urls