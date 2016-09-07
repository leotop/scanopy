from Tkinter import *
import threading
import scanner
import time

class Gui(threading.Thread):
    def __init__(self, scanner):
        threading.Thread.__init__(self)
        self.root = Tk()
        self.root.geometry("550x500")
        self.root.title("Scanopy - Port Scanner")
        self.scanner = scanner
        self.initComponents()
        self.console_rows = 0
        self.max_console_rows = 20
        self.stop = False

    def run(self):
        self.root.mainloop()

    def output_console(self, new_text):
        self.consoleText.config(state=NORMAL)
        self.consoleText.insert(END, "\n" + new_text)
        self.consoleText.see(END)
        self.consoleText.config(state=DISABLED)

    def initComponents(self):
        root = self.root

        # Input Frame
        inputFrame = Frame(root, width="200")
        inputFrame.pack(pady=15, padx=15)

        # Init Components
        startLabel = Label(inputFrame, text="Start:")
        endLabel = Label(inputFrame, text="End:")
        self.rangeStartEntry = Entry(inputFrame)
        self.rangeStartEntry.insert(0, "173.194.40.241")
        self.rangeEndEntry = Entry(inputFrame)
        self.rangeEndEntry.insert(0, "173.194.40.249")
        portLabel = Label(inputFrame, text="Port:")
        self.portEntry = Entry(inputFrame)
        self.portEntry.insert(0, "80")
        hostButton = Button(inputFrame, text="Resolve host", command=self.output_host)
        stopButton = Button(inputFrame, text="Stop", command=self.stopScan)
        scanButton = Button(inputFrame, text="Scan", command=self.scan)

        # Set Component Grid Positions
        startLabel.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        endLabel.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.rangeStartEntry.grid(row=0, column=1, padx=5, pady=5)
        self.rangeEndEntry.grid(row=0, column=3, padx=5, pady=5)
        portLabel.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.portEntry.grid(row=1, column=3, padx=5, pady=5)
        hostButton.grid(row=1, column=1, padx=5, pady=5)
        scanButton.grid(row=0, column=4, padx=10, pady=5)
        stopButton.grid(row=1, column=4, padx=10, pady=5)

        # Console Frame
        self.consoleFrame = Frame(root)
        self.consoleFrame.pack(expand=1, pady=15, padx=15, fill= BOTH)
        self.consoleText = Text(self.consoleFrame, fg="green", bg="black",state=DISABLED)
        self.consoleText.pack(expand=1, fill= BOTH)

    def scan(self):
        self.stop = False
        start_ip = self.rangeStartEntry.get()
        end_ip = self.rangeEndEntry.get()
        ip_list = self.scanner.getIpAddressesFromRange(start_ip, end_ip)
        port = self.portEntry.get()
        self.ip_scan_index = 0
        # Kindof recursive function with call to root.after() to keep gui from freezing
        self.output_console("\nScanning ip range " + start_ip + " - " + end_ip+"...")
        def scanIp():
            result = self.scanner.scan(ip_list[self.ip_scan_index], port)
            self.output_console(result)
            self.ip_scan_index += 1
            if self.ip_scan_index < len(ip_list):
                if self.stop:
                    self.stop = False
                    return
                self.root.after(1400, scanIp)
        scanIp()
    
    def output_host(self):
        ip = self.rangeStartEntry.get()
        try:
            self.output_console("\nResolved hostname to: " + self.scanner.getHostByIp(ip))
        except:
            self.output_console("\nCould not resolve hostname for: "+ ip)
    
    def stopScan(self):
        self.stop = True
