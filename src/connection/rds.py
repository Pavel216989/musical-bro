import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from config import RDS_ENDPOINT, RDS_USERNAME, RDS_PASSWORD, RDS_PORT, RDS_DB_NAME

sql_alchemy_db_url = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_ENDPOINT}/{RDS_DB_NAME}"


def create_connection():
    return psycopg2.connect(
        database=RDS_DB_NAME,
        user=RDS_USERNAME,
        password=RDS_PASSWORD,
        host=RDS_ENDPOINT,
        port=RDS_PORT
    )

def create_db_engine():
    engine = create_engine(sql_alchemy_db_url)
    return engine

def read_songs(genre: str = None, mood: str = None, shown_songs: dict = []):
    if genre == "skip genre":
        genre = None
    if mood == "skip mood":
        mood = None
    if genre is None and mood is None:
        # None of genre/mood selected
        query = "select * from public.songs"
    elif genre is not None:
        if mood is None:
            # Only genre selected
            query = f"select * from public.songs where '{genre}' = ANY(genre)"
        else:
            # Both genre and mood selected
            query = f"select * from public.songs where '{genre}' = ANY(genre) and '{mood}' = ANY(mood)"
    else:
        # Only mood selected
        query = f"select * from public.songs where '{mood}' = ANY(mood)"
    engine = create_db_engine()
    result_df = pd.read_sql_query(query, con=engine)
    result = result_df.to_dict('records')
    result = [{k: v for k, v in song.items() if v is not None} for song in result]
    result = [song for song in result if song['title'] not in shown_songs.get(song['artist'], [])]
    return result