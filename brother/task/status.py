class Status(object):
    
    def __init__(self, printer):
        self.printer = printer
        
    def query(self):
        self.printer.send("1B6953") # Status
            
    def read(self):
        #self.printer.send("00" * 200) # Reset
        #self.printer.send("1b40") # Init
        data = self.printer.read()
        self.printer.close()
        if len(data) != 32:
            raise Exception("Failed to read printer status")
        # Model
        self.model = "unknown"
        if data[4] == 0x36:
            self.model = "QL-710W" 
        if data[4] == 0x37:
            self.model = "QL-710NW" 
            
        # Error 1
        self.error1 = 0
        error1 = data[8]
        if error1 & 0x01:
            self.error1 = "No media error"
        if error1 & 0x02:
            self.error1 = "End of media"
        if error1 & 0x04:
            self.error1 = "Cutter jam"
        if error1 & 0x10:
            self.error1 = "Printer in use"
        if error1 & 0x20:
            self.error1 = "Printer turned off"
            
        # Error 1
        self.error2 = 0
        error2 = data[9]
        if error2 & 0x01:
            self.error2 = "Replace media"
        if error2 & 0x02:
            self.error2 = "Expansion buffer full"
        if error2 & 0x04:
            self.error2 = "Communication error"
        if error2 & 0x10:
            self.error2 = "Cover open"
        if error2 & 0x40:
            self.error2 = "Media cannot be fed"
        if error2 & 0x80:
            self.error2 = "System error"
