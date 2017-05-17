import struct
from StringIO import StringIO

class Packet(StringIO):
    def putByte(self, val):
        self.write(struct.pack('<B', val))

    def getByte(self):
        try: return struct.unpack('<B', self.read(1))[0]
        except: return 0

    def putShort(self, val):
        self.write(struct.pack('<h', val))

    def getShort(self, network=False):
        if not network:
            return struct.unpack('<h', self.read(2))[0]
        else:
            return struct.unpack('!H', self.read(2))[0]

    def putLong(self, val):
        self.write(struct.pack('<l', val))

    def getLong(self):
        try: return struct.unpack('<l', self.read(4))[0]
        except: return 0

    def getLongLong(self):
        try: return struct.unpack('<Q', self.read(8))[0]
        except: return 0

    def putFloat(self, val):
        self.write(struct.pack('<f', val))

    def getFloat(self):
        try: return struct.unpack('<f', self.read(4))[0]
        except: return 0

    def putString(self, val):
        self.write(val + '\x00')

    def getString(self):
        try:
            val = self.getvalue()
            start = self.tell()
            end = val.index('\0', start)
            val = val[start:end]
            self.seek(end+1)
            return val
        except:
            return 0