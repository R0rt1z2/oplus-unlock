import io
import json
import struct

from .logger import Logger
from .exceptions import NoPatchesFoundException,\
    InvalidImageException, InvalidPatchFileException

class BootloaderImage:
    RETURN_0 = bytes.fromhex("00207047")
    PATCHES = {
        "fastboot": {
            "2de9f04fadf5ac5d": RETURN_0,
            "f0b5adf5925d": RETURN_0,
        },
        "dm_verity": {
            "30b583b002ab": RETURN_0,
        },
        "orange_state": {
            "08b50a4b7b441b681b68022b": RETURN_0,
        },
        "red_state": {
            "f0b5002489b0": RETURN_0,
        },
    }

    def __init__(self, image: str, logger : Logger, patches_file : str):
        self.logger = logger
        self.image = image
        self.patches = []
        self.magic = None
        self.size = None
        self.name = None
        self.loaddr = None
        self.mode = None
        self.sequence = None
        self.offset = None

        if patches_file:
            self.load_patches(patches_file)
            self.logger.log(f"Loaded {len(self.PATCHES)} patches from {patches_file}!", 4)

    def parse_image(self):
        with open(self.image, 'r+b') as f:
            f.seek(0x4040 if f.read(4) == b'BFBF' else 0)
            header = struct.Struct('<II32sII')

            self.magic, self.size, self.name, self.loaddr, \
                self.mode = header.unpack(f.read(header.size))

            if int(hex(self.magic), 0) != 0x58881688:
                raise InvalidImageException("invalid magic")

            if int(hex(self.loaddr), 0) == 0xffffffff:
                while header != b'\x10\xff\x2f\xe1':
                    header = f.read(4)
                    # If we reach the end of the file, we can assume that
                    # the provided image is not a valid LK image.
                    if header == b'':
                        raise InvalidImageException("invalid load address")

                f.seek(f.tell() + 4)
                self.loaddr = struct.unpack("<I", f.read(4))[0]

    def validate_patches(self):
        if not isinstance(self.PATCHES, dict):
            raise InvalidPatchFileException("Patch file must contain a JSON object at the root.")

        for category, patches in self.PATCHES.items():
            if not isinstance(category, str) or not isinstance(patches, dict):
                raise InvalidPatchFileException(
                    f"Category '{category}' must be a string and its patches must be a JSON object.")

            for original_hex, patch in patches.items():
                if not isinstance(original_hex, str) or not isinstance(patch, str):
                    raise InvalidPatchFileException(f"Patch '{original_hex}' and its replacement must be strings.")

    def load_patches(self, file):
        with open(file, 'r') as f:
            self.PATCHES = json.load(f)
            self.validate_patches()
            for category in self.PATCHES:
                for patch in self.PATCHES[category]:
                    self.PATCHES[category][patch] = bytes.fromhex(self.PATCHES[category][patch])

    def apply_patch(self, data: bytearray, original: bytes, patch: bytes, name: str):
        offset = data.find(original)
        if offset != -1:
            self.patches.append(name)
            data[offset:offset + len(patch)] = patch
        else:
            self.logger.log(f"Unable to apply patch for {name} ({original.hex()})!", 5)

    def apply_patches(self, output):
        with open(self.image, 'r+b') as f:
            data = bytearray(f.read())

        for category, patches in self.PATCHES.items():
            for original_hex, patch in patches.items():
                original_bytes = bytes.fromhex(original_hex)
                self.apply_patch(data, original_bytes, patch, category)

        if not self.patches:
            raise NoPatchesFoundException("No valid patches were found!")

        with open(output, 'w+b') as f:
            f.write(data)