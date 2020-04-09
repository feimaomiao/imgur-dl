import setuptools
import re

with open('src/imgur_dl.py') as fh:
    _f = fh.read()

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', _f,
                    re.MULTILINE).group(1)
author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', _f,
                   re.MULTILINE).group(1)
email = re.search(r'^__email__\s*=\s*[\'"]([^\'"]*)[\'"]', _f,
                  re.MULTILINE).group(1)

with open('README.md', 'r') as fh:
    actual_description = fh.read()

setuptools.setup(
    name="imgur-dl",
    version=version,
    author=author,
    author_email=email,
    description="Imgur downloader",
    long_description=actual_description,
    packages=['src','src/source'],
    long_description_content_type="text/markdown",
    install_requires = ['lazyloads','tqdm','requests','pillow'],
    url="https://github.com/feimaomiao/imgur-dl",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent", "Topic :: Internet"
    ],
    keywords='imgur photo video download',
    zip_safe=False,
    python_requires='>=3.6',
    entry_points={'console_scripts': [
        'imgur-dl=src.imgur_dl:main',
    ]})
