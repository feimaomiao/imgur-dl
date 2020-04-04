import argparse
from sys import stdout as sys_stdout
"""
Functions to treat the arguments and return each values
"""
USAGE = '%(prog)s [-v][-o OUTPUT][-e][-f FORMAT][IMGUR LINK]'


def get_args():
    """
	function that loads the arguments and returns as a dictioary
	"""
    parser = argparse.ArgumentParser(description='Download imgur videos',
                                     prog='imgur-downloader',
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
    k['rename_each'] = bool(k['rename_each'])
    if not k['format']:
        k['format'] = False

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
