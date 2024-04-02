import streamlit as st
import pandas as pd
import base64
import requests
import io
from PIL import Image

# UI configurations
st.set_page_config(page_title="Leonardo Image Generator based on CSV Input", page_icon="🌟")

# API Tokens and endpoints from `.streamlit/secrets.toml` file
LEONARDO_API_TOKEN = st.secrets["LEONARDO_API_TOKEN"]
LEONARDO_ENDPOINT = st.secrets["LEONARDO_ENDPOINT"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPOSITORY = "your_github_repo/streamlit-leonardo-img-app" # Replace with your GitHub repo

# Function to convert the image to JPEG
def convert_to_jpeg(image_content):
    image = Image.open(io.BytesIO(image_content))
    with io.BytesIO() as output_stream:
        image.save(output_stream, format="JPEG")
        return output_stream.getvalue()

# Function to save the image to GitHub
def save_image_to_github(image_content, filename, repo_name, path_in_repo, commit_message, github_token):
    url = f"https://api.github.com/repos/{repo_name}/contents/{path_in_repo}/{filename}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "message": commit_message,
        "content": base64.b64encode(image_content).decode('utf-8'),
        "branch": "main",
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        st.success("Image successfully uploaded to GitHub.")
    else:
        st.error(f"Failed to upload image: {response.content}")

def main():
    df = pd.read_csv("ME-prompts-2021.csv")
    df['Display Prompt'] = df['Prompt'].str.replace("--no signage", "").str.strip()
    options = df['Display Prompt'].tolist()
    st.sidebar.title("Choose Your Prompt")
    selected_display_prompt = st.sidebar.selectbox('', options, index=0, help="Select a prompt from the list")

    st.title("Leonardo AI Image Generator")
    st.markdown("### Transform your ideas into stunning visuals!")
    
    if st.button('Generate Image', key='generate'):
        with st.spinner('🧚‍♂️ Creating magic...'):
            try:
                selected_row = df[df['Display Prompt'] == selected_display_prompt]
                selected_prompt = selected_row['Prompt'].values[0]
                naics_value = selected_row['Naics'].values[0]
                first_five_words = "-".join(selected_prompt.split()[:5])

                for ratio, dimensions, suffix in [("square", (1024, 1024), "sq"), ("horizontal", (1792, 896), "wide")]:
                    response = requests.post(
                        LEONARDO_ENDPOINT,
                        headers={"Authorization": f"Bearer {LEONARDO_API_TOKEN}"},
                        json={"prompt": selected_prompt, "width": dimensions[0], "height": dimensions[1]}
                    )

                    if response.status_code == 200:
                        # Assuming the response contains a direct link to the image
                        output = response.json().get('image_url')
                        image_response = requests.get(output)
                        if image_response.status_code == 200:
                            jpeg_content = convert_to_jpeg(image_response.content)
                            filename = f"ME-Naics-{naics_value}-{first_five_words}_{suffix}.jpg"
                            commit_message = "Add generated image"
                            save_image_to_github(
                                jpeg_content, 
                                filename, 
                                GITHUB_REPOSITORY, 
                                "images", 
                                commit_message, 
                                GITHUB_TOKEN
                            )
                            st.image(output, caption=f"Generated Image - {ratio}", use_column_width=True)
                        else:
                            st.error("Failed to download the generated image.")
                    else:
                        st.error(f"Failed to generate image. Status code: {response.status_code}")
            except Exception as e:
                st.error(f'Encountered an error: {e}')

if __name__ == "__main__":
    main()
