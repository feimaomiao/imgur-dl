import sys
from os import mkdir, path, rename
from re import match as re_match
from time import sleep

from PIL import Image
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
        self.request = req_get(link)
        self.verbose = verbose
        self.success = self.request.status_code == 200
        # When connection returned anything but 200<success>
        if not self.success:
            raise NetworkError(
                'Warning: Fallback on link {}, connection returned status code {}, \
will now skip image'.format(link, self.request.status_code))
        self.extension = link.split('.')[-1]
        if self.extension not in DATATYPES:
            raise TypeError(
                "Unknown/Unavaliable extension {} is given. Please contact https://github.com/feimaomiao/imgur-downloader use the -v flag"
                .format(self.extension))
        self.type = "IMAGE" if self.extension in IMAGETYPES else 'VIDEO'
        self.default_name = re_match(r".+com/([a-zA-Z0-9]+)\.\w+",
                                     link).group(1)

        self.file_path = ''
        self._name = ''

    @property
    def name(self):
        return self._name


def download(imgur_files, verbose, output_file, rename_all):
    def _d(imgur_files, verbose, output_file, rename_all):
        for (count, dlf) in tqdm(enumerate(imgur_files),
                                 total=len(imgur_files),
                                 desc='downloading_files',
                                 unit='files'):

            fp = '{folder}{name}.{extension}'.format(
                folder=folder,
                name=dlf.default_name
                if not output_file else '{}'.format(count),
                extension=dlf.extension)
            with open(fp, 'wb') as outfile:
                for chunk in dlf.request:
                    outfile.write(chunk)
                    sleep(0.00001)
            if verbose:
                sleep(0.03)

            if rename_all:
                Image.open(fp).show()
                final_name = input('What would you like to name this image?')
                rename(
                    fp, '{folder}{name}.{extension}'.format(
                        folder=folder,
                        name=final_name,
                        extension=dlf.extension))
                clear_lines(2) if not verbose else None
                fp = '{folder}{name}.{extension}'.format(
                    folder=folder, name=final_name, extension=dlf.extension)

            dlf.file_path = fp
            dlf._name = '.'.join(fp.split('.')[:-1])
            del fp
            yield dlf

    folder = ''
    if output_file:
        mkdir(output_file) if not path.isdir(output_file) else None
        folder = output_file + '/'
    processed_images = list(_d(imgur_files, verbose, output_file, rename_all))

    return sorted(processed_images,
                  key=lambda x: sum([ord(x) for x in x.name]))
