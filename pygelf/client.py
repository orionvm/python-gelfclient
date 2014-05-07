import socket
import zlib
import json
import math
import struct 
import time

class Client():

	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def __init__(self, host, port=12201, mtu=1450):
		assert isinstance(host, basestring)
		assert mtu > 12

		self.host = host
		self.port = int(port)
		self.mtu = int(mtu)

	def chunks(self, data):
		chunk_size = self.mtu - 12  # leave space for GELF chunked header
		totalChunks = int(math.ceil(len(data) / float(chunk_size)))
		assert(totalChunks <= 128)
		count = 0
		messageId = hash(str(time.time()) + socket.gethostname())
		for i in xrange(0, len(data), chunk_size):
			header = struct.pack("!ccqBB", '\x1e', '\x0f', messageId, count, totalChunks)
			yield header + data[i:i+chunk_size]
			count += 1

	def log(self, _fields_dict = {}, **fields_named):
		
		if isinstance(_fields_dict, basestring):
			_fields_dict = { 'short_message': _fields_dict }

		message = dict(_fields_dict.items() + fields_named.items())
		
		if 'version' not in message:
			message['version'] = '1.1'
		if 'short_message' not in message:
			message['short_message'] = 'null'
		if 'host' not in message:
			if 'source' in message:
				message['host'] = message['source']
			else:
				message['host'] = 'null'

		#print message		
		message_str = json.dumps(message).encode('utf-8')
		output = zlib.compress(message_str)
		
		if len(output) > self.mtu:
			for chunk in self.chunks(output):
				self.UDPSock.sendto(chunk, (self.host, self.port))
		else:
			self.UDPSock.sendto(output, (self.host, self.port))
