import praw
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent")
)

# Use this template to test if the api is running
'''subreddit = reddit.subreddit("python")

for post in subreddit.hot(limit=10):
    print(post.title)'''