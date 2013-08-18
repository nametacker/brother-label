from brother.protocol import Command, PrintInformation, CompressionMode, CommandMode
from PIL import Image
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        #self.commands.append("1B6953") # Status
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
            #b = bytes.fromhex(hstr)
            self.commands.append(hstr)
        self.commands.append(self.c.print_last_page())
        
        for command in self.commands:
            self.printer.send(command)
            
        s = Status(self.printer)
        s.read()
        return s
        
        