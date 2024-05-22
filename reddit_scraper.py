import os

#Reddit API Keys
CLIENT_ID = 'client id key goes here'
SECRET_KEY = 'secret key goes here'

#Imports and authentications for API
import requests
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

#Read Reddit account password from separate file 
with open('pw.txt', 'r') as f:
    pw = f.read()

#Reddit user login data
data = {
    'grant_type': 'password',
    'username': 'reddit username goes here',
    'password': pw
}

#Identify Version of API
headers = {'User-Agent': 'RedditTikTokFarm/0.0.1'}

#Sends API Request
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

# List of predefined subreddits
subreddits = ['r/Advice', 'r/AskReddit', 'r/amiwrong', 'r/AmItheAsshole', 'r/BestofRedditorUpdates']

# Display the options to the user
print("What subreddit do you want to pull from?:")
for i, subreddit in enumerate(subreddits, start=1):
    print(f"{i}: {subreddit}")
print(f"{len(subreddits) + 1}: Enter your own subreddit")

# Get the user's choice
choice = input("Select an option: ")

# Check if the user chose to enter their own subreddit
if choice == str(len(subreddits) + 1):
    subreddit_name = input("Enter the subreddit name (format 'r/SubredditName'): ")
else:
    # Validate the choice and retrieve the corresponding subreddit
    try:
        choice_index = int(choice) - 1
        subreddit_name = subreddits[choice_index]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        exit()

# Ensure the input format is correct, strip any leading 'r/' if present
if subreddit_name.startswith('r/'):
    subreddit_name = subreddit_name[2:]

# Construct the URL with the specified subreddit
url = f'https://oauth.reddit.com/r/{subreddit_name}/hot'

#Retrieve Posts from specified Subreddit
res = requests.get(url, headers=headers)

#Import pandas dataframe to clean up data
import pandas as pd

df = pd.DataFrame()

for post in res.json()['data']['children']:
   df = df._append({
       
       'subreddit': post['data']['subreddit'], 
       'title': post['data']['title'],
       'selftext': post['data']['selftext'],
       'upvote_ratio': post['data']['upvote_ratio'],
       'ups': post['data']['ups'],
       'downs': post['data']['downs'],
       }, ignore_index=True)

# Display the DataFrame with indices so the user can choose
print(df)

df.to_string()

# Prompt the user for the post number
post_number = int(input("Enter the number of the post to export to text files: "))

# Check if the selected post number is valid
if 0 <= post_number < len(df):
    # Retrieve the title and selftext of the chosen post
    title = df.iloc[post_number]['title']
    selftext = df.iloc[post_number]['selftext']  # Corrected line

    # Define the directory to save text files
    text_output_directory = 'text_output_files'
    os.makedirs(text_output_directory, exist_ok=True)  # Create directory if it doesn't exist

    # Write the title to its own file
    title_filename = os.path.join(text_output_directory, 'TITLE.txt')
    with open(title_filename, 'w', encoding='utf-8') as title_file:
        title_file.write(title)
    print(f"The title has been exported to {title_filename}")

    # Write the selftext to its own file
    selftext_filename = os.path.join(text_output_directory, 'BODY.txt')
    with open(selftext_filename, 'w', encoding='utf-8') as selftext_file:
        selftext_file.write(selftext)
    print(f"The selftext has been exported to {selftext_filename}")

    # Write both title and selftext to a combined file
    combined_filename = os.path.join(text_output_directory, 'TITLE_AND_BODY.txt')
    with open(combined_filename, 'w', encoding='utf-8') as combined_file:
        combined_file.write(f"{title}\n\n{selftext}")
    print(f"The title and selftext have been combined and exported to {combined_filename}")


else:
    print("Invalid post number. Exiting.")
    