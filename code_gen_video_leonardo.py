
import requests
import streamlit as st
import base64
import time


api_key = "915fb846-4ab0-4349-b535-bf45e1fbc613"
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# Function to handle the generation and uploading of a video
def generate_and_upload_video(prompt):
    # Step 1: Generate initial image
    payload_image = {
        "height": 768,
        "width": 1024,
        "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
        "prompt": prompt,
        "num_images": 1,
        "alchemy": True
    }
    response_image = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations", json=payload_image, headers=headers)
    if response_image.status_code != 200:
        st.error("Failed to generate initial image")
        return

    generation_id = response_image.json()['sdGenerationJob']['generationId']
    time.sleep(60)  # Wait for the image generation to complete

    # Step 2: Fetch the generated image
    url_generation = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    response_generation = requests.get(url_generation, headers=headers)
    image_id = response_generation.json()['generations_by_pk']['generated_images'][0]['id']

    # Step 3: Create an image variation (upscale)
    payload_variation = {"id": image_id}
    response_variation = requests.post("https://cloud.leonardo.ai/api/rest/v1/variations/upscale", json=payload_variation, headers=headers)
    time.sleep(100)  # Ensuring variation process completes

    image_variation_id = response_variation.json()['generated_image_variation_generic'][0]['id']

    # Step 4: Generate video with the variation
    payload_video = {
        "imageId": image_variation_id,
        "motionStrength": 10,
        "isVariation": True
    }
    response_video = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd", json=payload_video, headers=headers)
    generation_id_video = response_video.json()['motionSvdGenerationJob']['generationId']
    time.sleep(60)  # Wait for the video generation to complete

    # Step 5: Fetch and display or upload the video
    url_video_generation = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id_video}"
    response_video_generation = requests.get(url_video_generation, headers=headers)
    video_url = response_video_generation.json()['motion_svd_generations_by_pk']['generated_videos'][0]['url']
    
    # Optional: Show video in Streamlit
    st.video(video_url)

    # Optional: Save video to GitHub
    video_content = requests.get(video_url).content
    save_video_to_github(video_content, "generated_video.mp4", "videos/leonardo.", "New video upload", github_token)

# Streamlit interface for user input
st.title('Video Generation with Leonardo AI')
prompt = st.text_input("Enter your prompt for the video generation:", "Golden hour photograph of family biking under a tree canopy near a location with Building Equipment Contractors in Maine in 2021.")

# Streamlit button to initiate video generation
if st.button("Generate Video"):
    if prompt:
        with st.spinner("Generating Video..."):
            generate_and_upload_video(prompt)
    else:
        st.error("Please enter a valid prompt.")