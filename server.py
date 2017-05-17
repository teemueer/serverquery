from query import Query
from packet import Packet

class Server(Query):
    def get_info(self):
        self.connect()
        
        packet = Packet()
        packet.putLong(-1) # Whole
        packet.putByte(0x54) # Header
        packet.putString('Source Engine Query') # Payload
        
        self.udp.send(packet.getvalue())
        packet = self.receive()

        header = packet.getByte()
        result = {}

        if header == 0x49: # Normal response
            result['protocol'] = packet.getByte()
            result['hostname'] = packet.getString()
            result['map'] = packet.getString()
            result['gamedir'] = packet.getString().lower()
            result['gamedesc'] = packet.getString()
            appid = packet.getShort()
            result['numplayers'] = packet.getByte()
            result['maxplayers'] = packet.getByte()
            result['numbots'] = packet.getByte()
            result['servertype'] = chr(packet.getByte())
            result['os'] = chr(packet.getByte())
            result['passworded'] = packet.getByte()
            result['secure'] = packet.getByte()
        
        elif header == 0x6D: # Obsolete Goldsource response
            result['address'] = packet.getString()
            result['hostname'] = packet.getString()
            result['map'] = packet.getString()
            result['gamedir'] = packet.getString().lower()
            result['gamedesc'] = packet.getString()
            result['numplayers'] = packet.getByte()
            result['maxplayers'] = packet.getByte()
            result['protocol'] = packet.getByte()
            result['servertype'] = chr(packet.getByte())
            result['os'] = chr(packet.getByte())
            result['passworded'] = packet.getByte()
            if packet.getByte(): # Is Half-Life mod
                packet.getString() # Link
                packet.getString() # Download Link
                packet.getByte() # NULL
                packet.getLong() # Version
                packet.getLong() # Size
                packet.getByte() # Type
                packet.getByte() # DLL
            result['secure'] = packet.getByte()
            result['numbots'] = packet.getByte()

        return result

    def get_challenge(self):
        packet = Packet()
        packet.putLong(-1) # Whole
        packet.putByte(0x55) # Header
        packet.putLong(-1) # Challenge

        self.udp.send(packet.getvalue())
        packet = self.receive()
        
        header = packet.getByte()
        challenge = None
        
        if header == 0x41:
            challenge = packet.getLong()
        
        return challenge

    def get_players(self):
        self.connect()
        
        challenge = self.get_challenge()
        result = []
        
        if challenge:
            packet = Packet()
            packet.putLong(-1) # Whole
            packet.putByte(0x55) # Header
            packet.putLong(challenge)
            
            self.udp.send(packet.getvalue())
            packet = self.receive()
            
            header = packet.getByte()
            
            if header == 0x44:
                numplayers = packet.getByte()
                try:
                    for x in xrange(numplayers):
                        player = {}
                        packet.getByte() # Index
                        player['name'] = packet.getString()
                        player['score'] = packet.getLong()
                        player['duration'] = int(packet.getFloat())
                        result.append(player)
                except:
                    pass

        return result
        