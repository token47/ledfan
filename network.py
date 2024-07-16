#!/bin/false

import os
import re
import socket
import time

from select import select

FRAME = {
    "begin":  b"C0EEB7C9BAA3",
    "end":    b"C0EEBDF9E5B7",
    "upload": b"B2DDDDED",
    }

XMITCODE = {
    "start":  b"",                 # empty
    "onoff":  b"\x00\x63\x63\x61", # 00 63 63 61 .cca
    "next":   b"\x00\x63\x63\x63", # 00 63 63 63 .ccc
    "last":   b"\x00\x63\x63\x64", # 00 63 63 64 .ccd
    "pause":  b"\x00\x63\x63\x65", # 00 63 63 65 .cce # pause/play on video
    "play":   b"\x00\x63\x64\x42", # 00 63 64 42 .cdB # play a specific num
    "delete": b"\x00\x63\x64\x41", # 00 63 64 41 .cdA
    "sloop":  b"\x00\x63\x63\x67", # 00 63 63 67 .ccg
    "lloop":  b"\x00\x63\x63\x68", # 00 63 63 68 .cch
    "brigh-": b"\x00\x63\x63\x6c", # 00 63 63 6c .ccl
    "brigh+": b"\x00\x63\x63\x6d", # 00 63 63 6d .ccm
    "rotcw":  b"\x00\x63\x63\x70", # 00 63 63 70 .ccp
    "rotccw": b"\x00\x63\x63\x71", # 00 63 63 71 .ccq
    "upload": b"\x00\x6e\x63",     # 00 6e 63    .mc
    #"????":  b"\x00\x63\x67\x62\x93\xe3\x00\x00" # 00 63 67 62 93 e3 00 00 .cgb....
    }

RECVCODE = {
    "filelist":   b"\x00\x6d\x6e\x69",     # 00 6d 6e 69    .mni
    "filelist2":  b"\x00\x6d\x70\x69",     # 00 6d 70 69    .mpi
    "filelist3":  b"\x00\x6e\x66\x69",     # 00 6e 66 69    .nfi
    "filelist4":  b"\x00\x6e\x63\x69",     # 00 6e 63 69    .nci
    "uploadconf": b"\x00\x6b\x65",         # 00 6b 65       .ke
    }

FRAME_RE = re.compile(
    b'(('+FRAME["begin"]+b'|'+FRAME["upload"]+b')((?s:.)*?)'+FRAME["end"]+b')')


class LedFanNetwork:

    _sock = None
    _connected = False
    _recv_buffer = b''
    filelist = []
    filelist_extra = b""
    filepos = 0
    cb_filelist_changed = None


    #def __init__(self):
    #    pass

    def add_filelist_changed_callback(self, cb):
        self.cb_filelist_changed = cb


    def connect(self, host="192.168.4.1", port=20320):
        print(f"DEBUG: connect")
        if self._connected:
            return
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))
        self._sock.setblocking(0)
        self._connected = True


    def disconnect(self):
        print(f"DEBUG: disconnect")
        if not self._connected:
            return
        self._sock.close()
        self._connected = False


    def _sock_send(self, msg):
        print(f"DEBUG: _sock_send")
        self._sock.send(msg)


    def _sock_recv(self):
        if not self._connected:
            return
        #print("buffer 0 -> ", len(self._recv_buffer))
        while self._sock in select([self._sock], [], [], 0)[0]:
            received = self._sock.recv(16384)
            if not received:
                self.disconnect()
                return
            self._recv_buffer += received
            print(f"DEBUG: _sock_recv")
        #print("buffer 1 -> ", len(self._recv_buffer))


    def process_packets(self):
        self._sock_recv()
        while len(self._recv_buffer):
            matched_obj = FRAME_RE.match(self._recv_buffer)
            if not matched_obj:
                print(f"DEBUG: Buffer not matched, skipping: {self._recv_buffer}")
                break
            matched_len_total = len(matched_obj.group(1))
            matched_bytes_payload = matched_obj.group(3) 
            self._recv_buffer = self._recv_buffer[matched_len_total:]
            self.parse_codes(matched_bytes_payload)


    def parse_codes(self, pktbytes):
        if pktbytes.startswith(RECVCODE["filelist"]):
            print("RECV CODE: filelist")
            args = pktbytes[len(RECVCODE["filelist"]):]
            self.recv_filelist(args)
        elif pktbytes.startswith(RECVCODE["filelist2"]):
            print("RECV CODE: filelist2")
            args = pktbytes[len(RECVCODE["filelist2"]):]
            self.recv_filelist(args)
        elif pktbytes.startswith(RECVCODE["filelist3"]):
            print("RECV CODE: filelist3")
            args = pktbytes[len(RECVCODE["filelist3"]):]
            self.recv_filelist(args)
        elif pktbytes.startswith(RECVCODE["filelist4"]):
            print("RECV CODE: filelist4")
            args = pktbytes[len(RECVCODE["filelist4"]):]
            self.recv_filelist(args)
        elif pktbytes.startswith(RECVCODE["uploadconf"]):
            print("RECV CODE: uploadconf")
            args = pktbytes[len(RECVCODE["uploadconf"]):]
            self.recv_uploadconf(args)
        else:
            print(f"RECV CODE: unknown {pktbytes}")


    def recv_filelist(self, buffer):
        print(f"DEBUG: revc_filelist")
        self.filelist = []
        files = buffer[:-16]
        currpos = buffer[-16:-15]
        extra = buffer[-15:]
        for file in re.split(b"\x01|\x05|\x06|\x08", files)[1:]:
            self.filelist.append(file.decode())
        self.filepos = ord(currpos)
        self.filelist_extra = extra
        if self.cb_filelist_changed:
            self.cb_filelist_changed(self.filelist, self.filepos)


    def recv_uploadconf(self, buffer):
        print(f"DEBUG: Not implemented, got uploadconf + {buffer}")


    def send_cmd(self, cmd, arg=None):
        print(f"DEBUG: send_cmd, cmd:{cmd} arg:{arg}")
        frame = bytearray()
        frame.extend(FRAME["begin"])
        frame.extend(XMITCODE[cmd])
        frame.extend(arg.to_bytes(1, byteorder="little") if arg is not None else b"")
        frame.extend(FRAME["end"])
        self._sock_send(frame)


    def send_upload_file(self, filepath):
        print(f"DEBUG: send_upload_file")
        # device will stop and restart after upload
        filedata = open(filepath, "rb").read()
        filename = os.path.basename(filepath)
        self._sock_send(FRAME["upload"]+FRAME["end"])
        self._sock_send(FRAME["upload"]+XMITCODE["upload"]+filename.encode()+FRAME["end"])
        time.sleep(0.5)
        # a packet will come back, consume it just in case
        self.process_packets()
        # then send actual file data
        self._sock_send(filedata)
        # and finally send end sequence -- this seems a bug, not sending it
        #self._sock_send(FRAME["upload"]+FRAME["end"])

