import socket
import zlib
import json
import math
import struct
from datetime import datetime

class UdpClient():

    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, server, port=12201, mtu=1450, source=None):
        assert isinstance(server, basestring)
        assert mtu > 12

        self.server = server
        self.port = int(port)
        self.mtu = int(mtu)
        self.source = source if source else socket.gethostname()

    def chunks(self, data):
        chunk_size = self.mtu - 12  # leave space for GELF chunked header
        totalChunks = int(math.ceil(len(data) / float(chunk_size)))
        assert(totalChunks <= 128)
        count = 0
        messageId = hash(str(datetime.now().microsecond) + self.source)
        for i in xrange(0, len(data), chunk_size):
            header = struct.pack("!ccqBB", '\x1e', '\x0f', messageId, count, totalChunks)
            count += 1
            yield header + data[i:i+chunk_size]

    def log(self, _fields_dict = {}, **fields_named):
        if isinstance(_fields_dict, basestring):
            _fields_dict = { 'short_message': _fields_dict }

        message = dict(_fields_dict.items() + fields_named.items())
        message['version'] = '1.1'
        if 'short_message' not in message:
            message['short_message'] = 'null'
        if 'host' not in message:
            if 'source' in message:
                message['host'] = message['source']
            else:
                message['host'] = self.source
        level = int(message.get('level', 1)) # Default severity / level is alert (1)
        assert(0 <= level <= 7)
        message['level'] = level

        message_str = json.dumps(message).encode('utf-8')
        output = zlib.compress(message_str)
        if len(output) > self.mtu:
            for chunk in self.chunks(output):
                self.UDPSock.sendto(chunk, (self.server, self.port))
        else:
            self.UDPSock.sendto(output, (self.server, self.port))

        return message
