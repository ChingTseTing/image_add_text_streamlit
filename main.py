import streamlit as st
import numpy as np
from PIL import Image , ImageDraw , ImageFont
import os
from datetime import datetime
import io
# https://stackoverflow.com/questions/77038132/python-pillow-pil-doesnt-recognize-the-attribute-textsize-of-the-object-imag
def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

FOLDER_PATH = "/content/drive/MyDrive/Colab_Notebooks/image_add_text"
FONTS="Harshita.ttf" #"Harshita.ttf"




st.title("Image add text")
with st.form(key='user_form'):
    TEXT = st.text_input("Enter your text to add")
    uploaded_files = st.file_uploader("Upload images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    x_frac = st.number_input(label="x location", min_value=0.0, max_value=1.0, value=0.8)
    y_frac = st.number_input(label="y location", min_value=0.0, max_value=1.0, value=0.9)
    submit_button = st.form_submit_button(label="Submit")





# Process form submission
if submit_button and uploaded_files is not None:

  for i in uploaded_files :
    tmp = Image.open(   i   )
    draw = ImageDraw.Draw(tmp)
    font = ImageFont.truetype( font = os.path.join( FOLDER_PATH , "Fonts", FONTS)  , size = int(min(tmp.size[0],tmp.size[1])/40) )

  # print ( "Before: " ,INPUT_FILES[i]," After: " ,  str(i)+'.jpg' , " Ver: ", tmp.size[0]," Hor: ",tmp.size[1] ," Size: ",tmp.size[0]*tmp.size[1]  )



    text_width, text_height =textsize(TEXT, font)
    crop_box = (  0.8*tmp.size[0] ,  0.7*tmp.size[1] ,  0.8*tmp.size[0] + text_width, 0.7*tmp.size[1] + text_height)
    cropped_image = tmp.crop(crop_box)
    avg_brightness = np.mean(np.array(cropped_image.convert("L")))
    text_color = (255, 255, 255) if avg_brightness < 128 else (0, 0, 0)

    draw.text( xy=( x_frac*tmp.size[0] , y_frac*tmp.size[1] ) , text = TEXT ,font=font , fill = text_color , thickness=5)
    #draw.text( xy=( 0.8*tmp.size[0] , 0.8*tmp.size[1] ) , text = TEXT ,font=font , fill = text_color , thickness=5)

    st.write(f"Image size: {tmp.size}")

    # Convert the processed image to bytes
    img_byte_arr = io.BytesIO()
    tmp.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create a download button for the processed image

    st.download_button(
        label="Download Processed Image",
        data=img_byte_arr,
        file_name=f"processed_{i.name}",
        mime="image/png"
    )
