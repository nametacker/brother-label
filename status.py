from brother.task import Label, Status
from brother.printer import USBPrinter, NetPrinter
from brother.protocol import Command

if __name__ == '__main__':
   
    printer = USBPrinter('/dev/usb/lp0')
    # printer = NetPrinter('192.168.0.47')
    
    #l = Label(printer)
    #s = l.printRaster("sample.png")
    
    # 802042343730000000003e0a0000150000000000000000000000000000000000
    s = Status(printer)
    s.query()
    s.read()
    print(s.error1)
    print(s.error2)
    
    
    