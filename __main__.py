from source import *


# OSError
# image.convert('RGB').save()
def main():
    args = treat_args(get_args())
    if args['verbose']:
        printarg(args)
    link_generator = link_grabber(args['imgur_link'], args['verbose'])
    file_list = link_generator.return_file_objects()
    dl(file_list, args['verbose'], args['output'], args['rename_each'])


if __name__ == '__main__':
    main()
