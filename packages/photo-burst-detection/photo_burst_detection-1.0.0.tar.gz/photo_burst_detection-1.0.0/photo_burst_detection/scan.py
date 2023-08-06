import glob
import os
import re
from datetime import datetime, timedelta


class Scanner:
    directories = []

    def __init__(self, path, logger):
        self.path = path.rstrip('/').rstrip('\\')
        self.logger = logger
        self.load_directories()

    def get_link(self, path):
        return path.replace(self.path, '').replace('\\', '/')

    def get_fullpath(self, *paths):
        paths = [os.path.normpath(p).lstrip(os.sep) for p in paths]
        return os.path.join(self.path, *paths)

    def load_directories(self):
        self.directories = []
        for root, dirs, files in os.walk(self.path):
            if root != self.path and not root.lower().endswith('video') and len(files) > 0:
                self.directories.append({'name': os.path.basename(root),
                                         'link': self.get_link(root),
                                         'size': len(files),
                                         'bursts': len(self.get_bursts(self.get_link(root))),
                                         })
        self.directories = sorted(self.directories, key=lambda d: d['link'])

    def refresh(self):
        self.load_directories()

    def delete_photo(self, path):
        fullpath = self.get_fullpath(path)
        if os.path.isfile(fullpath):
            os.remove(fullpath)
        else:
            raise Exception(str(path) + ' not found or not a file')

    def get_directories(self, f=None):
        return self.directories if f is None else [d for d in self.directories if f in d]

    def get_namings(self):
        results = []
        for root, dirs, files in os.walk(self.path):
            if root != self.path and not root.lower().endswith('video') and len(files) > 0:
                results.append({'directory': self.get_link(root),
                                'prefix': {extract_prefix(f) for f in files if not f.startswith('.')},
                                'extension': {os.path.splitext(f)[1] for f in files if not f.startswith('.')},
                                })
        return results

    def get_bursts(self, path, seconds=2):
        prev_date = datetime(1970, 1, 1)
        prev_file = None

        pathname = self.get_fullpath(path, '*.jpg')
        self.logger.info(f'Scanner:get_bursts from {pathname}')
        results = [[]]
        files = sorted([[f, extract_date(f)] for f in glob.glob(pathname, recursive=True)], key=lambda x: str(x[1]))
        for [file, date] in files:
            if date is None:
                print('WARN ' + file)
                continue
            if date - prev_date < timedelta(seconds=seconds):
                results[-1].append(prev_file)
                results[-1].append(file)
            elif len(results[-1]) > 0:
                results.append([])
            prev_date = date
            prev_file = file

        if len(results[-1]) == 0:
            del results[-1]

        results = sorted(results, key=len, reverse=True)

        return [{
            'id': i + 1,
            'files': [{
                'name': os.path.basename(f),
                'link': '/photo' + self.get_link(f),
                'datetime_fmt': extract_date(f).strftime('%d/%m/%Y %H:%M:%S'),
                'datetime': extract_date(f).strftime('%d/%m/%Y %H:%M:%S.%f'),
            } for f in sorted(set(files))],
            'size': len(set(files))} for i, files in enumerate(results)]


def extract_date(s):
    match = re.search(r'_(\d{8}_\d{6,8})', s)
    if not match:
        return None
    sdate = match.group(1)
    return datetime.strptime(sdate, '%Y%m%d_%H%M%S%f')


def extract_prefix(s):
    match = os.path.basename(s).split('_')
    if len(match) == 0:
        return None
    return match[0]
