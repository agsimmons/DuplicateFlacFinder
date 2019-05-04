import glob
import subprocess
import json
import argparse
import shutil
import sys

METAFLAC_PATH = shutil.which('metaflacvc')
if not METAFLAC_PATH:
    print('ERROR: metaflac not found in path')
    sys.exit(1)


# TODO: Allow user to specify a list of files and directories to include in the comparison


def handle_arguments():
    parser = argparse.ArgumentParser('Finds duplicate FLAC files by comparing the hash of their contained raw audio')
    parser.add_argument('flac_dir', help='Path containing FLAC files to compare')
    return parser.parse_args()


def main():
    args = handle_arguments()

    # Find all flac files
    flac_files = glob.glob(args.flac_dir + r'\**\*.flac', recursive=True)

    flac_file_hashes = dict()

    for flac_file in flac_files:
        md5 = subprocess.run(f'"{METAFLAC_PATH}" --show-md5sum "{flac_file}"', stdout=subprocess.PIPE, encoding='utf_8').stdout[:-1]
        if md5 is not None:
            if md5 in flac_file_hashes:
                flac_file_hashes[md5].append(flac_file)
            else:
                flac_file_hashes[md5] = [flac_file]

    duplicate_file_hashes = dict()

    for key, value in flac_file_hashes.items():
        if len(value) > 1:
            duplicate_file_hashes[key] = value

    print(json.dumps(duplicate_file_hashes, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
