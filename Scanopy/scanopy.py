from gui import *
from ip_scanner import *
#import threading

if __name__ == '__main__':
    scanner = IpScanner()
    gui_thread = Gui(scanner)
    gui_thread.start()