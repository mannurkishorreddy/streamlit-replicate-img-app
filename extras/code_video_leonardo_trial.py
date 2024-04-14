import streamlit as st
import requests
import time

# Define your API key and headers
api_key = "915fb846-4ab0-4349-b535-bf45e1fbc613"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Streamlit app title
st.title('Video Generation with Leonardo AI')

# Text input for user prompt
prompt = st.text_input("Enter your prompt for the video generation:")

# Function to handle video generation and display
def generate_and_upload_video(prompt):
    # Generate initial image
    payload_image = {
        "height": 768,
        "width": 1024,
        "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
        "prompt": prompt,
        "num_images": 1,
        "alchemy": True
    }
    
    # Make the API call to generate the initial image
    response_image = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations", json=payload_image, headers=headers)
    
    # Check for errors in initial image generation
    if response_image.status_code != 200:
        st.error(f"Failed to generate initial image: {response_image.text}")
        return
    response_image_data = response_image.json()
    if 'sdGenerationJob' not in response_image_data:
        st.error(f"Unexpected response structure for image generation: {response_image_data}")
        return
    
    # Extract the generation ID from the response
    generation_id = response_image_data['sdGenerationJob'].get('generationId')
    if not generation_id:
        st.error(f"No generation ID found in the image generation response: {response_image_data}")
        return
    time.sleep(60)  # Wait for image generation to complete

    # Fetch the generated image using the generation ID
    response_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}", headers=headers)
    
    # Check for errors in fetching the generated image
    if response_generation.status_code != 200:
        st.error(f"Failed to fetch generated image: {response_generation.text}")
        return
    response_generation_data = response_generation.json()
    if 'generations_by_pk' not in response_generation_data:
        st.error(f"Unexpected response structure when fetching image generation data: {response_generation_data}")
        return
    
    generated_images = response_generation_data['generations_by_pk'].get('generated_images')
    if not generated_images:
        st.error(f"No generated images found in the response: {response_generation_data}")
        return
    image_id = generated_images[0]['id']
    time.sleep(10)  # Small delay before the next step

    # Other API calls and error checks continue as before...

# Button to generate video
if st.button("Generate Video"):
    if prompt:
        with st.spinner("Generating Video..."):
            generate_and_upload_video(prompt)
    else:
        st.error("Please enter a valid prompt.")
