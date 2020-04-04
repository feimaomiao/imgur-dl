import sys
from os import mkdir, path
from re import match as re_match
from time import sleep

from requests import get as req_get
from tqdm import tqdm

from .globfuncs import clear_lines

DATATYPES = [
    "jpeg", "jpg", "png", "gif", "apng", "tiff", "mp4", "mpeg", "avi", "webm",
    "quicktime", "x-matroska", "x-flv", "x-msvideo", "x-ms-wmv"
]
IMAGETYPES = ["jpeg", "jpg", "png", "gif", "apng", "tiff"]
VIDEOTYPES = [i for i in DATATYPES if i not in IMAGETYPES]


class imgur_object:
    def __init__(self, link, verbose):
        sys.stdout.flush()
        self.request = req_get(link)
        self.verbose = verbose
        print('Requesting {link}'.format(link=link)) if self.verbose else None
        self.success = self.request.status_code == 200
        # When connection returned anything but 200<success>
        if not self.success:
            raise NetworkError(
                'Warning: Fallback on link {}, connection returned status code {}, \
will now skip image'.format(link, self.request.status_code))
        print('Success!\nGetting extension ') if self.verbose else None
        self.extension = link.split('.')[-1]
        print('Extension {} found!'.format(
            self.extension)) if self.verbose else None
        if self.extension not in DATATYPES:
            raise TypeError(
                "Unknown/Unavaliable extension {} is given. Please contact https://github.com/feimaomiao/imgur-downloader use the -v flag"
                .format(self.extension))
        self.type = "IMAGE" if self.extension in IMAGETYPES else 'VIDEO'
        print('Media type : {}'.format(
            self.type.lower())) if self.verbose else None
        self.default_name = re_match(r".+com/([a-zA-Z0-9]+)\.\w+",
                                     link).group(1)
        print('Default name {} found'.format(
            self.default_name)) if self.verbose else None
        clear_lines(7 if self.verbose else 0)


def download(imgur_files, verbose, output_file, rename_all, format):
    processed_images = []
    folder = ''
    if output_file:
        mkdir(output_file) if not path.isdir(output_file) else None
        folder = output_file + '/'
    for (count, i) in tqdm(enumerate(imgur_files),
                           total=len(imgur_files),
                           desc='downloading_files',
                           unit='files'):
        """
        Singlle image download mode
        """
        # sleep(0.5)
        # sys.stdout.flush()
        if not rename_all:
            fp = '{folder}{name}.{extension}'.format(
                folder=folder,
                name=i.default_name if not output_file else output_file +
                '_{}'.format(count),
                extension=i.extension)
            print('Directly downloading image{filename}\nDestination: {dest}'.
                  format(dest=fp,
                         filename=i.default_name)) if verbose else None
            with open(fp, 'wb') as outfile:
                for chunk in i.request:
                    outfile.write(chunk)
                    sleep(0.00001)
            if verbose:
                sleep(0.03)
        else:
            pass
