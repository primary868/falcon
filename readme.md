"flac converter" -> "flaccon" -> "falcon"
Makes copies of FLAC files in specified file type (ALAC or 320k mp3).

# Usage
`python ./falcon.py [mp3/alac]`

Settings are stored in `./falcon-config.json`:
- `ffmpeg_path`: path to ffmpeg executable
- `in_list`: text file where each line is a path to an album of .flac files to work with.
- `out_folder`: where the files produced by the script are stored.

An example `falcon-config.json` is provided. It must be stored in the same folder as the main `falcon.py` script.