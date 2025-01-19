import streamlit as st
import google.generativeai as genai
import os

MODEL_ID = "gemini-2.0-flash-exp" 
api_key = os.getenv("GEMINI_API_KEY")
model_id = MODEL_ID
genai.configure(api_key=api_key)
ENABLE_STREAMING = True

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(MODEL_ID)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat()

def generate_text(image_path, mime_type, prompt):
    try:
        chat = st.session_state.chat
        
        response = None

        # Handle  if only a text prompt is provided
        if not image_path:
            # Send file and prompt to Gemini API
            response = chat.send_message(
                [ prompt ],
                stream = ENABLE_STREAMING
            )

        # Handle if an image is provided
        else:
            # Upload the file with the correct MIME type
            file_data = genai.upload_file(image_path, mime_type=mime_type)
            
            # Send file and prompt to Gemini API
            response = chat.send_message(
                [
                    prompt, 
                    file_data
                ],
                stream = ENABLE_STREAMING
            )

        full_response = ""
        if ENABLE_STREAMING:
            response_placeholder = st.empty()
            # Process the response stream
            for chunk in response:
                full_response += chunk.text                        
                response_placeholder.markdown(full_response)  
        else:
            # Extract and display the response
            full_response = response.text
            st.markdown(full_response)  

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

