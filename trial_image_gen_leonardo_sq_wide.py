import streamlit as st
import requests
import time

# Function to Generate Images
def generate_images(api_key, model_id, prompt, height, width):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'height': height,
        'width': width,
        'modelId': model_id,
        'prompt': prompt,
    }
    
    response = requests.post(
        'https://cloud.leonardo.ai/api/rest/v1/generations',
        headers=headers,
        json=data
    )
    return response

# Function to Get the Images
def get_images(api_key, generation_id):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    while True:
        response = requests.get(
            f'https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}',
            headers=headers
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json['generations_by_pk']['status'] != 'PENDING':
                if 'generated_images' in response_json['generations_by_pk']:
                    image_urls = [img['url'] for img in response_json['generations_by_pk']['generated_images']]
                    return image_urls
                break
            time.sleep(10)
    return []

# Main Streamlit App
def main():
    st.title('Automatic Image Generation with Leonardo AI')

    # Predefined API key, Model ID, and Prompt
    api_key = 'your_api_key_here'
    model_id = 'your_model_id_here'
    prompt = 'A beautiful landscape with mountains and a river'

    # Generate Images
    response_square = generate_images(api_key, model_id, prompt, 512, 512)
    response_wide = generate_images(api_key, model_id, prompt, 400, 956)

    if response_square.status_code == 200 and response_wide.status_code == 200:
        gen_id_square = response_square.json()['sdGenerationJob']['generationId']
        gen_id_wide = response_wide.json()['sdGenerationJob']['generationId']

        # Get and Display Images
        images_square = get_images(api_key, gen_id_square)
        images_wide = get_images(api_key, gen_id_wide)

        if images_square:
            st.image(images_square, caption="1:1 Aspect Ratio Image")
        if images_wide:
            st.image(images_wide, caption="2.39:1 Aspect Ratio Image")
    else:
        st.error("Failed to generate images.")

if __name__ == "__main__":
    main()
