# -*- version: python3 -*-
# -*- coding : utf-8   -*-
# =============================================================================
# Created By  : Ryan Strasburg
# Created Date: Fri March 31 11:00:00 PDT 2023
# =============================================================================
"""Trimble Zebra Printing was built to simplify and standardize ZPL printing
   in the Trimble Facilities. This includes features, such as DPI scaling,
   to improve printing automation. Upscaling DPI results in a loss of quality.
   Matching DPIs or downscaling is recommended."""
# =============================================================================
# Imports
# =============================================================================
from TrimbleZebraPrinting import trimble_graphics_conversion as tgc
import win32print

"""
ZPL Commands Capable of Scaling.
The following represent the ZPL commands that are capable of being resized.
"""
scalable_cmds = [
    "A0",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "B3",
    "B7",
    "BC",
    "BQ",
    "BY",
    "FB",
    "FO",
    "FT",
    "GB",
    "LH",
    "LH",
    "LL",
    "LS",
    "LT",
    "PW",
]

class Zebra:
    """
    Class To Communicate & Print With (Zebra) Label Printers.
    """

    def __init__(self, queue = None):
        """
        Initialize Printer Queue.
        :param queue: printer queue (string)
        """
        if queue is None:
            self.queue = win32print.GetDefaultPrinter()
        else:
            self.queue = queue

    def _rescale(self, commands, desired_resolution, current_resolution):
        """
        Rescale Label Per DPI.
        :param commands: ZPL code (string)
        :param desired_resolution: printer resolution (int)
        :param current_resolution: label resolution (int)
        :return: scaled ZPL code (string)
        """
        scaled_commands = ''
        for line in commands.split('\n'):
            scaled_sections = []
            if 'GFA' in line:
                scaled_sections.append(
                    self._scale_section(line, desired_resolution / current_resolution)
                )
            else:
                for section in line.split('^'):
                    scaled_sections.append(
                        self._scale_section(section, desired_resolution / current_resolution)
                    )
            scaled_commands += '^'.join([str(elem) for elem in scaled_sections]) + '\n'
        return scaled_commands

    def _scale_section(self, section_value, scale_factor):
        """
        Scale Individual Section of Label Per DPI.
        :param section_value: ZPL command (string)
        :param scale_factor: scale factor on label (float)
        :return: scaled ZPL command (string)
        """
        if any(section in section_value for section in scalable_cmds) and 'GFA' in section_value:
            section_split = section_value.split('^')
            section_parts = section_split[:2][1][2:].split(',')
            gf_command = str(section_split[2:])
            rescaled_x = int(round(float(section_parts[0]) * scale_factor))
            rescaled_y = int(round(float(section_parts[1]) * scale_factor))
            return self._scale_image(gf_command, rescaled_x, rescaled_y, scale_factor)
        elif any(section in section_value for section in scalable_cmds):
            cmd = section_value[:2]
            section_parts = section_value[2:].split(',')
            for section_part in section_parts:
                if section_part.isnumeric():
                    rescaled_part = int(round(float(section_part) * scale_factor))
                    cmd = f'{cmd}{rescaled_part},'
                else:
                    cmd = f'{cmd}{section_part},'
            return cmd[:-1]
        else:
            return section_value
    
    def _scale_image(self, gf_command, fo_x, fo_y, scale_factor):
        """
        Scale Graphics of Label Per DPI.
        :param gf_cmd: ^GF command (string)
        :param fo_x: upper left x-axis location (in dots)
        :param fo_y: upper left y-axis location (in dots)
        :return: ~DG command (string)
        """
        _, binary_byte_count, graphic_field_count, bytes_per_row, data = tgc.break_gf_command(gf_command)
        data = tgc.clean(data)
        if tgc.check_for_z64_compression(data):
            data = tgc.decompress_z64(data)
        data_bits = tgc.chars_to_bits(data)
        bits_total = tgc.size_byte_to_bit(binary_byte_count if binary_byte_count > graphic_field_count else graphic_field_count)
        bits_per_row = tgc.size_byte_to_bit(bytes_per_row)
        image = tgc.bits_to_image(bits_total, bits_per_row, data_bits)
        width, height = image.size
        scaled_width = int(round(float(width) * scale_factor))
        scaled_height = int(round(float(height) * scale_factor))
        remainder = scaled_width % 8
        scaled_width = scaled_width - remainder
        scaled_height = scaled_height - remainder
        image = image.resize((scaled_width, scaled_height), tgc.Image.NEAREST)
        bits_total, bits_per_row, data_bits = tgc.image_to_bits(image)
        bytes_total = tgc.size_bit_to_byte(bits_total)
        bytes_per_row = tgc.size_bit_to_byte(bits_per_row)
        data = tgc.bits_to_chars(data_bits)
        dg_cmd = tgc.build_dg_command(bytes_total, bytes_per_row, data, '000')
        return tgc.write_zpl(dg_cmd, fo_x, fo_y)

    def _output(self, commands, encoding = 'CP437'):
        """
        Send Raw Commands to Zebra Printer.
        :param commands: ZPL command (string)
        :param encoding: 8-bit character encoding (string)
        """
        if self.queue is None :
            self.queue = win32print.GetDefaultPrinter()
        if type(commands) != bytes:
            commands = str(commands).encode(encoding = encoding)
        try:
            hPrinter = win32print.OpenPrinter(self.queue)
        except:
            hPrinter = win32print.OpenPrinter(win32print.GetDefaultPrinter())
        try:
            win32print.StartDocPrinter(hPrinter, 1, ('Label', None, 'RAW'))
            try:
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, commands)
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

    def print_label(self, commands, queue = None):
        """
        Print Label Using ZPL Commands.
        :param commands: ZPL command (string)
        :param queue: printer queue (string) (optional)
        """
        if queue is None:
            self.queue = win32print.GetDefaultPrinter()
        else:
            self.queue = queue
        printer_dpi = self.get_printer_dpi(self.queue)
        label_dpi = self.get_label_dpi(commands)
        if printer_dpi > 0 and label_dpi > 0 and label_dpi != printer_dpi:
            self._output(self._rescale(commands, printer_dpi, label_dpi))
        else:
            self._output(commands)

    def set_queue(self, queue):
        """
        Set Printer Queue.
        :param queue: printer queue (string)
        """
        self.queue = queue

    def get_queues(self):
        """
        Get Printer Queues.
        :return: printer queues (list)
        """
        printers = []
        for (_, _, name, _) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append(name)
        return printers
    
    def get_printer_dpi(self, queue = None):
        """
        Get Printer DPI.
        :param queue: printer queue (string) (optional)
        :return: printer DPI (int)
        """
        if queue is None:
            queue = win32print.GetDefaultPrinter()
        pattern = r'\d{3}dpi'
        for (_, desc, name, _) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            if name == queue:
                driver = desc.split(',')[1]
                if tgc.re.search(pattern, driver):
                    dpi = tgc.re.search(pattern, driver)
                    return int(dpi.group().lower().strip('dpi'))
        return 0

    def get_label_dpi(self, commands):
        """
        Get Label DPI.
        :param commands: ZPL command (string)
        :return: label DPI (int)
        """
        pattern = r'\^LL\d{3}'
        if tgc.re.search(pattern, commands):
            dpi = tgc.re.search(pattern, commands)
            return int(dpi.group().strip('^LL'))
        else:
            return 0

    def setup(self, label_height, label_width, direct_thermal = None):
        """
        Setup Printer Parameters Manually.
        :param label_height: tuple (label height, label gap) (in dots)
        :param label_width: label width (in dots)
        :param direct_thermal: True if using direct thermal labels (bool) (optional)
        """
        commands = '\n'
        if direct_thermal:
            commands += 'OD\n'
        commands += 'Q%s,%s\n' % (label_height[0], label_height[1])
        commands += 'q%s\n' % label_width
        self._output(commands)

    def autosense(self):
         """
         Autosense Label Parameters.
         """
         self._output('\nxa\n')

    def reset(self):
        """
        Reset Printer.
        """
        self._output('\n^@\n')

    def reset_default(self):
        """
        Reset Printer to Factory Default.
        """
        self._output('\n^default\n')

if __name__ == '__main__':
    """
    Testing Protocols.
    """
    test_commands = ("""N\n"""
                     """A40,80,0,4,1,1,N,"Trimble Inc."\n"""
                     """A40,198,0,3,1,1,N,"ARFC Label Printing"\n"""
                     """A40,240,0,3,1,1,N,"Created On: March 31, 2023"\n"""
                     """A40,320,0,4,1,1,N,"With Trimble, Work Works Now."\n"""
                     """P1\n""")
    z = Zebra()
    z.setup((406, 32), 812, True)
    z.print_label(test_commands)
    print('~ Printer Commands ~' + '\n' + test_commands)
    print('Printer Queues:', z.get_queues(), '\n')