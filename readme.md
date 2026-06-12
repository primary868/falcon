# falcon FLAC Converter
Written as an easy interface for ffmpeg, for converting flac into a few formats I commonly use.
("flac converter" -> "flaccon" -> "falcon")

# Usage
```
falcon.py [-h] [--overwrite] infolder out_type

positional arguments:
  infolder          folder of flac files to convert
  out_type          Type of conversion to perform; valid values come from falcon_config.json

options:
  -h, --help        show this help message and exit
  --overwrite, -y   Overwrite existing output files
```

# Defining Conversion Types
Conversion types (arguments for ffmpeg) are defined outside the script. In `./falcon_config.json`, add an entry to the `out_types` dict in this format:
```json
"play":{
  "ext":"mp3",
  "output_format":"-c:a libmp3lame -vn -b:a 128k",
  "cover_func":"cover_playdate", // cover_playdate() exists in falcon to make a discrete album art image in the output.
  "use_album_artist":true // Use source files' 'album artist' tag as infiles' 'artist' tag
}
```
To convert to this format, the command would be: `falcon.py /path/to/input/folder play`

To create a custom cover art image file, add a function to the script which takes `PIL.Image` data as input and saves an image. Two example functions are at the top of the source code: `cover_playdate` and `cover_ipod`.