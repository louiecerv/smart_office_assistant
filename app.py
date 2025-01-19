import streamlit as st
from PIL import Image
import os
import tempfile
from aiutils import generate_text

# Set your Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()

st.title("WVSU Office Assistant")

with st.expander("ℹ️ About"):
    st.write("""
WVSU Office Assistant is an AI-powered document analysis tool designed to help 
faculty and staff process images and PDFs efficiently. Users can upload or 
capture documents, provide instructions, and receive AI-generated insights. 
Simplify office tasks with automated document interpretation and analysis.
""")
    
    st.write("""Created by:
Louie F. Cervantes, M.Eng.(Information Engineering).\n
Computer Sciience Department,
College of Information and Communications Technology\n
(c) 2025 Western Visayas State University             
""")

tabs = st.tabs(["Upload Document", "Take Photo"])

uploaded_file = None
captured_image = None
mime_type = None
file_path = None  # Store the file path for both PDFs & images

with tabs[0]:  # Upload Document Tab
    uploaded_file = st.file_uploader("Choose a document", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file is not None:
        mime_type = uploaded_file.type

        if mime_type.startswith('image'):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_container_width=True)

            # Save image as a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                image.save(temp_file, format="PNG")
                file_path = temp_file.name  # Store file path

        elif mime_type == "application/pdf":
            pdf_bytes = uploaded_file.getvalue()
            if len(pdf_bytes) == 0:  # Prevent empty PDFs
                st.error("The uploaded PDF is empty. Please upload a valid document.")
                st.stop()

            # Write PDF bytes to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_bytes)
                file_path = temp_file.name  # Store file path

with tabs[1]:  # Take Photo Tab
    captured_image = st.camera_input("Take a photo")
    if captured_image:
        mime_type = captured_image.type
        image = Image.open(captured_image)
        st.image(image, caption="Captured Image.", use_container_width=True)

        # Save captured image as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image.save(temp_file, format="JPEG")
            file_path = temp_file.name  # Store file path

prompt = st.text_area("Enter instructions for document analysis:", height=150)

if st.button("Analyze"):
    if file_path:
        try:
            analysis_result = generate_text(file_path, mime_type, prompt)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload a document or take a photo first.")
