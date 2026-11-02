from connection import *

async def create_user(username, full_name, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        INSERT INTO users(username, full_name, tg_id) VALUES 
        ($1, $2, $3) 

        """, username, full_name, int(tg_id))
        return True
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} create_user")
        return False
    finally:
        await conn.close()


async def profile(tg_id):

    try:
        conn = await connection_db()
        user =  await conn.fetchrow("""
        
        SELECT * FROM users 
        WHERE tg_id=$1 

        """, int(tg_id))

        return user
    
    except Exception as error:
        print(f"{type(error).__name__}: {error} profile")
        return False
    finally:
        await conn.close()


async def show_stats(tg_id):

    try:
        conn = await connection_db()
        stats = await conn.fetchrow("""
        select count(*) as count from favourites
        where tg_id = $1
""", int(tg_id))

        return stats

    except Exception as error:
        print(f"{type(error)}: {error} sss.py")     
        return False
    finally:
        await conn.close()   



async def show_favourites(tg_id):
    try:
        conn = await connection_db()
        movies = await conn.fetch("""
        select movies.title, movies.release_year as year, favourites.added_at as added from favourites
        join movies on favourites.movie_id = movies.id
        where favourites.user_id = $1
""", int(tg_id))

        return movies
    except Exception as error:
        print(f"{type(error)}: {error} ssf.py")     
        return False
    finally:
        await conn.close()   



async def one_movie(m_id):
    try:
        conn = await connection_db()
        movie = await conn.fetchrow("""
        select movies.*, users.full_name,
        (select count(*) from favourites where favourites.movie_id = movies.id) as fav_count from movies
        left join users on users.tg_id = movies.owner_id
        where movies.id = $1
""", int(m_id))

        return movie
    
    except Exception as error:
        print(f"{type(error)}: {error} sm.py")     
        return False
    finally:
        await conn.close()   



async def all_movies():
    try:
        conn = await connection_db()
        movie = await conn.fetch("""
        select movies.*, users.full_name from movies
        join users on users.tg_id = movies.owner_id
""")

        return movie
    except Exception as error:
        print(f"{type(error)}: {error} sms.py")     
        return False
    finally:
        await conn.close()   



async def add_new_movie_service(owner_id , name , genre, year, photo_id, caption=None):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into movies(owner_id, title, genre, release_year, poster_file_id, caption) values
            ($1, $2, $3, $4, $5, $6)
""", int(owner_id), name, genre, int(year), photo_id, caption)

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sanm.py")   
        return False  
    finally:
        await conn.close()   




async def to_favourites(movie_id, user_id):
    try:
        conn = await connection_db()
        await conn.execute("""  
        insert into favourites(movie_id, user_id) values
            ($1, $2)

""", int(movie_id), int(user_id))

        return True
    except Exception as error:
        print(f"{type(error)}: {error} stf.py") 
        return False    
    finally:
        await conn.close()   



async def check_favourites(movie_id, user_id):
    try:
        conn = await connection_db()
        movie = await conn.fetchrow("""  
        select movie_id from favourites 
        where movie_id = $1
        and user_id = $2

""", int(movie_id), int(user_id))
        
        return movie
    except Exception as error:
        print(f"{type(error)}: {error} stf.py") 
        return False    
    finally:
        await conn.close()   


async def get_favourites_count(tg_id):
    try:
        conn = await connection_db()
        count = await conn.fetchrow("""
        select count(*) as count from favourites 
        where user_id = $1
""",int(tg_id) )

        return count
    except Exception as error:
        print(f"{type(error)}: {error} sgfc.py")     
        return False
    finally:
        await conn.close()   



async def get_favourite_movies(tg_id):
    try:
        conn = await connection_db()
        movies = await conn.fetch("""
        
    select favourites.*, movies.title, movies.genre, movies.release_year, movies.caption, users.full_name, movies.poster_file_id,
    (select count(*) from favourites f where f.movie_id = movies.id) as fav_count
    from favourites
    join movies on movies.id = favourites.movie_id
    left join users on users.tg_id = movies.owner_id
    where user_id = $1
""", int(tg_id))

        return movies
    except Exception as error:
        print(f"{type(error)}: {error} sgfm.py")    
        return False 
    finally:
        await conn.close()   





async def delete_from_favourites(m_id, tg_id):

    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        delete from favourites
        where movie_id = $1 and user_id = $2
        returning id
""", int(m_id), int(tg_id))

        if not result:
            return False

        return True

    except Exception as error:
        print(f"{type(error)}: {error} sdf.py")  
        return False   
    finally:
        await conn.close()   



async def random_movie():
    try:
        conn = await connection_db()
        movie = await conn.fetchrow("""

            select movies.*, 
            (select count(*) from favourites where favourites.movie_id = movies.id) as fav_count,
            users.full_name FROM movies
            join users on users.tg_id = movies.owner_id
            ORDER BY RANDOM()
            LIMIT 1
        """)
        return movie
    except Exception as error:
        print(f"{type(error)}: {error} rm.py")    
        return False 
    finally:
        await conn.close()   





async def get_all_genres():
    try:
        conn = await connection_db()
        genres = await conn.fetch("""

        select genre, count(*) as count from movies
        where genre is not null
        group by genre
        order by genre
""")

        return genres
    
    except Exception as error:
        print(f"{type(error)}: {error} sgag.py")
        return False
    finally:
        await conn.close()



async def get_movies_by_genre(genre):

    try:
        conn = await connection_db()
        movies = await conn.fetch("""
        select movies.*, users.full_name from movies
        left join users on users.tg_id = movies.owner_id
        where movies.genre = $1
        order by movies.created_at desc
""", genre)

        return movies
    
    except Exception as error:
        print(f"{type(error)}: {error} sgmbg.py")
        return False
    finally:
        await conn.close()