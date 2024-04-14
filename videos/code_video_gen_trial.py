import streamlit as st
import requests
import time

# Function to handle the generation and uploading of a video
def generate_and_upload_video(prompt):
    # Step 1: Generate initial image
    response_image = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/generations",
        json={
            "height": 768,
            "width": 1024,
            "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
            "prompt": prompt,
            "num_images": 1,
            "alchemy": True
        },
        headers=headers
    )
    if response_image.status_code != 200:
        st.error("Failed to generate initial image")
        return

    generation_id = response_image.json().get('sdGenerationJob', {}).get('generationId')
    if not generation_id:
        st.error("No generation ID found in the response.")
        return

    time.sleep(60)  # Wait for the image generation to complete

    # Step 2: Fetch the generated image
    response_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}", headers=headers)
    if response_generation.status_code != 200 or 'generated_images' not in response_generation.json().get('generations_by_pk', {}):
        st.error("Failed to fetch generated images or no images returned.")
        return

    image_id = response_generation.json()['generations_by_pk']['generated_images'][0]['id']

    # Step 3: Create an image variation (upscale)
    response_variation = requests.post("https://cloud.leonardo.ai/api/rest/v1/variations/upscale", json={"id": image_id}, headers=headers)
    if response_variation.status_code != 200:
        st.error("Failed to create image variation.")
        return

    variation_response = response_variation.json()
    if 'sdUpscaleJob' not in variation_response:
        st.error(f"Unexpected response structure: {variation_response}")
        return

    image_variation_id = variation_response['sdUpscaleJob']['id']

    # Step 4: Generate video with the variation
    response_video = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd",
        json={"imageId": image_variation_id, "motionStrength": 10, "isVariation": True},
        headers=headers
    )
    if response_video.status_code != 200:
        st.error("Failed to initiate video generation.")
        return

    generation_id_video = response_video.json().get('motionSvdGenerationJob', {}).get('generationId')
    if not generation_id_video:
        st.error("No video generation ID found.")
        return

    time.sleep(60)  # Wait for the video generation to complete

    # Step 5: Fetch and display or upload the video
    response_video_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id_video}", headers=headers)
    if response_video_generation.status_code != 200:
        st.error("Failed to fetch the generated video.")
        return

    video_url = response_video_generation.json().get('motion_svd_generations_by_pk', {}).get('generated_videos', [{}])[0].get('url')
    if not video_url:
        st.error("No video URL found.")
        return

    # Optional: Show video in Streamlit
    st.video(video_url)

    # Optional: Save video to GitHub
    video_content = requests.get(video_url).content
    save_video_to_github(video_content, "generated_video.mp4", "videos/leonardo", "New video upload", github_token)

# Streamlit interface to initiate the process
st.title('Video Generation with Leonardo AI')
prompt = st.text_input("Enter your prompt for the video generation:")
if st.button("Generate Video"):
    if prompt:
        with st.spinner("Generating Video..."):
            generate_and_upload_video(prompt)
    else:
        st.error("Please enter a valid prompt.")