import re
import time
import os
from dataclasses import dataclass
from eyed3 import core

@dataclass
class MediaItem:
    path: str
    media: core.AudioFile

    def time(self) -> str:
        return self.media.info.time_secs

    def artist(self) -> str:
        return self.media.tag.artist

    def title(self) -> str:
        return self.media.tag.title

    def album(self) -> str|None:
        try:
            return self.media.tag.album
        except:
            return None

    def genre(self) -> str|None:
        try:
            return self.media.tag._getGenre().name
        except:
            return None

    def year(self):
        try:
            return self.media.tag.getBestDate().year
        except:
            return 0

    def playlists(self) -> set:
        lists = [ 'stats/all' ]

        try:
            lists += [ self.genre() ]
            lists += re.findall('\\((cover|live|unplugged|acoustic|remix|instrumental)', self.title().lower())

            for i in self.media.tag.comments:
                lists += i.text.replace('|', ',').replace('/', ',').strip('|').split(',')

            if len(lists) == 2:
                lists += [ 'stats/forever_alone' ]

            if time.time() - os.path.getmtime(self.path) < (3 * 30 * 24 * 60 * 60) :
                lists += [ 'stats/recently_modified' ]

            if self.year() > 1900:
                median = round(self.year(), -1)
                lists += [ 'stats/years-{}-{}'.format((int(median) - 5), (int(median) + 4)) ]
        except:
            lists += [ 'stats/unknown_errors' ]

        return set([x for x in lists if x != None])
