
import praw
import sqlite3

import config
import database

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('thanosdidnothingwrong')

conn = sqlite3.connect("thanos.db")

def find_users():
    print("Starting searching...")
    counter = 0
    sub = 0
    for submission in subreddit.top('all', limit=10000):
        sub += 1
        print("{} --> Starting new submission {}".format(sub, submission.id))
        submission.comments.replace_more(limit=1000)
        for comment in submission.comments:
            counter += 1
            print("{}. Doing {}".format(counter, comment.id))
            author = comment.author
            if (not database.is_logged(conn, author)):
                database.add_user(conn, author, comment.id)
                print("Added {}".format(author))


database.init_database(conn)
find_users()
conn.close()
