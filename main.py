import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import io
import zipfile

# Function to calculate text size
def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

FOLDER_PATH = "./"
FONT_FILES = []
for i in os.listdir("./Fonts"):
    if ".ttf" in  i :
        FONT_FILES.append(i)

st.title("Image add text")

# Form for user input
with st.form(key='user_form'):
    TEXT = st.text_input("Enter your text to add",value="Iris Chong")
    FONTS = st.selectbox("Choose an FONTS:", FONT_FILES , index=0)
    uploaded_files = st.file_uploader("Upload images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    x_frac = st.number_input(label="x location", min_value=0.0, max_value=1.0, value=0.8)
    y_frac = st.number_input(label="y location (top/bottom: 0/1)", min_value=0.0, max_value=1.0, value=0.9)
    submit_button = st.form_submit_button(label="Submit")

# Processed images and info lists
processed_images = []
processed_file_names = []

# Process form submission
if submit_button and uploaded_files:
    
    progress_bar = st.progress(0)
    for i in range(len(uploaded_files)):
        # Open and process image
        tmp = Image.open(uploaded_files[i])
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(font=os.path.join(FOLDER_PATH, "Fonts", FONTS), size=int(min(tmp.size) / 40))

        # Calculate text position and color based on brightness
        text_width, text_height = textsize(TEXT, font)
        crop_box = (0.8 * tmp.size[0], 0.7 * tmp.size[1], 0.8 * tmp.size[0] + text_width, 0.7 * tmp.size[1] + text_height)
        cropped_image = tmp.crop(crop_box)
        avg_brightness = np.mean(np.array(cropped_image.convert("L")))
        text_color = (255, 255, 255) if avg_brightness < 128 else (0, 0, 0)

        # Draw the text on the image
        draw.text((x_frac * tmp.size[0], y_frac * tmp.size[1]), TEXT, font=font, fill=text_color)

        # Convert the processed image to bytes
        img_byte_arr = io.BytesIO()
        tmp.save(img_byte_arr, format='PNG')
        processed_images.append(img_byte_arr.getvalue())
        processed_file_names.append(f"processed_{uploaded_files[i].name}")
    
        progress_bar.progress(i) 
        
    # Create a ZIP file with all processed images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for img_data, filename in zip(processed_images, processed_file_names):
            zip_file.writestr(filename, img_data)
    
    # Move to the beginning of the BytesIO buffer so it can be read from the start
    zip_buffer.seek(0)

    # Batch download button for all processed images in a ZIP file
    st.download_button(
        label="Download All Processed Images as ZIP",
        data=zip_buffer,
        file_name="processed_images.zip",
        mime="application/zip"
    )
