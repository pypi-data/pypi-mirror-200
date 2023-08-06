import base64
import os
from datetime import datetime
from pathlib import Path

import requests
import speech_recognition
from pydub import AudioSegment

from whosyouragent import get_agent

root = Path(__file__).parent

""" Extract text from an mp3 or wav file. """


def download_audio_file(url: str, file_ext: str) -> Path:
    """Downloads an audio file to
    a folder named audio in
    the same folder as this file.

    :param file_ext: Can be either '.mp3' or '.wav'.

    Returns a Path object for the saved file."""
    dest = root / "audio"
    dest.mkdir(parents=True, exist_ok=True)
    filepath = (dest / str(datetime.now().timestamp())).with_suffix(file_ext)
    source = requests.get(url, headers={"User-Agent": get_agent()})
    print(f"{source.status_code=}")
    with filepath.open("wb") as file:
        file.write(source.content)
    return filepath


def base64_to_audiofile(src: str, file_ext: str) -> Path:
    """Convert and save base64 string to an audio file.

    :param src: The base64 encoded string.

    :param file_ext: Can be either '.mp3' or '.wav'.

    Returns a Path object for the saved file."""
    dest = root / "audio"
    dest.mkdir(parents=True, exist_ok=True)
    filepath = (dest / str(datetime.now().timestamp())).with_suffix(file_ext)
    filepath.write_bytes(base64.b64decode(src))
    return filepath


def convert_MP3_to_WAV(MP3path: Path | str) -> Path:
    """Converts an mp3 file to a wav file
    of the same name and returns a Path object
    for the wav file."""
    MP3path = Path(MP3path)
    audio = AudioSegment.from_mp3(MP3path)
    WAVpath = MP3path.with_suffix(".wav")
    audio.export(WAVpath, format="wav")
    return WAVpath


def get_text_from_url(url: str, file_ext: str) -> str:
    """Returns text from an mp3 file
    located at the given url.

    :param file_ext: Can be either '.mp3' or '.wav'"""
    audiopath = download_audio_file(url, file_ext)
    if file_ext == ".mp3":
        return get_text_from_WAV(convert_MP3_to_WAV(audiopath))
    elif file_ext == ".wav":
        return get_text_from_WAV(audiopath)
    else:
        raise Exception('file_ext param must be ".mp3" or ".wav"')


def get_text_from_WAV(WAVpath: Path | str) -> str:
    """Returns text from a wav file
    located at the give file path."""
    WAVpath = Path(WAVpath)
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(str(WAVpath)) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
    return text


def get_text_from_MP3(MP3path: Path | str) -> str:
    """Returns text from an mp3 file
    located at the give file path."""
    return get_text_from_WAV(convert_MP3_to_WAV(MP3path))


def get_text_from_base64(src: str, file_ext: str) -> str:
    """Returns text from a base64 encoded audio string.

    :param src: The base64 encoded auio.

    :param file_ext: Can me '.mp3' or '.wav'."""
    filepath = base64_to_audiofile(src, file_ext)
    match file_ext:
        case ".wav":
            return get_text_from_WAV(filepath)
        case ".mp3":
            return get_text_from_MP3(filepath)


def clean_up(max_age: int):
    """Removes any files from the audio directory
    older than max_age minutes."""
    audiopath = root / "audio"
    if audiopath.exists():
        for file in audiopath.glob("*.*"):
            if (datetime.now().timestamp() - os.stat(file).st_ctime) > (60 * max_age):
                file.unlink()
