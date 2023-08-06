# Trimble Zebra Printing
Trimble Zebra Printing was built to simplify and standardize ZPL printing in the Trimble Facilities. This includes features, such as DPI scaling, to improve printing automation. Upscaling DPI results in a loss of quality. Matching DPIs or downscaling is recommended.

# class Zebra
Class To Communicate & Print With (Zebra) Label Printers.

## def print_label(self, commands, queue = None):
Print Label Using ZPL Commands.

:param commands: ZPL command (string)

:param queue: printer queue (string) (optional)

## def get_queues(self):
Get Printer Queues.

:return: printer queues (list)

## def get_printer_dpi(self, queue = None):
Get Printer DPI.

:param queue: printer queue (string) (optional)

:return: printer DPI (int)

## def get_label_dpi(self, commands):
Get Label DPI.

:param commands: ZPL command (string)

:return: label DPI (int)

## def setup(self,label_height, label_width, direct_thermal = None):
Setup Printer Parameters Manually.

:param label_height: tuple (label height, label gap) (in dots)

:param label_width: label width (in dots)

:param direct_thermal: True if using direct thermal labels (bool) (optional)

## def autosense(self):
Autosense Label Parameters.

## def reset(self):
Reset Printer.

## def reset_default(self):
Reset Printer to Factory Default.