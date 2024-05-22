This application turns Reddit Posts into subtitled videos with a text to speech audio. Each video has a custom thumbnail based off the Reddit post's title, a background video randomly selected for aethestics, and is automatically cropped to a 9:16 aspect ratio in 720p.


HOW TO RUN:

Create/Setup Reddit API Keys:
1. Go to https://old.reddit.com/prefs/apps/
2. Login/Create an account.
3. Select 'create application' and fill in the fields (doesn't have to be any specific info).
4. Save your CLIENT_ID & SERIAL_ID.
5. 1. In your local repo, type your Reddit password in the 'pw.txt' file.
6. In the 'reddit_scraper.py' file, on line 4 & 5 type in your CLIENT_ID & SERIAL_ID.
7. In the 'reddit_scraper.py' file, on line 18 type in your reddit username (username used for logging into your account).

Create AssemblyAPI Key:
1. Go to https://www.assemblyai.com/
2. Create Account/Login
3. Generate API key
4. In the 'video_creation.py' file, on line 10 type in your assembly api key.

Install Dependencies:
1. install dependencies from the requirements.txt file by running this command in your local directory.
2. pip install -r requirements.txt
3. If 'requirements.txt' is giving you trouble, individually pip install/upgrade the libraries used in this project:
pandas,
requests,
moviepy,
gtts,
assemblyai,
Pillow


Set Up Background Videos:
1. Download any videos you want playing in the background (YouTube to MP4 converter works well).
2. Put all background videos in the 'background_videos' folder.

CODE EXECUTION ORDER:
1. Run 'reddit_scraper.py' to select reddit post and generate transcripts for post.
2. Run 'thumbnail_creation.py' to create a thumbnail image for your video.
3. Run 'video_creation.py' to create your video equipped with text-to-speech audio, subtitles, background video, and thumbnail.
