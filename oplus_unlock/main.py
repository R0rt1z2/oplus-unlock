#!/usr/bin/env python

from argparse import ArgumentParser

try:
    from utils.logger import Logger
    from utils.bootloader import BootloaderImage
except ImportError:
    from oplus_unlock.utils.logger import Logger
    from oplus_unlock.utils.bootloader import BootloaderImage

def main():
    parser = ArgumentParser()

    parser.add_argument("input_image",  type = str, help="Input bootloader (LK) image.")
    parser.add_argument("-o", "--output", type = str, help="Output (patched) bootloader (LK) image.")

    args = parser.parse_args()

    if not args.output:
        args.output = "lk-patched.bin"

    logger = Logger()
    lk = BootloaderImage(image = args.input_image)

    try:
        lk.parse_image()
    except Exception as e:
        logger.die(f"Provided image is not a valid LK image ({e})!", 2)

    logger.log(f"Magic        = {hex(lk.magic)}", 0)
    logger.log(f"Size         = {lk.size}", 0)
    logger.log(f"Name         = {lk.name.decode('utf-8')}", 0)
    logger.log(f"Load address = {hex(lk.loaddr)}", 0)
    logger.log(f"Mode         = {hex(lk.mode)}", 0)

    try:
        lk.get_lock_sequence()
    except Exception as e:
        logger.die(f"Could not find the lock sequence ({e})", 2)

    logger.log(f"Sequence     = {lk.sequence.hex()} (0x{lk.offset:02x})", 0)

    try:
        lk.update_lock_sequence(args.output)
    except Exception as e:
        logger.die(f"Could not enable fastboot ({e})!", 3)

    logger.log(f"Sucessfully enabled fastboot. Check {args.output}!", 4)

if __name__ == '__main__':
    main()
