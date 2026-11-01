import asyncpg
from dotenv import load_dotenv
import os


load_dotenv()

p_db = os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="salim",
        database="movies_db",
        password= p_db
        )
        return conn
    except Exception as error:
        print(f"{type(error)}: {error} conn.py")




async def create_tables():
    try:
        conn = await connection_db()
        await conn.execute("""

        create table if not exists users(
            id serial primary key,
            tg_id bigint unique,
            username varchar(200),
            full_name varchar(200),
            is_active bool default true
        );

        create table if not exists movies(
            id serial primary key,
            owner_id bigint references users(tg_id),
            title varchar(200) not null, 
            genre varchar(200),
            release_year int not null,
            poster_file_id text,
            caption text,
            created_at timestamp default now(),
            is_active bool default true
        );

        create table if not exists favourites(
            id serial primary key,
            user_id bigint references users(tg_id),
            movie_id int references movies(id),
            added_at timestamp default now(),
            is_active bool default true,
            unique(user_id, movie_id)
        )
""")
        print("Tables created successfuly")

    except Exception as error:
        print(f"{type(error)}: {error} con.py")     
    finally:
        await conn.close()  