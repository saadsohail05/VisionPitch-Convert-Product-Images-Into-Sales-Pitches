import os
import asyncio
import argparse
from typing import Optional
from dotenv import load_dotenv
from zyphra import ZyphraClient, AsyncZyphraClient

def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Text-to-speech converter using Zyphra API')
    parser.add_argument('--text', type=str, help='Text to convert to speech', default="Hello, world!")
    parser.add_argument('--output', type=str, help='Output file path', default="output.webm")
    parser.add_argument('--speaking-rate', type=int, help='Speaking rate (1-20)', default=15)
    return parser

async def async_speech(client: AsyncZyphraClient, text: str, speaking_rate: int) -> bytes:
    try:
        audio_data = await client.audio.speech.create(
            text=text,
            speaking_rate=speaking_rate
        )
        return audio_data
    except Exception as e:
        raise Exception(f"Error in async speech generation: {str(e)}")

def sync_speech(client: ZyphraClient, text: str, speaking_rate: int, output_path: Optional[str] = None) -> Optional[bytes]:
    try:
        if output_path:
            return client.audio.speech.create(
                text=text,
                speaking_rate=speaking_rate,
                output_path=output_path
            )
        else:
            return client.audio.speech.create(
                text=text,
                speaking_rate=speaking_rate
            )
    except Exception as e:
        raise Exception(f"Error in sync speech generation: {str(e)}")

async def main():
    # Load environment variables
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv('ZYPHRA_API_KEY')
    if not api_key:
        raise ValueError("ZYPHRA_API_KEY not found in environment variables")

    # Parse command line arguments
    parser = setup_argparser()
    args = parser.parse_args()

    # Validate speaking rate
    if not 1 <= args.speaking_rate <= 20:
        raise ValueError("Speaking rate must be between 1 and 20")

    try:
        # Synchronous example
        with ZyphraClient(api_key=api_key) as client:
            print(f"Generating speech for text: {args.text}")
            output_path = sync_speech(
                client,
                text=args.text,
                speaking_rate=args.speaking_rate,
                output_path=args.output
            )
            print(f"Speech saved to: {output_path}")

        # Asynchronous example
        async with AsyncZyphraClient(api_key=api_key) as client:
            print("Generating speech asynchronously...")
            audio_data = await async_speech(
                client,
                text=args.text,
                speaking_rate=args.speaking_rate
            )
            print(f"Received {len(audio_data)} bytes of audio data")

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)