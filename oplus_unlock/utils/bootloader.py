import io
import struct

class BootloaderImage:
    SEQUENCES = [
        bytes.fromhex("2de9f04fadf5ac5d"), # Android 9
        bytes.fromhex("f0b5adf5925d")      # Android 10/11
    ]

    def __init__(self, image: str):
        self.image = image
        self.magic = None
        self.size = None
        self.name = None
        self.loaddr = None
        self.mode = None
        self.sequence = None
        self.offset = None

    def parse_image(self):
        with open(self.image, 'r+b') as f:
            f.seek(0x4040 if f.read(4) == b'BFBF' else 0)
            header = struct.Struct('<II32sII')

            self.magic, self.size, self.name, self.loaddr, \
                self.mode = header.unpack(f.read(header.size))

            if int(hex(self.magic), 0) != 0x58881688:
                raise Exception("invalid magic")

            if int(hex(self.loaddr), 0) == 0xffffffff:
                while header != b'\x10\xff\x2f\xe1':
                    header = f.read(4)

                f.seek(f.tell() + 4)
                self.loaddr = struct.unpack("<I", f.read(4))[0]

    def get_lock_sequence(self):
        with open(self.image, 'r+b') as f:
            data = f.read()

        for seq in self.SEQUENCES:
            offset = data.find(seq)
            if offset != -1:
                self.sequence, self.offset = seq, offset

        if self.sequence is None:
            raise Exception("no suitable sequence was found")

    def update_lock_sequence(self, out: str):
         with open(out, 'w+b') as o:
             with open(self.image, 'r+b') as f:
                 # 00 20 => movs r0, #0x0 
                 # 70 47 => bx   lr
                 o.write(f.read(self.offset) + \
                     bytes.fromhex("00207047"))
                 f.seek(f.tell() + len(self.sequence) - 2) # pad
                 o.write(f.read())