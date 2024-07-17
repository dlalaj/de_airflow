# Movies Table
CREATE_movies_TABLE = """
    CREATE TABLE IF NOT EXISTS movies(
        movie_id iNT PRIMARY KEY,
        title VARCHAR(256),
        domestic_sales INT,
        international_sales INT,
        released_at DATE
    )
"""

# Users Table
CREATE_users_TABLE = """
    CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY,
        first_name VARCHAR(256),
        last_name VARCHAR(256),
        review_date DATE
    )
"""

# MovieRating
CREATE_ratings_TABLE = """
    CREATE TABLE IF NOT EXISTS movieratings(
        movie_id INT,
        user_id INT,
        rating INT,
        created_at DATE,
        PRIMARY KEY (movie_id, user_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
"""
