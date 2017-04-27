import socket
from packet import Packet

class Query(object):
	def __init__(self, addr):
		self.addr = addr
		self.udp = False
		
	def connect(self, timeout=3):
		self.disconnect()
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.settimeout(timeout)
		self.udp.connect(self.addr)
		
	def disconnect(self):
		if self.udp:
			self.udp.close()
			self.udp = False
			
	def receive(self):
		packet = Packet(self.udp.recv(2048))
		typ = packet.getLong()
		if typ == -1: # Packet is whole
			return packet