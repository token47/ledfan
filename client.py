#!/usr/bin/python3

# test CLI client

import ledfannetwork

x = ledfannetwork.LedFanNetwork()

x.connect()

x.send_start()

while True:
    print("-------- main loop --------")
    x.process_packets()
    for i in range(len(x.filelist)):
        print(x.filelist[i], end="")
        print(" <--" if i == x.filepos else "")
    #print(x.filelist_extra)
    #time.sleep (3)
