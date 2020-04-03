from re import match as re_match
from sys import stdout

from requests import get as req_get

from .globfuncs import clear_lines

DATATYPES = ["jpeg","jpg","png","gif","apng","tiff","mp4","mpeg","avi","webm","quicktime","x-matroska","x-flv","x-msvideo", "x-ms-wmv"]

IMAGETYPES =["jpeg","jpg","png","gif","apng","tiff"]

VIDEOTYPES = [i for i in DATATYPES if i not in IMAGETYPES]


class imgur_object:
	def __init__(self,link, verbose):
		stdout.flush()

		self.request = req_get(link)
		self.verbose = verbose

		print('Requesting {link}'.format(link=link)) if self.verbose else None

		self.success = self.request.status_code == 200
		
		# When connection returned anything but 200<success>
		if not self.success:
			raise NetworkError('Warning: Fallback on link {}, connection returned status code {}, \
will now skip image'.format(link, self.request.status_code))

		print('Success!\nGetting extension ') if self.verbose else None

		self.extension = link.split('.')[-1]

		print('Extension {} found!'.format(self.extension)) if self.verbose else None

		if self.extension not in DATATYPES:
			raise TypeError("Unknown/Unavaliable extension {} is given. Please contact https://github.com/feimaomiao/imgur-downloader use the -v flag".format(self.extension))

		self.type = "IMAGE" if self.extension in IMAGETYPES else 'VIDEO'
		print('Media type : {}'.format(self.type.lower())) if self.verbose else None

		self.default_name = re_match(r".+com/([a-zA-Z0-9]+)\.\w+", link).group(1)
		print('Default name {} found'.format(self.default_name)) if self.verbose else None

		clear_lines(7 if self.verbose else 0)
