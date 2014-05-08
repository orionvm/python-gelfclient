pygelf
======

Python client for sending UDP messages in Graylog Extended Log Format (GELF).

Messages are zlib compressed, and support the GELF chunked encoding.

Since messages are sent with UDP, the log method should return quickly and not raise an exception due to timeout. However an exception may be raised due to a DNS name resolution problem.

Usage
======
```
import pygelf

gelf_server = 'graylog2.local'

# Using mandatory arguments
gelf = pygelf.UdpClient(gelf_server)

# Using all arguments
gelf = pygelf.UdpClient(gelf_server, port=12202, mtu=8000, source='macbook.local')

# Bare minimum is to send a string, which will map to gelf['short_message']
gelf.log('server is DOWN')

# 'source' and 'host' are the same. Defaults to socket.gethostname()
gelf.log('server is DOWN', source='hostchecker')

# Send different data fields
gelf.log('status change', state='DOWN', server='macbook', source='hostchecker')


# You can also prepare all data into a dictionary and give that to .log
data = {}
data['short_message'] = 'hello from python'
data['host'] = 'hostchecker'
gelf.log(data)
```

See the GELF specification for other fields and their meaning: 
http://graylog2.org/gelf#specs
