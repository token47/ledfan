#!/usr/bin/python3

import appui as baseui
import tkinter as tk
import tkinter.ttk as ttk

from network import LedFanNetwork


class app(baseui.appUI):

    _network = LedFanNetwork()
    _curr_filelist = []
    _curr_filepos = None

    def __init__(self, master=None):
        super().__init__(master)
        # intercept window close
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.cb_root_exit)
        # configure treeview columns
        self.treeview['columns'] = ('filename', 'current', 'rest')
        self.treeview.column("#0", width=3, anchor='center')
        self.treeview.heading("#0", text=" ID", anchor='center')
        self.treeview.column("filename" , width=50)
        self.treeview.heading("filename", text="Filename")
        self.treeview.column("current" , width=6)
        self.treeview.heading("current", text="Playing")
        self._network.add_filelist_changed_callback(self.cb_filelist_changed)


    # use this instead of run() for non-blocking calls
    def update(self):
        self.mainwindow.update()


    def cb_button_lastone_clicked(self):
        self._network.send_cmd("last")


    def cb_button_singleloop_clicked(self):
        self._network.send_cmd("sloop")


    def cb_button_playpause_clicked(self):
        self._network.send_cmd("pause")


    def cb_button_listloop_clicked(self):
        self._network.send_cmd("lloop")


    def cb_button_nextone_clicked(self):
        self._network.send_cmd("next")

    def cb_button_disconnect_clicked(self):
        self._network.disconnect()
        self.treeview.delete(*self.treeview.get_children())
        self.label_connected.configure(
            text='disconnected')

    def cb_button_connect_clicked(self):
        self._network.connect()
        self._network.send_cmd("start")
        self.label_connected.configure(
            text='connected')

    def cb_button_onoff_clicked(self):
        self._network.send_cmd("onoff")

    def cb_button_format_clicked(self):
        # not implemented yet in network lib
        #self._network.send_cmd("format")
        pass

    def cb_button_upload_clicked(self):
        # a little more involving (will need a separate connection)
        #self._network.send_cmd("upload")
        pass

    def cb_button_brighplus_clicked(self):
        self._network.send_cmd("brigh+")

    def cb_button_brighminus_clicked(self):
        self._network.send_cmd("brigh-")

    def cb_button_cwadjust_clicked(self):
        self._network.send_cmd("rotcw")

    def cb_button_ccwadjust_clicked(self):
        self._network.send_cmd("rotccw")

    def cb_button_play_clicked(self):
        sel = self.treeview.selection()
        item = self.treeview.item(sel)
        pos = int(item["text"])
        self._network.send_cmd("play", pos)

    def cb_button_delete_clicked(self):
        sel = self.treeview.selection()
        item = self.treeview.item(sel)
        pos = int(item["text"])
        # disabled for now... (preventing mistakes)
        #self._network.send_cmd("delete", pos)
        pass

    def cb_button_quit_clicked(self):
        self.cb_root_exit()

    def cb_key_pressed(self, event=None):
        global exitflag
        if event.char == "q":
            exitflag = True

    def cb_root_exit(self):
        global exitflag
        self._network.disconnect()
        self.mainwindow.destroy()
        exitflag = True

    def cb_filelist_changed(self, filelist, filepos):
        if set(self._curr_filelist) == set(filelist):
            # list is the same as before, just update 'currently playing' status
            print(f"DEBUG: clearing filepos:{self._curr_filepos}")
            for child in self.treeview.get_children():
                if int(self.treeview.item(child)['text']) == self._curr_filepos:
                    self.treeview.set(child, 'current', '')
        else:
            # list is different, reset and reload complete list
            print("DEBUG: replacing whole treeview children")
            self.treeview.delete(*self.treeview.get_children())
            for i in range(len(filelist)):
                self.treeview.insert('', 'end', text=str(i), values=(filelist[i]))
        # set the currently playing status
        print(f"DEBUG: setting filepos:{filepos}")
        for child in self.treeview.get_children():
            if int(self.treeview.item(child)['text']) == filepos:
                self.treeview.set(child, 'current', '<--')
        self._curr_filepos = filepos
        self._curr_filelist = filelist


app = app()
exitflag = False

def main():
    while not exitflag:
        app.update()
        app._network.process_packets()


if __name__ == "__main__":
    main()
