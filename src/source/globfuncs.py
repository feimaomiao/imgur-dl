from os import get_terminal_size as gts
from os import path, remove
from sys import stdout as sys_stdout
from time import sleep

from lzl import lzfloat, lzlist
from PIL import Image
from tqdm import tqdm


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
