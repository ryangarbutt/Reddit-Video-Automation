from PIL import Image, ImageDraw, ImageFont
import os

def draw_text(draw, text, position, font, max_width, font_size):
    """
    Draw the text on the image with word wrapping, utilizing font size for line height.
    """
    # Split the text into words
    words = text.split()
    lines = []
    line = ""

    # Approximate line height using font size, adding a small buffer
    line_height = font_size * 1.2

    for word in words:
        # Check the width of the line with the new word added
        test_line = f'{line} {word}' if line else word
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            line = test_line
        else:
            # If the line is too wide, start a new line
            lines.append(line)
            line = word
    lines.append(line)  # Add the last line to ensure it is included

    # Draw each line on the image
    y_offset = 0
    for line in lines:
        draw.text((position[0], position[1] + y_offset), line, font=font, fill=text_color)
        y_offset += line_height  # Increment y_offset by the approximate line height for each new line

# Load the image
image = Image.open("thumbnail/thumbnail.png")  # Assuming "thumbnail" folder is in the root directory

# Prepare to draw on the image
d = ImageDraw.Draw(image)

# Choose a font and size
font_size = 55
font_path = "arial.ttf"  # Adjust as necessary
font = ImageFont.truetype(font_path, font_size)

# Read the text from TITLE.txt
with open("text_output_files/TITLE.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()

text_pos = (123, 235)  # Dimensions where the text is entered on the thumbnail
text_color = (0, 0, 0)
max_width = image.width - text_pos[0] * 2  # set maximum width for text

# Call the text-wrapping function with the font size argument
draw_text(d, text, text_pos, font, max_width, font_size)

# Specify the directory path to save the image
output_directory = "thumbnail/"
os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist

# Save the modified image in the specified directory
output_path = os.path.join(output_directory, "output_img.png")
image.save(output_path)
