import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Loading the environment variables
load_dotenv()

# Configuring the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image, input):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0], input])
    return response.text

# Function for defining the input format of the gemini model


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        return image_parts

    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit app
st.set_page_config(page_title="Calories Advisor App")
st.header("Calories Advisor App")

input = st.text_input("Input Prompt:", key='input')

uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "png", "jpeg"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
            Finally, you can also mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugar and other important things required in our diet

"""

# If submit is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is:")
    st.write(response)