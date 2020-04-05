import re

from requests import get as req_get
from tqdm import tqdm as progress_bar

from .download import imgur_object
from .globfuncs import clear_lines


class NetworkError(Exception):
    pass


class link_grabber:
    def __init__(self, link, verbose=False):
        self.files = []
        self._link = link
        self.verbose = verbose
        print('Getting video id') if self.verbose else None
        video_id_search = re.match(
            r"(?:https)?\:\/{2}(?:www/.)?(?:m\.)?imgur\.com/(?:a|gallery)?/([a-zA-Z0-9]+)(?:#[0-9]+)?",
            self._link)
        print('Video id search finished,\nlink: {}'.format(
            video_id_search.group(0))) if self.verbose else None
        try:
            # Get the link to the actual video
            self._albumextension = video_id_search.group(1)
            print('Video id get successful!\nVideo id: {}'.format(
                self._albumextension)) if self.verbose else None
        except AttributeError:
            print(
                'Video id is not in expected imgur format.\nNo file is expected'
            ) if self.verbose else None
            # Raised when the user did not enter an imgur link
            raise ValueError('Please input a proper link!') from AttributeError
        print('Getting blog link from video id {}\nConnecting to website'.
              format('<' + self._albumextension +
                     '>')) if self.verbose else None
        # get the longer link
        self.__actuallink = req_get("http://imgur.com/a/" +
                                    self._albumextension + "/layout/blog")
        print(
            'Connecting to blog link:\nBlog link: {url}\nStatus code: {status}'
            .format(url=self.__actuallink.url,
                    status=self.__actuallink.status_code
                    )) if self.verbose else None
        if self.__actuallink.status_code != 200:
            raise NetworkError(
                'The link is unresponsive, imgur returned status code {}\
\n{}'.format(
                    self.__actuallink.status_code,
                    'Is the photo you are looking for deleted?'
                    if self.__actuallink.status_code == 404 else ''))
        print('Connected to blog...\nLooking for references to images/videos'
              ) if self.verbose else None
        # find hash and extension
        self._reflist = re.findall(
            r'.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?',
            self.__actuallink.text)
        print(
            'Found {length} matched cases, shrinking duplicated lists'.format(
                length=len(self._reflist))) if self.verbose else None
        # Make the list unique
        self._uniqlist = list(set(self._reflist))
        # Set the supposed length for the imgur link
        self._supp_len = len(self._uniqlist)
        print('Getting unique values was successful, {} items in total'.format(
            self._supp_len)) if self.verbose else None

    def __repr__(self):
        return self._link

    @property
    def length(self):
        return self._supp_len

    def generate_download_links(self):
        """
		Function as a generator that yields the proper download links of given videos
		"""
        for items in self._uniqlist:
            yield "http://i.imgur.com/" + items[0] + items[1]

    def return_file_objects(self):
        """
		Function that returnss a list of imgur_object that can be later iterated
		"""
        print('Loading images from {}'.format(self._link))
        for links in progress_bar(self.generate_download_links(),
                                  unit='connections',
                                  total=self._supp_len,
                                  desc='Loading images'):
            try:
                req_obj = imgur_object(link=links, verbose=self.verbose)
                self.files.append(req_obj)
            except NetworkError as ne:
                print('NetworkError is raised in link {}'.format(
                    links)) if self.verbose else None
                print(ne)
            except TypeError as te:
                print(te)
            else:
                pass
        print(
            'Final list length is {length}, expencted length is {explength}.\nSuccessful rate is {percentage}'
            .format(length=len(self.files),
                    explength=self._supp_len,
                    percentage=(str(len(self.files) / self._supp_len * 100)) +
                    '%')) if self.verbose else None
        return self.files
