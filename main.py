import io
import threading
from time import sleep
import sys
from pydub import AudioSegment
from pydub.playback import play
import pytube


def time_count():
    cur = 0
    while True:
        sys.stdout.write("\r%02d:%02d" % (cur // 60, cur % 60))
        sys.stdout.flush()
        cur += 1
        sleep(1)


if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} [youtube music link]")
    exit(1)

print(f"Getting {url}...")

audio = pytube.YouTube(url)
streams = audio.streams.filter(only_audio=True, file_extension="mp4")
if len(streams) == 0:
    print("No stream found.")
    exit(2)
stream = streams[0]

# print song info
print()
print(audio.title)
print("Length: %02d:%02d" % (audio.length // 60, audio.length % 60))
print(f"Published at {audio.publish_date.strftime('%Y-%M-%d')} by {audio.author}")

data = ""
with io.BytesIO() as buffer:
    stream.stream_to_buffer(buffer)
    data = buffer.getvalue()

song = AudioSegment.from_file(io.BytesIO(data), format="mp4")

print("Start playing...")
t = threading.Thread(target=time_count, daemon=True)
t.start()
play(song)
