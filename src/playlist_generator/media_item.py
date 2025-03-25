import re
import time
import os
from dataclasses import dataclass
from eyed3 import core, id3

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
        lists = []

        try:
            for i in self.media.tag.comments:
                lists += i.text.replace('|', ',').replace('/', ',').strip(',').split(',')

            custom_lists = [ item for item in lists if item.lower() not in list(id3.genres.values()) ]
            if len(custom_lists) > 3:
                lists += [ 'stats/im_popular' ]

            lists += re.findall('\\((cover|live|unplugged|acoustic|remix|instrumental|classic)', self.title().lower())
            if len(lists) == 0:
                lists += [ 'stats/forever_alone' ]

            if time.time() - os.path.getmtime(self.path) < (3 * 30 * 24 * 60 * 60) :
                lists += [ 'stats/recently_modified' ]

            if self.year() > 1900:
                median = round(self.year(), -1)
                lists += [ 'stats/years-{}-{}'.format((int(median) - 5), (int(median) + 4)) ]

            lists += [ self.genre() ]
        except:
            lists += [ 'stats/unknown_errors' ]

        lists += [ 'stats/all' ]
        return set([x for x in lists if x != None])
