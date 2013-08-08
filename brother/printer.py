import logging
import socket
import binascii
from time import sleep

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NetPrinter(object):
    
    port = 9100
    
    def __init__(self, host):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.s.connect((self.host, self.port))
        logger.debug('Connected to %s:%d' % (self.host, self.port))
        
    def send(self, hexdata):
        hexdata = hexdata.lower()
        data = bytearray(binascii.unhexlify(hexdata))
        self.s.send(data)
        logger.debug('Sent: %s' % (hexdata))
        
    def read(self):
        data = self.s.recv(32)
        logger.debug('Received: %s' % (binascii.hexlify(data)))
        return data
    
    def close(self):
        self.s.close()
        logger.debug('Closed connection to: %s:%d' % (self.host, self.port))
        
class USBPrinter(object):
    
    def __init__(self, device):
        self.device = device
        self.open()
        
    def open(self):
        self.dev = open(self.device, 'r+b')
        logger.debug('Opened connection to: %s' % (self.device))
        
    def send(self, hexdata):
        hexdata = hexdata.lower()
        self.dev.write(binascii.unhexlify(hexdata))
        logger.debug('Sent: %s' % (hexdata))
        
    def read(self):
        data = self.dev.read(32)
        logger.debug('Received: %s' % (binascii.hexlify(data)))
        return data
    
    def close(self):
        self.dev.close()
        logger.debug('Closed connection to: %s' % (self.device))
