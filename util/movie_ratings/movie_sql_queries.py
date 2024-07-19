# Movies Table
CREATE_movies_TABLE = """
    CREATE TABLE IF NOT EXISTS movies(
        movie_id INT PRIMARY KEY,
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
        last_name VARCHAR(256)
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

# Number of reports per user
COUNT_REVIEWS_PER_USER = """
    SELECT U.user_id, U.first_name, U.last_name, COUNT(R.movie_id) AS num_reviews
    FROM users AS U
    LEFT JOIN movieratings AS R
    ON U.user_id = R.user_id
    GROUP BY U.user_id, U.first_name, U.last_name;
"""

# 5 movies with the highest reviews - break ties alphabetically
MOST_REVIEWS_MOVIES = """
    SELECT M.movie_id, M.title, COUNT(R.user_id) AS num_reviews
    FROM movies AS M
    LEFT JOIN movieratings AS R
    ON M.movie_id = R.movie_id
    GROUP BY M.movie_id, M.title
    ORDER BY num_reviews DESC, M.title ASC
    LIMIT 10
"""
