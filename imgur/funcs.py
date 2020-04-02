import re
from requests import get as req_get
from lzl import lzlist

# Photo link
# IMGURLINK = 'https://imgur.com/gallery/oOitM6T'
# Video link
# IMGURLINK = "https://imgur.com/gallery/yUWbS"
# Gallery link
IMGURLINK= 'https://imgur.com/gallery/7T1ebb7'
# Error case
# IMGURLINK = "https://imgur.com/a/as12asd"
# Deleted link
# IMGURLINK = "https://m.imgur.com/a/JI1Ia3X"

class NetworkError(Exception):
	pass

class link_grabber:
	
	def __init__(self, link, verbose=False):
		self._link = link

		print('Getting video id') if verbose else None

		video_id_search = re.match(r"(?:https)?\:\/{2}(?:www/.)?(?:m\.)?imgur\.com/(?:a|gallery)?/([a-zA-Z0-9]+)(?:#[0-9]+)?", self._link)	

		print('Video id search finished,\nlink: {}'.format(video_id_search.group(0))) if verbose else None

		try:

			# Get the link to the actual video
			self._linkextension = video_id_search.group(1)
		
			print('Video id get successful!\nVideo id: {}'.format(self._linkextension)) if verbose else None

		except AttributeError:

			print('Video id is not in expected imgur format.\nNo file is expected') if verbose else None
			# Raised when the user did not enter an imgur link
			raise ValueError('Please input a proper link!')

		print('Getting blog link from video id {{}}\nConnecting to website'.format(self._linkextension)) if verbose else None

		# get the longer link
		self.__actuallink = req_get("http://imgur.com/a/" + self._linkextension + "/layout/blog")

		print('Connecting to blog link:\nBlog link: {url}\nStatus code: {status}'.format(url=self.__actuallink.url,status=self.__actuallink.status_code)) if verbose else None

		if self.__actuallink.status_code != 200:
			raise NetworkError('The link is unresponsive, imgur returned status code {}\
\n{}'.format(self.__actuallink.status_code,'Is the photo you are looking for deleted?' 
if self.__actuallink.status_code==404 else '' ))

		print('Connected to blog...\nLooking for references to images/videos') if verbose else None

		# find hash and extension
		self._reflist = re.findall(r'.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', self.__actuallink.text)

		print('Found {length} matched cases, shrinking duplicated lists'.format(length=len(self._reflist))) if verbose else None

		# Make the list unique
		self._uniqlist = lzlist(self._reflist).unique

		# Set the supposed length for the imgur link
		self._supp_len = len(self._uniqlist)

		print('Getting unique values was successful, {} items in total'.format(self._supp_len)) if verbose else None

	def generate_download_links(self):
		"""
		Function as a generator that yields the proper download links of given videos
		"""
		for items in self._uniqlist:
			yield "http://i.imgur.com/"+ items[0] + items[1]

link_grabber(IMGURLINK,True)