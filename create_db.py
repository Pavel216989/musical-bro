from ytmusicapi import YTMusic
import pandas as pd
from sqlalchemy.dialects import postgresql
from sqlalchemy import types
from src.platforms_integration.youtube_music import get_artist_songs, get_songs_titles_urls, get_artist_title_song, get_song_url
from src.platforms_integration.song_link import get_multiple_songlink_urls
from src.connection.rds import create_connection, create_db_engine

FIRST_COLUMNS = ["artist", "title", "genre", "mood"]

# def save_top_10_songs(ytmusic_client, artist: str):
#     ytmusic_songs = get_artist_songs(
#         youtube_music_client=ytmusic_client,
#         artist_name=artist,
#         n_songs=10
#     )
#     ytmusic_titles, ytmusic_urls = get_songs_titles_urls(ytmusic_songs)
#     songlink_urls = get_multiple_songlink_urls(urls=ytmusic_urls)
    # new_df = pd.DataFrame.from_records(songlink_urls)
    # new_df['artist'] = artist
    # new_df['title'] = ytmusic_titles
    # new_df['genre'] = [["test", "test1"] for i in range(new_df.shape[0])]
    # new_df['mood'] = [["sport", "cry"] for i in range(new_df.shape[0])]
    # new_df = _sort_dataframe_columns(new_df)
#     print('done')
    # engine = create_db_engine()
    # # connection = create_connection()
    # new_df.to_sql(
    #     name="songs",
    #     con=engine,
    #     schema="public",
    #     if_exists="append",
    #     index=False,
    #     dtype={
    #         "genre": postgresql.ARRAY(types.String),
    #         "mood": postgresql.ARRAY(types.String)
    #     }
    # )

def write_songs(ytmusic, songs: list[dict]):
    artists = []
    titles = []
    ytmusic_urls = []
    genres = []
    moods = []
    for song in songs:
        ytmusic_song = get_artist_title_song(
            youtube_music_client=ytmusic,
            artist_name=song['Artist'],
            song_name=song['Title']
            )
        if ytmusic_song is None:
            continue
        url = get_song_url(ytmusic_song)
        artists.append(song['Artist'])
        titles.append(song['Title'])
        ytmusic_urls.append(url)
        genre = song['Genre'].split(',')
        genre = [g.lower().strip() for g in genre]
        genres.append(genre)
        mood = song['Mood'].split(',')
        mood = [m.lower().strip() for m in mood]
        moods.append(mood)
    songlink_urls = get_multiple_songlink_urls(urls=ytmusic_urls)
    new_df = pd.DataFrame.from_records(songlink_urls)
    new_df['artist'] = artists
    new_df['title'] = titles
    new_df['genre'] = genres
    new_df['mood'] = moods
    new_df = _sort_dataframe_columns(new_df)
    engine = create_db_engine()
    # connection = create_connection()
    new_df.to_sql(
        name="songs",
        con=engine,
        schema="public",
        if_exists="append",
        index=False,
        dtype={
            "genre": postgresql.ARRAY(types.String),
            "mood": postgresql.ARRAY(types.String)
        }
    )

def main():
    ytmusic = YTMusic()
    df = pd.read_csv('db.csv')
    songs = df.to_dict('records')
    write_songs(ytmusic=ytmusic, songs=songs)

        
def _sort_dataframe_columns(df: pd.DataFrame):
    df = df.copy()
    columns_order = FIRST_COLUMNS
    for column_name in df.columns.values:
        if column_name not in FIRST_COLUMNS:
            columns_order.append(column_name)
    return df[columns_order]    


if __name__ == '__main__':
    main()
    