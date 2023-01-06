import eyed3
import os
from .media_item import MediaItem

class FileFinder:
    def __init__(self, path, allowed_extensions = [ 'mp3' ]) -> None:
        if not os.path.isdir(path):
            print("\nERROR: {} is not a directory.".format(path))
            exit(1)

        self.path = path
        self.allowed_extensions = allowed_extensions
        eyed3.log.setLevel("ERROR")

    def find_media_files(self):
        files = []
        print("Searching for media files...\n")
        for dirname, dirnames, filenames in sorted(os.walk(self.path)):

            if os.path.basename(dirname).startswith('_'):
                continue

            for filename in filenames:
                file = os.path.join(dirname, filename)
                ext = str(os.path.splitext(file)[1]).lower().replace('.', '')
                if ext in self.allowed_extensions:
                    audio_file = eyed3.load(file)
                    files.append(MediaItem(file, audio_file))

        return files
