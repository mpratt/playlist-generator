import os
from alive_progress import alive_it
from argparse import ArgumentParser
from .listwriter import ListWriter
from .filefinder import FileFinder

def main():
    parser = ArgumentParser(description = __name__)
    parser.add_argument(
        'path',
        help = 'The path where the mp3s are stored'
    )

    parser.add_argument(
        'output_dir',
        help = 'The path where the playlists are going to be generated'
    )

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    output_dir = os.path.abspath(args.output_dir)

    if None in (path, output_dir):
        parser.print_help()
        print("\nERROR: Missing arguments.")
        exit(1)

    if not os.path.isdir(path):
        parser.print_help()
        print("\nERROR: {} is not a credentials file.".format(path))
        exit(1)

    writer = ListWriter(output_dir)
    items = FileFinder(path).find_media_files()
    for item in alive_it(items):
        writer.write_detected_lists(item)

if __name__ == "__main__":
    main()
