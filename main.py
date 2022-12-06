import io
import threading
from time import sleep
import sys
import os
from pydub import AudioSegment
from pydub.playback import play
import pytube

N = os.get_terminal_size().columns
RESET = "\033[0m"
PROGRESS_BAR_BG = "\033[44m"
TITLE_FG = "\033[91m"
AUTHOR_FG = "\033[93m"


def time_count(length):
    cur = 0
    while True:
        # progress bar
        sys.stdout.write(
            f"\r{PROGRESS_BAR_BG}[%s]{RESET} %02d:%02d"
            % (
                ("=" * int(cur // (length / (N - 10)) + 1)).ljust(N - 10),
                cur // 60,
                cur % 60,
            )
        )
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
print(f"{TITLE_FG}{audio.title}{RESET}".center(N, " "))
print(("Length: %02d:%02d" % (audio.length // 60, audio.length % 60)).center(N, " "))
print(
    f"Published at {audio.publish_date.strftime('%Y-%m-%d')} by {AUTHOR_FG}{audio.author}{RESET}".center(
        N, " "
    )
)

data = ""
with io.BytesIO() as buffer:
    stream.stream_to_buffer(buffer)
    data = buffer.getvalue()

song = AudioSegment.from_file(io.BytesIO(data), format="mp4")

print("Start playing...")
t = threading.Thread(target=time_count, daemon=True, args=(audio.length,))
t.start()
play(song)
