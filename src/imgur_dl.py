from time import time

from .source import *

__version__ = '0.1.1'
__author__ = 'Matthew Lam'
__email__ = 'lcpmatthew@gmail.com'


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
    quit()


if __name__ == '__main__':
    main()
