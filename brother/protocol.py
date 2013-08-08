class PrintInformation(object):
    
    flags_media_type = 0x02
    flags_media_width = 0x04
    flags_media_length = 0x08
    flags_priority = 0x40
    flags_printer_recovery_always_on = 0x80
    
    media_type_continous = "0A"
    media_type_diecut = "0B"
    
    page_start = "00"
    page_other = "01"
    
class CommandMode(object):
    
    escp = "00"
    raster = "01"
    ptouch_template = "03"
    
class CompressionMode(object):
    
    no_compression = 0x00
    tiff = 0x02
    
class Command(object):
    
    def status(self):
        """
        Before sending print data to the printer, this command should be sent once. Since error
information is automatically sent by the printer during printing, do not send this command while
printing.
        """
        return self.command_prefix() + "53"
        
    
    def invalidate(self):
        """
        Sends a 200-byte invalidate command, and then resets the printer
to the receiving state.
        """
        return "00" * 200
    
    def command_prefix(self):
        """
        Every printer command is prefixed with this sequence
        """
        return "1B69"
    
    def initialize(self):
        """
        Initializes the printer for printing.
        """
        return "1B40"
    
    def select_mode(self, mode):
        """
        Switches the printer to raster mode.
        """
        return self.command_prefix() + "61" + mode
    
    def margin_amount(self, margin):
        """
        Specify margin amount (feed amount at beginning and end of page)
        """
        return self.command_prefix() + "64" + self.hex(int(margin / 256) << 8 | margin % 256)
    
    def print_information(self, flags, media_type, media_width, media_length, num_lines, start_page=PrintInformation.page_start):
        """
        Print information command
        """
        return "1B697A" + self.hex(flags) + media_type + self.hex(media_width) + self.hex(media_length) + self.hex(int(num_lines / 256)) + self.hex(num_lines % 256) + "0000" + start_page + "00"
    
    def print_page(self):
        """
        Used as a print command at the end of pages other than the last page when multiple pages are printed.
        """
        return "0C"
    
    def print_last_page(self):
        """
        Used as a print command at the end of the last page.
        """
        return "1A"
    
    def various_mode(self, mode):
        """
        Set various switches
        """
        return self.command_prefix() + "4D" + self.hex(mode)
    
    def compression_mode(self, mode):
        """
        Select compression mode
        """
        return self.various_mode(mode)
    
    def auto_cut(self, auto=True):
        """
        Select cut mode
        """
        if auto:
            return self.various_mode(1 << 6)
        else:
            return self.various_mode(0 << 6)
        
    def cut_after(self, page):
        """
        Specify the page number in “cut each * labels”
        """
        return self.command_prefix() + "41" + self.hex(page)
    
    def expand_mode(self, cut_at_end=True, high_resolution=False):
        """
        Expanded mode
        """
        mode = 0
        if cut_at_end:
            mode = mode | 1 << 3
        if high_resolution:
            mode = mode | 1 << 6
        return self.command_prefix() + self.hex(mode)
    
    def hex(self, n):
        return "%0.2x" % n

            
