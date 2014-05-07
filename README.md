pygelf
======

Python client for sending UDP messages in Graylog Extended Log Format (GELF)

Usage
======
```
import pygelf

# Using mandatory arguments
gelf = pygelf.Client('graylog2.local')

# Using all arguments
gelf = pygelf.Client('graylog2.local', port=12202, mtu=8000)

# Bare minimum is to send a string, which will map to gelf['short_message']
gelf.log('server is DOWN')

# You should also supply 'host' as this is displayed on graylog as 'source'
gelf.log('server is DOWN', host='hostchecker')

# Send different data fields
gelf.log('status change', state='DOWN', server='macbook', host='hostchecker')


# You can also prepare all data into a dictionary and give that to .log
data = {}
data['short_message'] = 'hello from python'
data['host'] = 'hostchecker'
gelf.log(data)
```

See the GELF specification for other fields and their meaning: 
http://graylog2.org/gelf#specs
