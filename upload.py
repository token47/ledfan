#!/usr/bin/python3

import network

x = network.LedFanNetwork()

x.connect()
x.send_upload_file("./y.BIN")
