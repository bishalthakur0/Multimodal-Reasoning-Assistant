import streamlit as st
import requests
from PIL import Image
import io
import os

# Set page configuration and theme
st.set_page_config(page_title="Multimodal Reasoning Assistant", layout="wide")

# Custom CSS for dark theme with blue accent
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(to bottom, #0a192f, #0a1525);
    }
    
    /* Text color */
    .stMarkdown, .stTextInput > label, h1, h2, h3, p {
        color: #ffffff !important;
    }
    
    /* File uploader */
    .stUploadedFile {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0ea5e9;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
    }
    
    .stButton > button:hover {
        background-color: #0284c7;
    }
    
    /* Text area */
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("Multimodal Reasoning Assistant")
st.write("Enter your text query and/or upload an image for multimodal reasoning.")

# Text input
text_query = st.text_area("Text Query")

# Image upload
uploaded_file = st.file_uploader("Upload Image", type=["PNG", "JPG", "JPEG"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(uploaded_file, caption=uploaded_file.name)

# Get response button
if st.button("Get Response"):
    try:
        files = {}
        data = {}
        
        if text_query:
            data["text"] = text_query
            
        if uploaded_file:
            files["image"] = ("image.jpg", uploaded_file.getvalue(), "image/jpeg")
            
        # Use environment variable for backend URL, default to localhost for local development
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        response = requests.post(
            f"{backend_url}/encode/",
            data=data,
            files=files
        )
        
        if response.status_code == 200:
            result = response.json()
            st.subheader("Reasoning Assistant Response:")
            st.json(result)
        else:
            st.error(f"Could not connect to the backend. Status code: {response.status_code}. Please ensure the FastAPI server is running.")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend. Please ensure the FastAPI server is running. Error: {e}")