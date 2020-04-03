from source import *

# OSError
# image.convert('RGB').save()

def main():
	args = treat_args(get_args())
	if args['verbose']:
		printarg(args)
	link_generator = link_grabber(args['imgur_link'], args['verbose'])
	link_generator.return_file_objects()

if __name__ == '__main__':
	main()
