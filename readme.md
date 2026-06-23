# falcon FLAC Converter
Written as an easy interface for ffmpeg, for converting flac into a few formats I commonly use.
("flac converter" -> "flaccon" -> "falcon")

# Usage
```
usage: falcon.py [-h] [--overwrite] [--show_command] [--outfolder OUTFOLDER] infolder {...}

positional arguments:
  infolder              folder of flac files to convert
  {...}
                        Type of conversion to perform

options:
  -h, --help            show this help message and exit
  --overwrite, -y       Overwrite existing output files
  --show_command, -s    Show generated ffmpeg commands
  --outfolder, -o OUTFOLDER
                        Folder to place converted files. Makes it if it does not exist.
```

# Defining Conversion Types
Conversion types (arguments for ffmpeg) are defined outside the script. In `./falcon_config.json`, add an entry to the `out_types` dict in this format:
```json
"play":{
  "ext":"mp3",
  "output_format":"-c:a libmp3lame -vn -b:a 128k",
  "cover_func":"cover_playdate",
  "use_album_artist":true
}
```
- `cover_func`: Name of function **within falcon script** to make a discrete album art image in the output. The function should take `PIL.Image` image dta object as a function and handle saving the output image file. (Follow example functions at the top o the script)
- `use_album_artist`: Use source files' 'album artist' tag as infiles' 'artist' tag

To use this example conversion type, the command would be: `falcon.py /path/to/input/folder play`