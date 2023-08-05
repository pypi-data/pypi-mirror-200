from .voxscribe import (clean_up, get_text_from_MP3, get_text_from_url,
                        get_text_from_WAV)

""" FFMPEG needs to be installed and in your PATH for this module to work. """
clean_up(max_age=5)
