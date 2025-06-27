import requests
import streamlit as st

def generate_all(resume_text, job_description, user_notes):
    """
    Calls the backend API to generate the application content.
    """
    # Get the backend URL from Streamlit's secrets
    # The key 'HF_SPACE_URL' should match what you set in Streamlit Cloud
    API_URL = st.secrets.get("HF_SPACE_URL")

    if not API_URL:
        st.error("Backend API URL is not configured. Please set the HF_SPACE_URL secret in your Streamlit app settings.")
        return None

    # The full endpoint URL for the generation function
    endpoint = f"{API_URL}/generate"
    
    payload = {
        "resume_text": resume_text,
        "job_description": job_description,
        "user_notes": user_notes
    }

    try:
        # Make the API call with a generous timeout for the AI model
        response = requests.post(endpoint, json=payload, timeout=300) # 5-minute timeout

        # Check for HTTP errors (like 404, 500, etc.)
        response.raise_for_status() 

        # Return the JSON data from the successful response
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the AI backend: {e}")
        return None
    except Exception as e:
        st.error(f"An unknown error occurred while communicating with the backend: {e}")
        return None