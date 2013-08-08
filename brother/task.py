from brother.protocol import Command, PrintInformation, CompressionMode, CommandMode
from PIL import Image
import logging
import socket
import binascii
from struct import pack, unpack

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Status(object):
    
    def __init__(self, printer):
        self.printer = printer
    
    def read(self):
        #self.printer.send("00" * 200) # Reset
        #self.printer.send("1b40") # Init
        self.printer.send("1B6953") # Status
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

class Label(object):
    
    commands = []
    
    def __init__(self, printer, width=720):
        self.c = Command()
        self.printer = printer
        self.width = 720
    
    def printRaster(self, rasterFile):
        
        im = Image.open(rasterFile)
        if im.mode not in ("P"):
            logger.info('Converting to b/w image')
            im.convert('P')
        width, height = im.size
        if (width != self.width):
            #resize to 720px width
            logger.info('Resizing to 720px width')
            im.resize(self.width, self.width / width * height, filter=Image.ANTIALIAS)
        line = 0
        row = 0
        data = [""]
        for px in list(im.getdata()):
            if len(data) - 1 != line:
                data.append("")
            data[line] = data[line] + "%d" % px
            row = row + 1
            if row % self.width == 0:
                line = line + 1
                row = 0
            
        logger.debug('%d lines of data' % len(data))
        
        self.commands.append(self.c.invalidate())
        self.commands.append(self.c.initialize())
        self.commands.append(self.c.select_mode(CommandMode.raster))
        i = self.c.print_information(
             PrintInformation.flags_media_type | PrintInformation.flags_media_width | PrintInformation.flags_printer_recovery_always_on,
             PrintInformation.media_type_continous,
             62, # width 62mm
             0, # width infinite
             len(data), # number if data lines
        )
        self.commands.append(i)
        self.commands.append(self.c.auto_cut(True))
        self.commands.append(self.c.cut_after(1))
        self.commands.append(self.c.expand_mode(True, False))
        self.commands.append(self.c.margin_amount(35))
        self.commands.append(self.c.compression_mode(CompressionMode.no_compression))
        
        for line in data:
            hstr = '%0*X' % ((len(line) + 3) // 4, int(line, 2))
            b = bytes.fromhex(hstr)
            self.commands.append(b)
        self.commands.append(self.c.print_last_page())
        
        for command in self.commands:
            self.printer.send(command)
        
        