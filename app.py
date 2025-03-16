import streamlit as st
from openai import OpenAI
from together import Together
import os
import base64  
from PIL import Image
import io
import requests.exceptions
import time
import asyncio
from zonos import sync_speech, ZyphraClient

# Initialize API clients with error handling
try:
    openrouter_api_key = st.secrets["OPENROUTER_API_KEY"]
    together_api_key = st.secrets["TOGETHER_API_KEY"]
    zyphra_api_key = st.secrets["ZYPHRA_API_KEY"]
except Exception:
    st.error("One or more API keys not found in Streamlit secrets. Please add them in the Streamlit Cloud dashboard.")
    st.stop()

try:
    qwen_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )
except Exception as e:
    st.error("Failed to initialize Qwen VL client. Please check your API configuration.")
    st.stop()

try:
    Together.api_key = together_api_key
except Exception as e:
    st.error("Failed to initialize Together API client. Please check your API configuration.")
    st.stop()

def get_image_description(image_bytes):
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            completion = qwen_client.chat.completions.create(
                model="qwen/qwen-vl-max",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze the following product image and generate a comprehensive description. Focus on the product's key features, design details, colors, materials, and any visible functionalities. Provide a clear and concise summary that could be used as a product overview."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            return completion.choices[0].message.content
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise Exception(f"Network error while analyzing image: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")

def generate_sales_pitch(description):
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            messages = [
                {"role": "system", "content": "You are a professional sales expert with deep product knowledge. Your tone is confident, persuasive, and customer-focused while maintaining natural engagement."},
                {"role": "user", "content": f"""Here's a product description:
{description}

Generate a compelling sales pitch targeting potential customers. The tone should be professional yet approachable, emphasizing value propositions and customer benefits. Focus on how this product solves problems or enhances the customer's life. Highlight key features, benefits, and unique selling points in a natural flow. End with a strong, professional call-to-action that creates urgency. Keep the language polished, direct, and impactful while maintaining a customer-centric focus."""}
            ]
            
            response = Together().chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.7,
                stop=["<|eot_id|>", "<|eom_id|>"],
                stream=False
            )
            
            # Handle the response properly
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                raise Exception("No valid response received from the model")
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise Exception(f"Network error while generating sales pitch: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating sales pitch: {str(e)}")

def generate_audio_from_text(text: str, output_path: str = "output.webm"):
    try:
        with ZyphraClient(api_key=zyphra_api_key) as client:
            return sync_speech(
                client,
                text=text,
                speaking_rate=15,
                output_path=output_path
            )
    except Exception as e:
        raise Exception(f"Error in speech generation: {str(e)}")

# Configure Streamlit page
st.set_page_config(
    page_title="Product Image to Sales Pitch Generator",
    page_icon="🎯",
    layout="wide"
)

# Streamlit UI
st.title("Product Image to Sales Pitch Generator")
st.write("Upload a product image and get an AI-generated sales pitch!")

# File uploader with size limit (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

uploaded_file = st.file_uploader(
    "Choose a product image...", 
    type=["jpg", "jpeg", "png"],
    help="Maximum file size: 10MB"
)

if uploaded_file is not None:
    # Validate file size
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("File size too large. Please upload an image smaller than 10MB.")
        st.stop()
    
    try:
        # Try to open and validate the image
        image = Image.open(uploaded_file)
        
        # Display the uploaded image with controlled size
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(image, caption="Uploaded Product Image", width=400)  # Set fixed width
        
        with st.spinner("Analyzing image..."):
            try:
                # Get the image bytes
                img_bytes = uploaded_file.getvalue()
                
                # Get image description
                description = get_image_description(img_bytes)
                
                # Display description
                st.subheader("Product Description")
                st.write(description)
                
                with st.spinner("Generating sales pitch..."):
                    try:
                        # Generate sales pitch
                        sales_pitch = generate_sales_pitch(description)
                        
                        # Display sales pitch
                        st.subheader("Generated Sales Pitch")
                        st.write(sales_pitch)
                        
                        with st.spinner("Converting sales pitch to speech..."):
                            try:
                                output_path = "output.webm"
                                generate_audio_from_text(sales_pitch, output_path)
                                
                                # Display audio player
                                with open(output_path, "rb") as audio_file:
                                    audio_bytes = audio_file.read()
                                    st.audio(audio_bytes, format="audio/webm")
                                    
                            except Exception as e:
                                st.error(f"Failed to generate audio: {str(e)}")
                                
                    except Exception as e:
                        st.error(f"Failed to generate sales pitch: {str(e)}")
                        st.info("Please try again in a few moments.")
                        
            except Exception as e:
                st.error(f"Failed to analyze image: {str(e)}")
                st.info("Please try again with a different image or try again later.")
                
    except Exception as e:
        st.error("Invalid or corrupted image file. Please upload a valid image.")
        st.info("Supported formats: JPG, JPEG, PNG")

# Instructions at the bottom
st.markdown("---")
st.markdown("### How to use:")
st.markdown("1. Upload a product image using the file uploader above (max 10MB)")
st.markdown("2. Wait for the AI to analyze the image and generate a description")
st.markdown("3. Review the generated sales pitch based on the image analysis")

# Error reporting section
st.markdown("---")
st.markdown("### Having issues?")
error_types = {
    "Image upload fails": "Make sure your image is in JPG or PNG format and under 10MB",
    "Analysis takes too long": "The service might be busy. Please try again in a few moments",
    "Generation fails": "Check your internet connection and try again",
}
with st.expander("Troubleshooting Guide"):
    for error, solution in error_types.items():
        st.markdown(f"**{error}**: {solution}")