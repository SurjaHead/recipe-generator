from dotenv import load_dotenv
import os
import base64
import requests
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Recipe Generator",
    page_icon="🍳",
)

st.title("Recipe Generator")
st.write("This app uses OpenAI's GPT-4 model to generate recipes based on the ingredients in the image you upload.")

picture = st.camera_input("Take a picture")
cuisine = st.text_input("What type of food would you like?", "Indian")

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Function to save the image
def save_image(picture, filename):
    with open(filename, "wb") as f:
        f.write(picture.read())

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

if picture:
    # Save the image to a file
    image_path = "temp_image.jpg"
    save_image(picture, image_path)

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Give me a recipe can be made with the ingredients in this image. Include the preparation time. The recipe should be of " + cuisine + " cuisine."
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300,
    "temperature": 0
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    st.write(response.json().get("choices")[0].get("message").get("content"))