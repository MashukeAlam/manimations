import asyncio
import edge_tts
from mutagen.mp3 import MP3
import os
import hashlib
import datetime

VOICE = "en-GB-SoniaNeural"
OUTPUT_DIR = "./media/sounds"


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
    communicate = edge_tts.Communicate(text, VOICE)
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

    # Create a unique filename for the audio file
    filename = f"{hashlib.sha256(text.encode('utf-8')).hexdigest()}{datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.mp3"
    output_file = os.path.abspath(os.path.join(OUTPUT_DIR, filename))

    # Generate the voiceover if it doesn't already exist
    if not os.path.exists(output_file):
        print(f"Generating voiceover for: {text}")
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