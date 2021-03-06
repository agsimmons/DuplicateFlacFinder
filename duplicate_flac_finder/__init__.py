import subprocess
import json
import argparse
import shutil
import sys
import pathlib
from collections import defaultdict

METAFLAC_PATH = shutil.which("metaflac")
if not METAFLAC_PATH:
    print("ERROR: metaflac not found in path")
    sys.exit(1)


# TODO: Allow user to specify a list of files and directories to include in the comparison


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Finds duplicate FLAC files by comparing the hash of their contained raw audio"
    )
    parser.add_argument("flac_dir", help="Path containing FLAC files to compare")
    return parser.parse_args()


def hash_flac_file(flac_file):
    md5 = subprocess.run(
        [METAFLAC_PATH, "--show-md5sum", str(flac_file)],
        stdout=subprocess.PIPE,
        encoding="utf_8",
    ).stdout.strip()

    return md5


def find_duplicates(flac_files):
    flac_file_hashes = defaultdict(list)
    for flac_file in flac_files:
        md5 = hash_flac_file(flac_file)

        if md5 is not None:
            flac_file_hashes[md5].append(str(flac_file))

    # Remove hashes associated with a single file
    duplicate_file_hashes = dict()
    for key, value in flac_file_hashes.items():
        if len(value) > 1:
            duplicate_file_hashes[key] = value

    return duplicate_file_hashes


def main():
    args = handle_arguments()
    flac_dir = pathlib.Path(args.flac_dir)

    # Find all flac files
    flac_files = flac_dir.glob("**/*.flac")

    duplicate_file_hashes = find_duplicates(flac_files)

    print(json.dumps(duplicate_file_hashes, indent=4, ensure_ascii=False))
