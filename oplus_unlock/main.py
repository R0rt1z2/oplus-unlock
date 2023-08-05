#!/usr/bin/env python

from argparse import ArgumentParser

try:
    from utils.logger import Logger
    from utils.bootloader import BootloaderImage
    from utils.exceptions import NoPatchesFoundException, InvalidImageException
except ImportError:
    from oplus_unlock.utils.logger import Logger
    from oplus_unlock.utils.bootloader import BootloaderImage

def main():
    parser = ArgumentParser()

    parser.add_argument("input_image",  type = str, help="Input bootloader (LK) image.")
    parser.add_argument("-o", "--output", type = str, help="Output (patched) bootloader (LK) image.")
    parser.add_argument("-p", "--patches", type = str, help="Custom json with patches.")
    parser.add_argument("-d", "--debug", action = "store_true", default = False, help="Enable debug logging.")

    args = parser.parse_args()

    if not args.output:
        args.output = "lk-patched.bin"

    logger = Logger(debug=args.debug)
    lk = BootloaderImage(
        logger=logger,
        image = args.input_image,
        patches_file = args.patches
    )

    try:
        lk.parse_image()
    except InvalidImageException as e:
        logger.die(f"Provided image is not a valid LK image ({e})!", 2)

    logger.log(f"Magic        = {hex(lk.magic)}", 0)
    logger.log(f"Size         = {lk.size}", 0)
    logger.log(f"Name         = {lk.name.decode('utf-8')}", 0)
    logger.log(f"Load address = {hex(lk.loaddr)}", 0)
    logger.log(f"Mode         = {hex(lk.mode)}", 0)

    try:
        lk.apply_patches(args.output)
    except NoPatchesFoundException as e:
        logger.die(f"Unable to find valid patches!", 3)

    logger.log(f"Successfully applied {len(lk.patches)} patches ({lk.patches})!", 4)

if __name__ == '__main__':
    main()
