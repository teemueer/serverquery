from query import Query
from packet import Packet

class Master(Query):
    def get_servers(self, **filters):
        self.connect()
        
        first = last = ('0.0.0.0', 0)
        filter = ''
        for pair in filters.items():
            filter += r'\%s\%s' % pair
        
        while True:
            packet = Packet()
            packet.putByte(0x31) # Message Type
            packet.putByte(0xFF) # Region Code
            packet.putString('%s:%d' % last) # IP:Port
            packet.putString(filter) # Filter

            self.udp.send(packet.getvalue())
            packet = self.receive()
            
            packet.getByte() # 0x66
            packet.getByte() # 0x0A

            len = packet.len
            while packet.tell() != len:
                oct1 = packet.getByte() # First octet
                oct2 = packet.getByte() # Second octet
                oct3 = packet.getByte() # Third octet
                oct4 = packet.getByte() # Fourth octet
                port = packet.getShort(network=True) # Port number
                
                addr = ('%d.%d.%d.%d' % (oct1, oct2, oct3, oct4), port)
                if addr != first and addr != last:
                    yield addr
                last = addr
                
            if last == first:
                break