import argparse
from os import path, remove, get_terminal_size as gts
from sys import stdout as sys_stdout
from time import sleep

from lzl import lzfloat, lzlist
from PIL import Image
from tqdm import tqdm
"""
Functions to treat the arguments and return each values
"""
USAGE = '%(prog)s [-s][-v][-o OUTPUT][-e][-f FORMAT][IMGUR LINK]'


def get_args():
    """
	function that loads the arguments and returns as a dictioary
	"""
    parser = argparse.ArgumentParser(description='Download imgur videos',
                                     prog='imgur-dl',
                                     usage=USAGE)
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='print more descriptions')
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        help=
        'File name.\nOutput to file name or directory name depending on the amount of files being downloaded.'
    )
    parser.add_argument('-e',
                        '--rename',
                        dest='rename_each',
                        action='store_true',
                        help='Displays each file and lets you choose the name')
    parser.add_argument(
        '-f',
        '--format',
        dest='format',
        action='store',
        help=
        'Converts all similar types of objects to one type of file. Only supports image files'
    )
    parser.add_argument('-s',
                        '--stats',
                        dest='stats',
                        action='store_true',
                        help='Prints time taken for each function')
    parser.add_argument(dest='imgur_link',
                        action='store',
                        help='The link provided by you')
    return vars(parser.parse_args())


def treat_args(a):
    """
	Fix the None types and returns a filled dict.
	"""
    k = a.copy()
    k['verbose'] = bool(k['verbose'])
    if not bool(k['output']):
        """
		Fllagging the attribute to False and makes the next step easier
		"""
        k['output'] = False
    else:
        """
        allowing UNIX-like file paths
        """
        k['output'] = path.expanduser(k['output'])
    k['rename_each'] = bool(k['rename_each'])
    if not k['format']:
        k['format'] = False
    k['stats'] = bool(k['stats'])

    return k


def printarg(d):
    """
	Prints all the arguments from given arguments
	"""
    print(
        'Verbose switch is set to on. All functions would be printed\nArgs:\n')
    print('-' * 25)
    for i in d.items():
        print('{:12}|{}'.format(i[0], i[1]))
    print('-' * 25)
    return


"""
Other functions
"""


def clear_lines(lines=0):
    for i in range(lines):
        # move up one line and clear whole line
        sys_stdout.write("\033[F")
        sys_stdout.write("\033[K")
    sys_stdout.flush()
    return


"""
COnvert donwloaded images
"""


def convert_file(files_list, fat, verbose):
    print('Converting files to {}'.format(fat))
    for downloaded_files in tqdm(files_list,
                                 total=len(files_list),
                                 desc='converting images',
                                 unit='files'):
        if downloaded_files.type == 'VIDEO':
            continue
        imgfile = Image.open(downloaded_files.file_path)
        print('Converting {} to {}'.format(
            downloaded_files.file_path, downloaded_files.name +
            '.{}'.format(fat))) if verbose else None
        sleep(0.01)
        try:
            sys_stdout.flush()
            imgfile.save(downloaded_files.name + '.{}'.format(fat), fat)
            remove(downloaded_files.file_path)
        except KeyError:
            print('Unknown file type: {}'.format(fat))
        except OSError:
            imgfile.convert('RGB').save(
                downloaded_files.name + '.{}'.format(fat), fat)
            remove(downloaded_files.file_path)
        finally:
            sleep(0.001)
    return


# get_stats = stats(start_time, treat_args, print_args, generate_link, get_file_list, download_time, format_time)
def stats(*args):
    a = list(args)
    dist = gts().columns // 2 - 1
    file_types = str(lzlist(['.' + x.extension for x in a[7]]).unique)
    STATSPAGE = f'''\
Time Taken:
|{'-'*(gts().columns- 2)}|
|{'Treating args':^{dist}}|{lzfloat(a[1]-a[0]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|
|{'Printing args':^{dist}}|{lzfloat(a[2]-a[1]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|
|{'Generating links':^{dist}}|{lzfloat(a[3]-a[2]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|
|{'Getting file lists':^{dist}}|{lzfloat(a[4]-a[3]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|
|{'Downloading image':^{dist}}|{lzfloat(a[5]-a[4]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|
|{'Converting files':^{dist}}|{lzfloat(a[6]-a[5]).round_sf(8):^{dist}}|
|{'-'*(gts().columns- 2)}|

Files:
|{'-'*(gts().columns- 2)}|
|{'Amount of files':^{dist}}|{len(a[7]):^{dist-1}}|
|{'-'*(gts().columns- 2)}|
|{'File types':^{dist}}|{file_types:^{dist-1}}|
|{'-'*(gts().columns- 2)}|
'''
    return STATSPAGE
