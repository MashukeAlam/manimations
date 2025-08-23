import asyncio
import edge_tts
from mutagen.mp3 import MP3
import os
import hashlib
import datetime

# Default voice
DEFAULT_VOICE = "en-GB-SoniaNeural"
OUTPUT_DIR = "./media/sounds"


def get_voice():
    """Get the voice setting from .voice file or return default"""
    try:
        if os.path.exists('.voice'):
            with open('.voice', 'r') as f:
                voice = f.read().strip()
                if voice:  # Make sure it's not empty
                    return voice
    except Exception:
        pass  # Fall back to default if any error occurs

    return DEFAULT_VOICE


# Set VOICE dynamically
VOICE = get_voice()


def get_audio_duration(file_path: str) -> float:
    """Get the duration of an audio file."""
    try:
        audio = MP3(file_path)
        return audio.info.length
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0


async def _generate_voiceover(text: str, output_file: str) -> None:
    """Generate voiceover from text and save it to a file."""
    # Get the current voice setting each time
    current_voice = get_voice()
    communicate = edge_tts.Communicate(text, current_voice)
    await communicate.save(output_file)


def generate_voice_and_get_duration(text: str) -> tuple[str | None, float]:
    """
    Generates a voiceover for the given text, saves it as an MP3 file,
    and returns the file path and duration.
    """
    if not text:
        return None, 0

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Include voice in filename hash to avoid conflicts when voice changes
    current_voice = get_voice()
    text_with_voice = f"{text}_{current_voice}"
    filename = f"{hashlib.sha256(text_with_voice.encode('utf-8')).hexdigest()}{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.mp3"
    output_file = os.path.abspath(os.path.join(OUTPUT_DIR, filename))

    # Generate the voiceover if it doesn't already exist
    if not os.path.exists(output_file):
        print(f"Generating voiceover for: {text} (Voice: {current_voice})")
        try:
            asyncio.run(_generate_voiceover(text, output_file))
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None, 0
    else:
        print(f"Voiceover already exists for: {text}")

    # Get the duration of the audio file
    duration = get_audio_duration(output_file)
    return output_file, duration


if __name__ == "__main__":
    # Example usage
    text_to_speak = "Hello, this is a test of the voice generation system."
    audio_file, audio_duration = generate_voice_and_get_duration(text_to_speak)
    if audio_file:
        print(f"Audio file saved at: {audio_file}")
        print(f"Audio duration: {audio_duration} seconds")
        print(f"Using voice: {get_voice()}")