import subprocess, argparse, glob, os, sys, json

# constants
COMMANDS = {
    'alac':["-c:a", "alac", "-c:v", "copy"],
    'mp3':['-ab', '320k', '-c:v', 'copy']
}
EXTENSIONS = {
    'alac':'m4a',
    'mp3':'mp3'
}

# note: this script is not linux-safe.
if os.name != 'nt': print("This script is only compatible with Windows environments."); sys.exit(2)

# define arguments from commandline and json
try:
    parser = argparse.ArgumentParser()
    parser.add_argument('format', help='The format of the output files.', choices=['mp3','alac'])
    with open("falcon-config.json","r") as file:
        js = json.load(file)
        ARGS = {
            "format":parser.parse_args().format,
            "in_list":js['in_list'],
            "out_folder":js['out_folder'],
            "ffmpeg_path":js['ffmpeg_path']
        }
    
except Exception as e: print(f"Error parsing arguments: {e}"); sys.exit(2)

# parse infile
with open(ARGS['in_list']) as infile: album_folders = [line.rstrip().replace('\"','') for line in infile]

try:
    for album in album_folders:
        # create album output folder
        dest_folder = f"{ARGS['out_folder']}\\{os.path.basename(os.path.dirname(album))} - {os.path.basename(album)}"
        os.makedirs(dest_folder)
        print(f"Creating: {dest_folder}")

        # run ffmpeg
        for file in glob.glob(f"{album}\\*.flac"):
            print(f"  Processing {os.path.basename(file)}...")
            p = subprocess.run(
                [ARGS['ffmpeg_path'], "-i", file] + 
                COMMANDS[ARGS['format']] +
                [f"{dest_folder}\\{os.path.basename(file)[:-5]}.{EXTENSIONS[ARGS['format']]}", "-hide_banner", "-loglevel", "error"])

except Exception as e: print(f"Error during conversion: {e}"); sys.exit(1)

sys.exit(0)