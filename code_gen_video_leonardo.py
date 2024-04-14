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
    
    generated_images = response_generation_data['generations_by_pk'].get('generated_images', [])
    if not generated_images:
        st.error("Generated images list is empty.")
        return
    image_id = generated_images[0]['id']
    time.sleep(10)  # Small delay before the next step

    # Create a variation of the generated image (e.g., upscale)
    payload_variation = {"id": image_id}
    response_variation = requests.post("https://cloud.leonardo.ai/api/rest/v1/variations/upscale", json=payload_variation, headers=headers)
    if response_variation.status_code != 200:
        st.error(f"Failed to create image variation: {response_variation.text}")
        return
    time.sleep(100)  # Ensuring variation process completes

    # Extract the variation ID
    variation_response = response_variation.json()
    image_variation_id = variation_response.get('sdUpscaleJob', {}).get('id')
    if not image_variation_id:
        st.error(f"No image variation ID found in the response: {variation_response}")
        return

    # Generate video with the image variation
    payload_video = {
        "imageId": image_variation_id,
        "motionStrength": 10,
        "isVariation": True
    }
    response_video = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd", json=payload_video, headers=headers)
    if response_video.status_code != 200:
        st.error(f"Failed to initiate video generation: {response_video.text}")
        return
    time.sleep(60)  # Wait for video generation to complete

    # Fetch the generated video
    video_generation_response = response_video.json()
    generation_id_video = video_generation_response.get('motionSvdGenerationJob', {}).get('generationId')
    if not generation_id_video:
        st.error(f"No video generation ID found in the response: {video_generation_response}")
        return

    response_video_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id_video}", headers=headers)
    if response_video_generation.status_code != 200:
        st.error(f"Failed to fetch generated video: {response_video_generation.text}")
        return

    video_info = response_video_generation.json().get('motion_svd_generations_by_pk', {})
    if 'generated_videos' in video_info:
        video_url = video_info['generated_videos'][0].get('url')
        if video_url:
            st.success("Video has finished generating!")
            st.video(video_url)

            # Download the video content for saving locally
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                st.download_button(
                    label="Download Video",
                    data=video_response.content,
                    file_name="generated_video.mp4",
                    mime="video/mp4"
                )
            else:
                st.error("Failed to download the video content.")
        else:
            st.error("No video URL found.")
    else:
        st.error("No video information found in the response.")

# Button to generate video
if st.button("Generate Video"):
    if prompt:
        with st.spinner("Generating Video..."):
            generate_and_upload_video(prompt)
    else:
        st.error("Please enter a valid prompt.")
