import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("apis.env")

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URL = "http://localhost:8080"
USER_AGENT=os.getenv("USER_AGENT")
REFRESH_TOKEN=os.getenv("REFRESH_TOKEN")


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    refresh_token=REFRESH_TOKEN,
    user_agent=USER_AGENT
)

def submission_to_df(submission, listing_tpe):
    return {
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "num_comments": submission.num_comments,
        "created_utc": submission.created_utc,
        "selftext": submission.selftext,
        "listing_type": listing_tpe
    }

subreddit_name = input("Enter the subreddit name: ")

df_hot = pd.DataFrame([submission_to_df(submission, "hot") for submission in reddit.subreddit(subreddit_name).hot(limit=10)])
df_new = pd.DataFrame([submission_to_df(submission, "new") for submission in reddit.subreddit(subreddit_name).new(limit=10)])
df_top = pd.DataFrame([submission_to_df(submission, "top") for submission in reddit.subreddit(subreddit_name).top(limit=10)])
df_rising = pd.DataFrame([submission_to_df(submission, "rising") for submission in reddit.subreddit(subreddit_name).rising(limit=10)])
df_controversial = pd.DataFrame([submission_to_df(submission, "controversial") for submission in reddit.subreddit(subreddit_name).controversial(limit=10)])

df = pd.concat([df_hot, df_new, df_top, df_rising, df_controversial])

