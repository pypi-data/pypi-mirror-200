# Trimble Zebra Printing
Trimble Zebra Printing was built to simplify and standardize ZPL printing in the Trimble Facilities. This includes features, such as DPI scaling, to improve printing automation. Upscaling DPI results in a loss of quality. Matching DPIs or downscaling is recommended.

# class Zebra
Class To Communicate & Print With (Zebra) Label Printers.

## def print_label(commands, queue = None):
Print Label Using ZPL Commands.

:param commands: ZPL command (string)

:param queue: printer queue (string) (optional)

## def set_queue(queue):
Set Printer Queue.

:param queue: printer queue (string)

## def get_queues():
Get Printer Queues.

:return: printer queues (list)

## def get_printer_dpi(queue = None):
Get Printer DPI.

:param queue: printer queue (string) (optional)

:return: printer DPI (int)

## def get_label_dpi(commands):
Get Label DPI.

:param commands: ZPL command (string)

:return: label DPI (int)

## def setup(label_height, label_width, direct_thermal = None):
Setup Printer Parameters Manually.

:param label_height: tuple (label height, label gap) (in dots)

:param label_width: label width (in dots)

:param direct_thermal: True if using direct thermal labels (bool) (optional)

## def autosense():
Autosense Label Parameters.

## def reset():
Reset Printer.

## def reset_default():
Reset Printer to Factory Default.