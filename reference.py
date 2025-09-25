import praw

CLIENT_ID = "HRkWE5YFju2vWzsidgnk-A"
CLIENT_SECRET = "zLKngu30DLNhPWeB6wC3kRX_fsktNg"
REDIRECT_URI = "http://localhost:8080"
USER_AGENT = "windows:reddit_ai_agent:v1.0"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,          
    redirect_uri=REDIRECT_URI,
    user_agent=USER_AGENT
)

# Step 1: Generate authorization URL
scopes = ["identity", "read"]  # add more scopes as needed
auth_url = reddit.auth.url(scopes=scopes, state="uniqueKey", duration="permanent")
print("1️⃣ Visit this URL in your browser to authorize the app:\n")
print(auth_url)
print("\nAfter authorizing, Reddit will redirect to your REDIRECT_URI with a 'code' in the URL.")

# Step 2: Enter the code from the redirect URL
code = input("2️⃣ Paste the 'code' parameter from the URL here: ").strip()

# Step 3: Exchange code for refresh token
refresh_token = reddit.auth.authorize(code)
print("\n✅ Your refresh token is:\n", refresh_token)
print("\n💡 Save this token safely — you can now use it in your bot without your password.")

# Step 4: Test login using refresh token
reddit_bot = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    refresh_token=refresh_token,
    user_agent=USER_AGENT
)

print("\nTesting login with refresh token...")
print("Logged in as:", reddit_bot.user.me())

# Example: fetch 5 hot posts from r/Python
print("\nTop 5 hot posts from r/Python:")
for submission in reddit_bot.subreddit("Python").hot(limit=5):
    print("-", submission.title)
