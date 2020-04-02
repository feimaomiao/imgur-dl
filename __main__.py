import argparse
from imgur import funcs
from time import time as time
from os import path

parser = argparse.ArgumentParser(description='Download imgur videos',prog='imgur-downloader')
parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-o','--output', action='store')
parser.add_argument('-n','--name',dest='rename_all', action='store_true')
print(parser.parse_args())
