import streamlit as st
import requests
import time

api_key = "915fb846-4ab0-4349-b535-bf45e1fbc613"
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

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
    response_image = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations", json=payload_image, headers=headers)
    if response_image.status_code != 200:
        st.error(f"Failed to generate initial image: {response_image.text}")
        return

    generation_id = response_image.json().get('sdGenerationJob', {}).get('generationId')
    time.sleep(60)  # Wait for the image generation to complete

    # Fetch the generated image
    response_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}", headers=headers)
    image_id = response_generation.json()['generations_by_pk']['generated_images'][0]['id']

    # Create an image variation (upscale)
    payload_variation = {"id": image_id}
    response_variation = requests.post("https://cloud.leonardo.ai/api/rest/v1/variations/upscale", json=payload_variation, headers=headers)
    time.sleep(100)  # Ensuring variation process completes

    image_variation_id = response_variation.json().get('sdUpscaleJob', {}).get('id')

    # Generate video with the variation
    payload_video = {
        "imageId": image_variation_id,
        "motionStrength": 10,
        "isVariation": True
    }
    response_video = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd", json=payload_video, headers=headers)
    if response_video.status_code != 200:
        st.error(f"Failed to initiate video generation: {response_video.text}")
        return

    generation_id_video = response_video.json().get('motionSvdGenerationJob', {}).get('generationId')
    time.sleep(60)  # Wait for the video generation to complete

    # Fetch and display the video
    response_video_generation = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id_video}", headers=headers)
    video_url = response_video_generation.json().get('motion_svd_generations_by_pk', {}).get('generated_videos', [{}])[0].get('url')

    st.video(video_url)

st.title('Video Generation with Leonardo AI')
prompt = st.text_input("Enter your prompt for the video generation:")
if st.button("Generate Video") and prompt:
    with st.spinner("Generating Video..."):
        generate_and_upload_video(prompt)
