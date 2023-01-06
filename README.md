# Playlist Generator
Python script used create M3U playlists for mp3 files
using their ID3 information.

It takes into account the genre, release date and the comments.
Comments can have list names separated by `|` for example:

`disco|my mix`

# Installation
Download the source code, extract the data, go to the folder and run

`pip install -e .`

# Usage
```
playlist-generator  path_with_mp3s output_dir_of_playlist
```

**Warning:** This scripts deletes any .m3u found inside
the output_dir_of_playlist before creating the lists.
