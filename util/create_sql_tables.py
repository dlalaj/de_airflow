# Movies Table
# +---------------+---------+
# | Column Name   | Type    |
# +---------------+---------+
# | movie_id      | int     |
# | title         | varchar |
# | released_at    | date    |
# +---------------+---------+
# movie_id is the primary key

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
# +---------------+---------+
# | Column Name   | Type    |
# +---------------+---------+
# | user_id       | int     |
# | name          | varchar |
# +---------------+---------+
# user_id is the primary key (column with unique values) for this table.

CREATE_users_TABLE = """
    CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY,
        first_name VARCHAR(256),
        last_name VARCHAR(256),
        review_date DATE
    )
"""

# MovieRating
# +---------------+---------+
# | Column Name   | Type    |
# +---------------+---------+
# | movie_id      | int     |
# | user_id       | int     |
# | rating        | int     |
# | created_at    | date    |
# +---------------+---------+
# (movie_id, user_id) is the primary key (column with unique values) for this table.
# movied_id is a foreign key to movies table
# user_id is a foreign key to users table

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
