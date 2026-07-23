import praw
import pandas as pd
import os
from reference import reddit

def do_subreddit_exist(subreddit_name):
    try:
        reddit.subreddit(subreddit_name).id 
        return True
    except Exception as e:
        return False

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
    try:
        subreddit = reddit.subreddit(subreddit_name)
        _ = subreddit.id 
    except Exception: 
        raise ValueError(f"Subreddit r/{subreddit_name} does not exist")  
    
    print("making dataframe")
    df_hot = pd.DataFrame([submission_to_df(submission, "hot") for submission in reddit.subreddit(subreddit_name).hot(limit=10)])
    df_new = pd.DataFrame([submission_to_df(submission, "new") for submission in reddit.subreddit(subreddit_name).new(limit=10)])
    df_top = pd.DataFrame([submission_to_df(submission, "top") for submission in reddit.subreddit(subreddit_name).top(limit=10)])
    df_rising = pd.DataFrame([submission_to_df(submission, "rising") for submission in reddit.subreddit(subreddit_name).rising(limit=10)])
    df_controversial = pd.DataFrame([submission_to_df(submission, "controversial") for submission in reddit.subreddit(subreddit_name).controversial(limit=10)])

    df = pd.concat([df_hot, df_new, df_top, df_rising, df_controversial])
    print("dataframe made")
    return df