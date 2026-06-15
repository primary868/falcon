import os, sys, glob, subprocess, argparse, shutil, json
from PIL import Image #type: ignore

######### Art Conversion Functions #########

def cover_playdate(img: Image): 
  outfile = os.path.join(OUTFOLDER,'_artwork.gif')
  img.resize((128, 128), Image.Resampling.LANCZOS).convert("1").save(outfile,'GIF')
  print("Playdate-format cover art saved.")

def cover_ipod(img: Image): 
  outfile = os.path.join(OUTFOLDER,'cover.jpg')
  img.resize((600,600)).save(outfile)
  print("iPod/iTunes format cover saved.")

######### Functions #########

def run_command(cmd: list) -> int: 
  if ARGS.show_command: print(' '.join(cmd))
  return subprocess.run(cmd, check=True).returncode

def get_cover_img_data() -> Image:
  print("Getting source cover art")
  
  # look for cover.jpg
  if os.path.exists(cov := os.path.join(ARGS.infolder,"cover.jpg")): return Image.open(cov)
  else: print("Could not find cover.jpg -- extracting from FLACs")

  # extract from one of the flac files
  extracted_tmp = ("extracted_tmp.jpg")
  source_file = INFILES[0]
  run_command(['ffmpeg', '-loglevel', 'error', '-hide_banner', '-i', source_file, '-an', '-vcodec', 'copy', extracted_tmp])
  output = Image.open(extracted_tmp)
  os.remove(extracted_tmp)
  print(f"Got cover art from {source_file}")
  return output

def album_artist_map() -> list:
  print("--- Getting album artist ---")
  try: 
    album_artist = subprocess.run(
      ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=album_artist', '-of', 'default=noprint_wrappers=1:nokey=1', INFILES[0]],
      check=True,
      capture_output=True
    ).stdout.decode('utf-8').strip()
    if album_artist == '': raise
  except: 
    print("Could not find album artist in source files. Outfiles will use original artist tags.")
    return []
  else: 
    print(f"Album artist is: '{album_artist}'")
    return['-metadata',f'artist={album_artist}']
  
def make_template_command() -> list:
  print("=== Make base ffmpeg command ===")
  cmd = ['ffmpeg','-loglevel','error','-hide_banner']
  if ARGS.overwrite: cmd += ['-y']
  cmd += ['-i',9] # 9 is replaced by flac file path during use
  cmd += THIS['output_format'].split()
  if THIS['use_album_artist']: cmd += album_artist_map()
  # path to output file is tacked onto the end when the command is used
  return cmd

######### Prereq #########

try:
  for dep in ['ffmpeg','ffprobe']: assert shutil.which(dep), f"Dependency not found: {dep}"
  
  with open('./falcon_config.json','r') as file:
    data = json.load(file)
    FLAGS = data['out_types']
    OUTFOLDER = data['outfolder']
  
  parser = argparse.ArgumentParser()
  parser.add_argument('infolder',help="folder of flac files to convert")
  parser.add_argument('out_type',choices=list(FLAGS.keys()),help="Type of conversion to perform")
  parser.add_argument('--overwrite','-y',action='store_true',help='Overwrite existing output files')
  parser.add_argument('--show_command','-s',action='store_true',help='Show generated ffmpeg commands')
  ARGS = parser.parse_args()
  ARGS.infolder = os.path.expanduser(ARGS.infolder)

  INFILES = glob.glob(os.path.join(ARGS.infolder,'*.flac'))
  assert INFILES, "No flac files found in input folder."

  OUTFOLDER = os.path.expanduser(OUTFOLDER).replace(r'%A%',os.path.basename(ARGS.infolder)).replace(r'%F%',ARGS.out_type)
  if not os.path.exists(OUTFOLDER): os.makedirs(OUTFOLDER)
  print(f"Saving to folder: {OUTFOLDER}")

  THIS = FLAGS[ARGS.out_type]

except Exception as e:
  print(f"{type(e).__name__}: {e}")
  sys.exit(2)

######### Main #########

try:
  if (func_name := THIS['cover_func']): 
    print("=== Make output cover art ===")
    source_img = get_cover_img_data()
    globals().get(func_name)(source_img)
  
  cmd = make_template_command()
  print("Command made.")

  print("=== Convert FLAC files ===")
  for flac in INFILES:
    outfile = os.path.join(OUTFOLDER, os.path.splitext(os.path.basename(flac))[0]+'.'+THIS['ext'])
    this_cmd = [flac if arg == 9 else arg for arg in cmd]+[outfile] # fill in infile and outfile paths
    run_command(this_cmd)
    print(f"Done: {os.path.basename(outfile)}")

except Exception as e:
  print(f"{type(e).__name__}: {e}")
  sys.exit(1)
else: print("=== All operations complete ===")