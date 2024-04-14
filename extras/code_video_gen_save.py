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
    
    # Check for errors
    if response_image.status_code != 200:
        st.error(f"Failed to generate initial image: {response_image.text}")
        return

    # Extract the generation ID from the response
    generation_id = response_image.json().get('sdGenerationJob', {}).get('generationId')
    time.sleep(60)  # Wait for image generation to complete

    # Fetch the generated image using the generation ID
    response_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}", headers=headers)
    
    # Check for errors
    if response_generation.status_code != 200:
        st.error("Failed to fetch generated image.")
        return

    image_id = response_generation.json()['generations_by_pk']['generated_images'][0]['id']
    time.sleep(10)  # Small delay before the next step

    # Create a variation of the generated image
    response_variation = requests.post("https://cloud.leonardo.ai/api/rest/v1/variations/upscale", json={"id": image_id}, headers=headers)
    
    # Check for errors
    if response_variation.status_code != 200:
        st.error("Failed to create image variation.")
        return

    # Extract the variation ID from the response
    image_variation_id = response_variation.json().get('sdUpscaleJob', {}).get('id')
    time.sleep(100)  # Wait for the upscale variation to complete

    # Generate video with the image variation
    payload_video = {
        "imageId": image_variation_id,
        "motionStrength": 10,
        "isVariation": True
    }
    
    # Make the API call to generate the video
    response_video = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd", json=payload_video, headers=headers)
    
    # Check for errors
    if response_video.status_code != 200:
        st.error(f"Failed to initiate video generation: {response_video.text}")
        return

    # Extract the generation ID for the video
    generation_id_video = response_video.json().get('motionSvdGenerationJob', {}).get('generationId')
    time.sleep(60)  # Wait for video generation to complete

    # Fetch the generated video using the generation ID
    response_video_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id_video}", headers=headers)
    
    # Check for errors
    if response_video_generation.status_code != 200:
        st.error("Failed to fetch generated video.")
        return

    # Extract the video URL from the response
    video_url = response_video_generation.json().get('motion_svd_generations_by_pk', {}).get('generated_videos', [{}])[0].get('url')
    
    # Check if the video URL exists
    if video_url:
        # Display the video in Streamlit
        st.video(video_url)
        
        # Fetch the video content for download
        video_response = requests.get(video_url)
        
        # Check for errors
        if video_response.status_code == 200:
            # Create a download button for the video
            st.download_button(
                label="Download Video",
                data=video_response.content,
                file_name="generated_video.mp4",
                mime="video/mp4"
            )
        else:
            st.error("Failed to download the video.")
    else:
        st.error("No video URL found.")

# Button to generate video
if st.button("Generate Video"):
    if prompt:
        with st.spinner("Generating Video..."):
            generate_and_upload_video(prompt)
    else:
        st.error("Please enter a valid prompt.")
