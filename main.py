import io
import sys
from pydub import AudioSegment
from pydub.playback import play
import pytube

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print("Usage: python main.py [youtube music link]")
    exit(1)

print(f"Getting {url}...")

audio = pytube.YouTube(url)
streams = audio.streams.filter(only_audio=True, file_extension="mp4")
if len(streams) == 0:
    print("No stream found.")
    exit(2)
stream = streams[0]
print(
    f"{audio.title}\nLength: {audio.length // 60}:{audio.length % 60}\nPublished at {audio.publish_date} by {audio.author}"
)

data = ""
with io.BytesIO() as buffer:
    stream.stream_to_buffer(buffer)
    data = buffer.getvalue()

song = AudioSegment.from_file(io.BytesIO(data), format="mp4")
print("Start playing...")
play(song)
print("Song is over.")
