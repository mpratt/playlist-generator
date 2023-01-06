import os
from setuptools import setup, find_packages

DEPENDENCIES = ( 'eyed3', 'alive_progress' )

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'playlist_generator',
    version = '0.1.0',
    author = "Michael Pratt",
    author_email = "author@michaelpratt.dev",
    description = ( "Create M3U playlists for mp3 files using their ID3 information." ),
    license = "MIT",
    keywords = "",
    include_package_data=True,
    url = "",
    packages = find_packages(),
    package_dir = { '' : 'src' },
    long_description = read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=DEPENDENCIES,
    entry_points = {
        'console_scripts': [ 'playlist-generator = playlist_generator.cli:main' ],
    },
)
