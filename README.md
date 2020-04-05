# imgur-downloader
CLI for downloading imgur photos and videos

## To Download
download the binary code from release  
or  
`pip install imgur-dl`

### Usage
`imgur-dl [-s][-v][-o OUTPUT][-e][-f FORMAT][IMGUR LINK]` 


### Arguments
Optional arguments: 

	-s 	--stat						outputs the statistics of the file  
	-v 	--verbose 					outputs more download options
	-o 	--output 		[OUTPUT]	Creates a directory and saves every photo/video into the directory
	-e 	--rename-all				For every image downloaded, open the file and allows you to rename the file
	-f 	--format 		[FORMAT]	Converts all the image files into the givern format

Positional Arguments:  

	IMGUR LINK 						A valid imgur link, could be an image or a gallery

### License
MIT

### Credits
inspired by @alexgisby


###### imgur-dl
###### © 2020 Matthew Lam