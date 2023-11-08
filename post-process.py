#!/usr/bin/env python3

import argparse
from datetime import datetime,timedelta
import exiftool
import os
import shutil
import sys

FILENAME_TEMPLATE = 'JAPAN_{datetimestr}_{counter}.jpg'
DATETIME_STR = '%Y%m%d_%H%M%S'
TIME_OFFSET = timedelta(days=31)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, help="input directory with scalpel results", default='./scalpel-out')
  parser.add_argument("-o", "--output", type=str, help="output directory for processed files", default='./processed')
  args = parser.parse_args()
  input_dir = args.input
  output_dir = args.output
  print('Processing scalpel files from {inp} and writing to {out}'.format(inp=input_dir, out=output_dir))
  if not os.path.exists(output_dir):
    print('Creating folder {out}'.format(out=output_dir))
    os.mkdir(output_dir)

  last_timestr = ''
  counter = 1
  total_counter = 0

  with exiftool.ExifToolHelper() as et:
    for path, _, filenames in os.walk(input_dir):
      for filename in sorted(filenames):
        # filter jpgs
        if not filename.lower().endswith('.jpg'):
          print('Skipping {f}'.format(f=filename))
          continue
        try:
          data = et.get_metadata(os.path.join(path,filename))
          # filter too small images
          if data[0]['EXIF:ExifImageWidth'] != 4288:
            print('Skipping {img}, too small'.format(img=filename))
            continue
          origdatestr = data[0]['EXIF:DateTimeOriginal']
        except Exception as e:
          print('[!] Could not process {f}'.format(f=filename))
          continue
        origdate = datetime.strptime(origdatestr, '%Y:%m:%d %H:%M:%S')
        origdate = origdate + TIME_OFFSET
        new_timestr = origdate.strftime(DATETIME_STR)
        if new_timestr == last_timestr:
          counter += 1
        else:
          counter = 1
        total_counter += 1
        last_timestr = new_timestr
        outfilename = FILENAME_TEMPLATE.format(datetimestr=new_timestr, counter=str(counter).zfill(2))

        print('Creating {a} (from {b})'.format(a=outfilename, b=filename))
        shutil.copy(os.path.join(path, filename), os.path.join(output_dir, outfilename))
  print('Processed and written {n} files matching the filter to {out}'.format(n=total_counter, out=output_dir))        

if __name__ == '__main__':
  main()

