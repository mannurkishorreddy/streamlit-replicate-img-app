<img src="images/ME-Naics-7225-A-small-honey-bee-is-near-a_wide.jpg" alt="Streamlit Replicate Image App" style="width:100%;max-width:1000px">

# Replicate Image Generator

## Supports loading prompts from a CSV file, and outputing images directly to GitHub

"Replicate Image Generator" is a Streamlit application designed to transform text prompts into stunning visual images using the Replicate API. Users can enter a prompt or optionally read prompts from a CSV file. Images are generated in different aspect ratios and can be saved directly to a GitHub repository for easy access and embedding using either our [JQuery Images Display](https://model.earth/replicate/images/) or our [React Gallery](https://model.earth/replicate/gallery/).

### Features

- **Prompt Selection**: Users can choose from a variety of predefined prompts listed in a CSV file.
- **Image Generation**: The app generates images based on the selected prompt using the Replicate model.
- **Multiple Aspect Ratios**: Supports the creation of images in square and horizontal formats.
- **GitHub Integration**: Automatically saves generated images to a specified GitHub repository.

## Getting Started

### Prerequisites

- Streamlit
- Pandas
- Replicate Python Client
- Python Requests
- Pillow (PIL)

### Installation

1.) Clone the repository to your local computer.

2.) Navigate to the directory, start a virtual env, and install the required packages:
   
   ```bash
   python3 -m venv env && source env/bin/activate &&
   pip install -r requirements.txt
   ```

3.) Save a copy of example_secrets.toml as secrets.toml

4.) If you will be sending files to your GitHub account, in .streamlit/secrets.toml add:

GITHUB_TOKEN
GITHUB_REPOSITORY

To create a GitHub.com token, go to: Settings -> Developer Settings -> [Personal access tokens](https://github.com/settings/tokens)

It's not necessary to check any of the access boxes for the GitHub token.

5.) Set your Replicate API Token in .streamlit/secrets.toml. 

You can get a free [Replicate API Token](https://replicate.com/docs/reference/http#authentication), but they are slow.

6.) Update the CSV file with your prompts.

7.) Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

8.) Open the Streamlit app in your web browser.

9.) Use the sidebar to select a prompt from the CSV file.

10.) Click on 'Generate Image' to start the image generation process.

11.) View the generated images in different aspect ratios.

12.) Check your GitHub repository for the saved images.


## Contributing

Contributions to improve this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.
