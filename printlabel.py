"""
Read status from printer connected via USB.
"""

from brother.task import Status
from brother.printer import USBPrinter

if __name__ == '__main__':
    printer = USBPrinter('/dev/usb/lp0')
    s = Status(printer)
    s.query()
    s.read()
    print(s.error1)
    print(s.error2)
    
    
    