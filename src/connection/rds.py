import psycopg2
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

def read_songs(genre: str = None, mood: str = None):
    if genre is None and mood is None:
        # None of genre/mood selected
        query = "select * from public.songs"
    elif genre is not None:
        if mood is None:
            # Only genre selected
            query = f"select * from public.songs where '{genre}' = ANY(genre)"
        else:
            # Both genre and mood selected
            query = f"select * from public.songs where {genre}' = ANY(genre) and '{mood}' = ANY(mood)"
    else:
        # Only mood selected
        query = f"select * from public.songs where '{mood}' = ANY(mood)"
    
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
    return result