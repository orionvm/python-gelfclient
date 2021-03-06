import os
import sys
import socket
import time
import string
import random
import unittest
from gelfclient import UdpClient as GelfUdp

string_types = str if sys.version_info[0] == 3 else basestring

HOST = os.environ.get('GELF_TEST_HOST', 'localhost')
PORT = int(os.environ.get('GELF_TEST_PORT', '12201'))

print('Sending UDP GELF packets to %s:%s' % (HOST, PORT))

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(length)))


class TestUdp(unittest.TestCase):
    def test_init(self):
        gelf = GelfUdp(HOST, PORT)
        self.assertEqual(gelf.server, HOST)
        self.assertIsInstance(gelf.port, int)
        self.assertEqual(gelf.source, socket.gethostname())

    def test_log_minimum(self):
        gelf = GelfUdp(HOST, PORT)
        jsn = gelf.log(sys._getframe().f_code.co_name)
        msg = jsn['short_message']
        self.assertEqual(msg, sys._getframe().f_code.co_name)
        self.assertEqual(jsn['host'], socket.gethostname())
        self.assertIsInstance(jsn['version'], string_types)

    def test_log_source(self):
        gelf = GelfUdp(HOST, PORT, source='source')
        jsn = gelf.log(sys._getframe().f_code.co_name)
        self.assertEqual(jsn['host'], 'source')

    def test_log_source_override(self):
        gelf = GelfUdp(HOST, PORT, source='source')
        jsn = gelf.log(sys._getframe().f_code.co_name, source='notsource')
        self.assertEqual(jsn['host'], 'notsource')
        jsn = gelf.log(sys._getframe().f_code.co_name, host='notsource')
        self.assertEqual(jsn['host'], 'notsource')

    def test_log_extra_value(self):
        gelf = GelfUdp(HOST, PORT)
        jsn = gelf.log(sys._getframe().f_code.co_name, server='server', test='test')
        self.assertEqual(jsn['server'], 'server')
        self.assertEqual(jsn['test'], 'test')

    def test_log_timestamp(self):
        gelf = GelfUdp(HOST, PORT)
        ts = time.time() - 120  # override timestamp 2 mintes in past
        jsn = gelf.log(sys._getframe().f_code.co_name, timestamp = ts)
        self.assertEqual(jsn['timestamp'], ts)

    def test_log_chunked(self):
        gelf = GelfUdp(HOST, PORT, mtu=50)
        data = random_string(gelf.mtu * 5)
        jsn = gelf.log(sys._getframe().f_code.co_name, data=data)

    def test_log_chunked_small_mtu(self):
        gelf = GelfUdp(HOST, PORT, mtu=50)
        data = random_string(gelf.mtu * 5)
        jsn = gelf.log(sys._getframe().f_code.co_name, data=data)

    def test_default_log_level(self):
        gelf = GelfUdp(HOST, PORT)
        jsn = gelf.log(sys._getframe().f_code.co_name)
        self.assertEqual(jsn['level'], 1)

    def test_different_log_level(self):
        gelf = GelfUdp(HOST, PORT)
        for level in [0, 4, '0', '3', '7']:
            jsn = gelf.log(sys._getframe().f_code.co_name, level=level)
            self.assertEqual(jsn['level'], int(level))

    def test_out_of_range_level(self):
        gelf = GelfUdp(HOST, PORT)
        for level in [-1, 8]:
            with self.assertRaises(AssertionError):
                jsn = gelf.log(sys._getframe().f_code.co_name, level=level)

    def test_wrong_type_for_level(self):
        gelf = GelfUdp(HOST, PORT)
        with self.assertRaises(ValueError):
            jsn = gelf.log(sys._getframe().f_code.co_name, level='not a number!')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
