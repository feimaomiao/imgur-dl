import argparse
from time import time

from .source import *

__version__ = '0.1.3'
__author__ = 'Matthew Lam'
__email__ = 'lcpmatthew@gmail.com'
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
    k = vars(parser.parse_args())
    return k


def main():
    start_time = time()
    args = treat_args(get_args())
    treat_argstime = time()
    if args['verbose']:
        printarg(args)
    print_args = time()
    link_generator = link_grabber(args['imgur_link'], args['verbose'])
    generate_link = time()
    file_list = link_generator.return_file_objects()
    get_file_list = time()
    donwloaded_file_list = dl(file_list, args['verbose'], args['output'],
                              args['rename_each'])
    download_time = time()
    if args['format']:
        convert_file(donwloaded_file_list, args['format'], args['verbose'])
    format_time = time()
    if args['stats']:
        print(
            stats(start_time, treat_argstime, print_args, generate_link,
                  get_file_list, download_time, format_time, file_list))
    print('Thank you !')
