from hashlib import md5
from pathlib import Path
from collections import OrderedDict

from duplicate_flac_finder import hash_flac_file, find_duplicates

BUFFER_SIZE = 65535

RESOURCE_PATH = Path(__file__).parent / "res"
FLAC_FILES = list(RESOURCE_PATH.glob("**/*.flac"))


def hash_file(file_path):
    hasher = md5()

    with open(file_path, "rb") as f:
        buffer = f.read(BUFFER_SIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(BUFFER_SIZE)

    return hasher.hexdigest()


def test_normal_hashes():
    hashes = []
    for file in FLAC_FILES:
        hashes.append(hash_file(file))

    assert sorted(hashes) == [
        "2a2ede58cab4e031b005223f69945568",
        "2a2ede58cab4e031b005223f69945568",
        "4a23f042e74abe71e234863b5511c02b",
        "4a23f042e74abe71e234863b5511c02b",
        "6685d91bae6656350aa0022f1249e64b",
    ]


def test_flac_hashes():
    hashes = []
    for file in FLAC_FILES:
        hashes.append(hash_flac_file(file))

    assert sorted(hashes) == [
        "7dbd054753e1390a5a5368184c85e70f",
        "7dbd054753e1390a5a5368184c85e70f",
        "e55a6c6266f4d4be65c9391d552c7b1c",
        "fd49f2c54cfb1f92a2d0cff0846fe907",
        "fd49f2c54cfb1f92a2d0cff0846fe907",
    ]


def test_find_duplicates():
    duplicate_flac_files = sorted(OrderedDict(find_duplicates(FLAC_FILES)))

    assert duplicate_flac_files == sorted(OrderedDict({
        "fd49f2c54cfb1f92a2d0cff0846fe907": [
            "tests/res/test1.flac",
            "tests/res/test1_dup.flac",
        ],
        "7dbd054753e1390a5a5368184c85e70f": [
            "tests/res/test2_dup.flac",
            "tests/res/test2.flac",
        ],
    }))
