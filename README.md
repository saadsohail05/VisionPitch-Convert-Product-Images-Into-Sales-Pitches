# VisionPitch Convert Product Images Into Sales Pitches

A AI-powered web application that converts product images into compelling sales pitches with audio narration.

## Features

- Upload product images (JPG, JPEG, PNG formats supported)
- AI-powered image analysis and description generation
- Professional sales pitch generation based on product analysis
- Text-to-speech conversion of sales pitches
- User-friendly web interface

## Technologies Used

- **Frontend**: Streamlit
- **AI Services**:
  - Qwen VL Max for image analysis
  - Llama 3 70B for sales pitch generation
  - Zyphra AI Zonos for text-to-speech conversion

## Prerequisites

- Python 3.x
- Required API keys:
  - OpenRouter API key
  - Together AI API key
  - Zyphra API key

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/saadsohail05/VisionPitch-Convert-Product-Images-Into-Sales-Pitches]
cd Zonos
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key
TOGETHER_API_KEY=your_together_api_key
ZYPHRA_API_KEY=your_zyphra_api_key
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the displayed local URL (typically http://localhost:8501)

3. Upload a product image (max 10MB)

4. Wait for the AI to analyze the image and generate:
   - Product description
   - Sales pitch
   - Audio narration

## Error Handling

The application includes comprehensive error handling for:
- Image upload issues
- API connection problems
- File size limitations
- Invalid file formats

## Limitations

- Maximum file size: 10MB
- Supported image formats: JPG, JPEG, PNG
- Requires active internet connection
- API rate limits may apply

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Acknowledgments

- Qwen VL Max for image analysis capabilities
- Together AI for the Llama 3 language model
- Zyphra AI for text-to-speech conversion
- Streamlit for the web interface framework