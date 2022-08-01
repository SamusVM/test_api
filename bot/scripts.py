import sqlite3
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from faker import Faker
from dateutil import parser

import config

number_of_users = config.NUMBER_OF_USERS
max_posts_per_user = config.MAX_POSTS_PER_USER
max_likes_per_user = config.MAX_LIKES_PER_USER
date_from = config.DATE_FROM
date_to = config.DATE_TO


class SQLite():
    def __init__(self, file=config.DB_FILE):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def make_password(password, salt):
    hasher = PBKDF2PasswordHasher()
    return hasher.encode(password, salt)


if __name__ == "__main__":
    with SQLite() as cur:
        fake = Faker()
        users_id = []
        posts_id = []
        users = (
            (
                fake.user_name(),
                fake.email(),
                make_password(fake.password(), fake.slug()),
                0, 0, 0, 'current_timestamp', 'current_timestamp'
            )
            for i in range(number_of_users))

        for user in users:
            cur.execute(
                '''
                INSERT OR IGNORE INTO my_auth_user
                (username, email, password,  is_superuser,  is_active, is_staff, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)            
                ''',
                user)
            user_id = cur.lastrowid
            users_id.append(user_id)
            posts = (
                (
                    fake.text(fake.random_int(100, 1000)),
                    user_id,
                )
                for i in range(fake.random_int(0, max_posts_per_user))
            )

            for post in posts:
                cur.execute(
                    '''
                    INSERT OR IGNORE INTO my_api_post
                    ("text", created_by_id)
                    VALUES (?, ?)            
                    ''',
                    post)
                posts_id.append(cur.lastrowid)

        for user_id in users_id:
            likes = [
                (
                    user_id,
                    fake.random_element(posts_id),
                    fake.date_time_between(parser.parse(date_from), parser.parse(date_to))
                )
                for i in range(fake.random_int(0, max_likes_per_user))
            ]
            for like in likes:
                cur.executemany(
                    '''
                    INSERT OR IGNORE INTO my_api_like
                    (created_by_id, post_id, created_at)
                    VALUES (?, ?, ?)            
                    ''',
                    likes)

