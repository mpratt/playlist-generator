import os
import re
import unicodedata

from .media_item import MediaItem

class ListWriter:
    def __init__(self, output_dir) -> None:
        self.output_dir = output_dir.rstrip('/')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            os.makedirs('{}/stats'.format(self.output_dir))

        self.clean_dir(self.output_dir)
        self.clean_dir('{}/stats'.format(self.output_dir))

    def clean_list_name(self, text):
        if not text or len(text) <= 2 or len(text) > 30:
            return None

        text = text.lower().strip()

        " Ignore urls, strange checksums, 'ripped by' tags and useless junk "
        regexes = [
            '^https?://\\S+', '^album title', '^artist album', '^direct', '^http-?', '^waxdotcom'
            '^goo goo dolls cover', '^good', '^bitches', '^one group to rule them all', '^tranquil',
            '^ac_ripper', '^ripp', '^created by', '^Florilegium Musicorum Aetati', '^eeuu', '^m3u', 'djbooth',
            'cxmxix', 'to\xf1o valverde', '^feat', '\xa9 \xa4 @', 'Luisitou', 'encoded',
            '\\.com$', '^www', '^[0-9a-z]{7,8}[ -][0-9a-z]{7,8}[ -][0-9a-z]{7,8}', '[0-9a-z]{7,8}[ -][0-9a-z]{7,8}[ -][0-9a-z]{7,8}',
            '^[0-9a-z]{6,8} [0-9a-z]{6,7} [0-9a-z]{2}', '^[0-9]{2}-[0-9a-z]+ ?-[0-9]+',
        ]

        r = '(' + ')|('.join(regexes) + ')'
        regex = re.compile(r, re.IGNORECASE)
        if re.match(regex, text):
            print('*** Ignoring comment {}'.format(text))
            return None

        for char in ['(', ')', '\'', '"', '[', ']']:
            text = text.replace(char, '')

        for char in [' ', '..', ',', '!', '%', '#', '$', '@', '*', '/', '\\', '+', ':']:
            text = text.replace(char, '-')

        table = {
            'stats-': 'stats/',
            'soundtracks': 'soundtrack',
            'sountrack': 'soundtrack',
            'acoustic': 'unplugged',
            'cover': 'covers',
            'aletrnative': 'alternative',
            'programing': 'programming',
            'let-go': 'lets-go',
            'reaggeton': 'reggaeton',
            '+': ' ',
        }

        for key in table.keys():
            text = text.replace(key, table[key])

        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    def clean_dir(self, directory) -> None:
        for f in [f for f in os.listdir(directory) if f.endswith('.m3u')]:
            os.remove(os.path.join(directory, f))

    def write_list(self, list, file_path, time, artist, title):
        exists = os.path.isfile(list)
        playlist = open(list, 'a')
        if not exists:
            playlist.write("#EXTM3U\n")

        playlist.write(u"#EXTINF: {}, {} - {} \n".format(time, artist, title))
        playlist.write(file_path + "\n")
        playlist.close()

    def write_detected_lists(self, file:MediaItem):
        lists = file.playlists()
        for list in lists:
            list = self.clean_list_name(list)
            if list:
                list = os.path.join(self.output_dir, '{}.m3u'.format(list.replace('0S.', '0s.')))
                self.write_list(list, file.path, file.time(), file.artist(), file.title())
