import praw
import pandas as pd
import os
from reference import reddit

def submission_to_df(submission, listing_type):
    return {
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "num_comments": submission.num_comments,
        "created_utc": submission.created_utc,
        "selftext": submission.selftext,
        "listing_type": listing_type
    }

def make_dataframe(subreddit_name):
    try:  # changed - wrap Reddit API call to catch invalid subreddits
        subreddit = reddit.subreddit(subreddit_name)
        _ = subreddit.id  # changed - this line actually triggers the API call, forces PRAW to validate the subreddit
    except Exception:  # changed - PRAW throws Redirect or NotFound for invalid subreddits
        raise ValueError(f"Subreddit r/{subreddit_name} does not exist")  # changed
    
    print("making dataframe")
    df_hot = pd.DataFrame([submission_to_df(submission, "hot") for submission in reddit.subreddit(subreddit_name).hot(limit=10)])
    df_new = pd.DataFrame([submission_to_df(submission, "new") for submission in reddit.subreddit(subreddit_name).new(limit=10)])
    df_top = pd.DataFrame([submission_to_df(submission, "top") for submission in reddit.subreddit(subreddit_name).top(limit=10)])
    df_rising = pd.DataFrame([submission_to_df(submission, "rising") for submission in reddit.subreddit(subreddit_name).rising(limit=10)])
    df_controversial = pd.DataFrame([submission_to_df(submission, "controversial") for submission in reddit.subreddit(subreddit_name).controversial(limit=10)])

    df = pd.concat([df_hot, df_new, df_top, df_rising, df_controversial])
    print("dataframe made")
    return df