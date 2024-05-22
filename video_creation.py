from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, AudioFileClip, vfx, afx, ImageClip
from moviepy.video.tools.subtitles import SubtitlesClip
import gtts
import assemblyai as aai
from PIL import Image
import os
import random


aai.settings.api_key = "a54bb014271a4547b48d73d132073d83"

# import os
# os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI"


# -- start title and body --

with open('text_output_files/title_and_body.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Convert text to speech and save as an audio file
title_and_body_tts = gtts.gTTS(text)
title_and_body_tts.save('tts_audio_files/title_and_body.mp3')

# Load the TTS audio file
title_and_body_tts_audio = AudioFileClip('tts_audio_files/title_and_body.mp3')

# -- end title and body --





# -- start title -- 

with open('text_output_files/title.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Convert text to speech and save as an audio file
title_tts = gtts.gTTS(text)
title_tts.save('tts_audio_files/title_tts.mp3')

# Load the TTS audio file
title_tts_audio = AudioFileClip('tts_audio_files/title_tts.mp3')


title_transcript = aai.Transcriber().transcribe("tts_audio_files/title_tts.mp3")

# -- end title --





# -- start body --

#Open Reddit text file to prepare it for audio conversion
with open('text_output_files/body.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Convert text to speech and save as an audio file
tts = gtts.gTTS(text)
tts.save('tts_audio_files/body_tts.mp3')

# Load the TTS audio file
tts_audio = AudioFileClip('tts_audio_files/body_tts.mp3')


transcript = aai.Transcriber().transcribe("tts_audio_files/body_tts.mp3")

# -- end body





# used for minutes and seconds
def convertTo2Digits(num) -> str:
    ans = ""
    
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)
# used for only miliseconds 
def convertTo3Digits(num) -> str:
    
    if num > 99:
        return str(num)
    elif num > 9:
        return "0" + str(num)
    else:
        return "00" + str(num)
    

srt_file_path = "subtitles/subs.srt"


# -- start subs for body
with open(srt_file_path, "w") as file:
    for index, word in enumerate(transcript.words):
        miliseconds_to_seconds = 1000
        
        
        start_tot_time = word.start + int(title_tts_audio.duration*1000)
        end_tot_time = word.end + int(title_tts_audio.duration*1000)
        
        
        start_minutes = start_tot_time//60//miliseconds_to_seconds
        start_seconds = start_tot_time//miliseconds_to_seconds - start_minutes*60
        start_miliseconds = start_tot_time - start_minutes*60*1000 - start_seconds*1000
        
        end_minutes = end_tot_time//60//miliseconds_to_seconds
        end_seconds = end_tot_time//miliseconds_to_seconds - end_minutes*60
        end_miliseconds = end_tot_time - end_minutes*60*1000 - end_seconds*1000
        
        
        file.write(f"{index}\n")
        file.write(f"{"00:" + convertTo2Digits(start_minutes) + ":" + convertTo2Digits(start_seconds) + "," + convertTo3Digits(start_miliseconds)} --> {"00:" + convertTo2Digits(end_minutes) + ":" + convertTo2Digits(end_seconds) + "," + convertTo3Digits(end_miliseconds)}\n")
        file.write(f"{word.text}\n")
        file.write("\n")
        sentence = ""
#print(transcript.words) 
# -- end subs for body


print(f"SRT file created: {srt_file_path}")
#---- nico test end
subtitles = "subtitles/subs.srt"
f = open(subtitles, "a")
f.write(subtitles)
f.close()


# Specify the directory where your videos are stored
video_directory = 'background_videos'

# List all files in the directory
files = os.listdir(video_directory)

# Filter for video files (e.g., .mp4, .mov). Adjust the extensions as needed.
video_files = [file for file in files if file.endswith('.mp4') or file.endswith('.mov')]

# Ensure there's at least one video file in the directory
if not video_files:
    raise ValueError("No video files found in the directory.")

# Randomly select a video file
selected_video_file = random.choice(video_files)

# Construct the full path to the selected video file
selected_video_path = os.path.join(video_directory, selected_video_file)

# Load the randomly selected background video
background_video = VideoFileClip(selected_video_path).subclip(0, tts_audio.duration+title_tts_audio.duration+2)

#Mutes original background video audio so that it can be replaced with tts audio
background_video  = background_video.without_audio()

#background_video = background_video.set_audio(tts_audio)
background_video = background_video.set_audio(title_and_body_tts_audio)

# Crop the video to 9:16 aspect ratio
new_width = background_video.size[1] * 9 // 16

# Crop the video. Assuming we want to crop from the center
cropped_video = background_video.fx(vfx.crop, width=new_width, x_center=background_video.w / 2)

# When opening and resizing an image
image = Image.open('thumbnail/output_img.png')

# Determine the scale factor
scale_factor = 0.32  # Example: 25% of the video's width

# Calculate new dimensions
thumbnail_width = int(background_video.size[0] * scale_factor)
aspect_ratio = image.height / image.width
thumbnail_height = int(thumbnail_width * aspect_ratio)

# Resize the image
image = image.resize((thumbnail_width, thumbnail_height), Image.LANCZOS)
image.save('thumbnail/resized_output_img.png')  # Save the resized image

logo_clip = ImageClip('thumbnail/resized_output_img.png').set_duration(title_tts_audio.duration).set_position("center", "center")

# Manual adjustment values
adjust_x = 5  # Positive value moves it right, negative left
adjust_y = -75  # Positive value moves it down, negative up

# Set the position of the logo_clip with manual adjustment
logo_clip = logo_clip.set_position(lambda t: (
    cropped_video.size[0] / 2 - logo_clip.size[0] / 2 + adjust_x,  # Center X and adjust
    cropped_video.size[1] / 2 - logo_clip.size[1] / 2 + adjust_y   # Center Y and adjust
))

# Function to generate subtitles from the SRT file
def make_subtitles_layer(srt_file, font_name, fontsize, color, kerning):
    """Helper function to generate a styled subtitles layer."""
    return SubtitlesClip(srt_file, lambda txt: 
        TextClip(txt, font=font_name, fontsize=fontsize, color=color, kerning=kerning))
    
# Define the subtitles file
srt_file = "subtitles/subs.srt"
    
# Create the shadow/outline subtitles layer (black, slightly bigger font)
shadow_subtitles = make_subtitles_layer(srt_file, "IndivisibleBlack", fontsize=52, color="black", kerning = -1)

# Create the main subtitles layer (white, standard font size)
main_subtitles = make_subtitles_layer(srt_file, "IndivisibleBlack", fontsize=50, color="white", kerning = 0)

# Set the position of shadow subtitles slightly off to mimic an outline or shadow effect
shadow_subtitles = shadow_subtitles.set_position(("center", "center")).set_start(0)
main_subtitles = main_subtitles.set_position(("center", "center")).set_start(0)

# Create a composite video clip with both layers of subtitles
# Note: Adjust the position offsets as necessary to get the desired outline effect
final_clip = CompositeVideoClip([cropped_video, logo_clip, shadow_subtitles, main_subtitles])

final_clip.write_videofile("irl_reddit_stories.mp4", fps=60, bitrate="8000k")
