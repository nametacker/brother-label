from brother.task import Label, Status
from brother.printer import USBPrinter, NetPrinter
from brother.protocol import Command

if __name__ == '__main__':
   
    printer = USBPrinter('/dev/usb/lp0')
    # printer = NetPrinter('192.168.0.47')
    
    #l = Label(printer)
    #l.printRaster("sample.png")
    
    s = Status(printer)
    s.read()
    print(s.model)
    print(s.error1)
    print(s.error2)
    
    
    