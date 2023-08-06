# voxscribe
Extract text from .wav and .mp3 files. <br>
Install with:
<pre>pip install voxscribe</pre>
FFmpeg also needs to be installed and in your PATH.<br>
It can be obtained here: https://ffmpeg.org/ <br>
Usage:<br>
<pre>
from voxscribe import get_text_from_url, get_text_from_WAV, get_text_from_MP3
# For web hosted audio (mp3 or wav needs to be specified in the second argument)
text = get_text_from_url("https://github.com/matt-manes/voxscribeTestAudio/blob/main/testaudio.mp3?raw=true", '.mp3')
#For local files
text = get_text_from_MP3('some/filePath/someAudio.mp3')
#or
text = get_text_from_WAV('some/other/filePath/someOtherAudio.wav')
</pre>