#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class appUI:
    def __init__(self, master=None):
        # build ui
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.img_app = tk.PhotoImage(file="./app.png")
        self.toplevel.configure(height=200, width=200)
        self.toplevel.iconphoto(True, self.img_app)
        self.toplevel.resizable(False, False)
        self.toplevel.title("Led Fan Controller App")
        self.frame_main = ttk.Frame(self.toplevel, name="frame_main")
        self.frame_main.configure(
            borderwidth=1, height=200, padding=5, width=200)
        label1 = ttk.Label(self.frame_main)
        label1.configure(font="{Ubuntu} 12 {bold}",
                         text='Led-Fan Hologram Control App For Linux')
        label1.pack(pady="0 5", side="top")
        self.frame_main_sub = ttk.Frame(self.frame_main, name="frame_main_sub")
        self.frame_main_sub.configure(borderwidth=1, height=200, width=200)
        self.frame_left = ttk.Frame(self.frame_main_sub, name="frame_left")
        self.frame_left.configure(borderwidth=1, height=200, width=200)
        self.frame_buttons_top = ttk.Frame(
            self.frame_left, name="frame_buttons_top")
        self.frame_buttons_top.configure(height=200, width=200)
        self.button_lastone = ttk.Button(
            self.frame_buttons_top, name="button_lastone")
        self.button_lastone.configure(
            cursor="arrow",
            state="normal",
            takefocus=False,
            text='Last one',
            width=10)
        self.button_lastone.pack(padx="0 3", side="left")
        self.button_lastone.configure(command=self.cb_button_lastone_clicked)
        self.button_singleloop = ttk.Button(
            self.frame_buttons_top, name="button_singleloop")
        self.button_singleloop.configure(text='Single loop', width=10)
        self.button_singleloop.pack(padx=3, side="left")
        self.button_singleloop.configure(
            command=self.cb_button_singleloop_clicked)
        self.button_playpause = ttk.Button(
            self.frame_buttons_top, name="button_playpause")
        self.button_playpause.configure(text='Play/Pause', width=10)
        self.button_playpause.pack(padx=3, side="left")
        self.button_playpause.configure(
            command=self.cb_button_playpause_clicked)
        self.button_listloop = ttk.Button(
            self.frame_buttons_top, name="button_listloop")
        self.button_listloop.configure(text='List loop', width=10)
        self.button_listloop.pack(padx=3, side="left")
        self.button_listloop.configure(command=self.cb_button_listloop_clicked)
        self.button_nextone = ttk.Button(
            self.frame_buttons_top, name="button_nextone")
        self.button_nextone.configure(text='Next one', width=10)
        self.button_nextone.pack(padx="3 0", side="left")
        self.button_nextone.configure(command=self.cb_button_nextone_clicked)
        self.frame_buttons_top.pack(pady="0 10", side="top")
        self.treeview = ttk.Treeview(self.frame_left, name="treeview")
        self.treeview.configure(height=25, selectmode="extended")
        self.treeview.pack(expand=False, fill="both", side="top")
        self.frame_left.pack(fill="both", side="left")
        self.frame_buttons_right = ttk.Frame(
            self.frame_main_sub, name="frame_buttons_right")
        self.label_connected = ttk.Label(
            self.frame_buttons_right, name="label_connected")
        self.label_connected.configure(
            anchor="center",
            background="#333333",
            font="{Ubuntu Mono} 12 {}",
            foreground="#ffffff",
            padding=0,
            text='disconnected',
            width=13)
        self.label_connected.pack(ipadx=2, ipady=5, pady="0 10", side="top")
        self.button_disconnect = ttk.Button(
            self.frame_buttons_right, name="button_disconnect")
        self.button_disconnect.configure(text='Disconnect', width=12)
        self.button_disconnect.pack(pady="0 3", side="top")
        self.button_disconnect.configure(
            command=self.cb_button_disconnect_clicked)
        self.button_connect = ttk.Button(
            self.frame_buttons_right, name="button_connect")
        self.button_connect.configure(text='Connect', width=12)
        self.button_connect.pack(pady=3, side="top")
        self.button_connect.configure(command=self.cb_button_connect_clicked)
        self.button_onoff = ttk.Button(
            self.frame_buttons_right, name="button_onoff")
        self.button_onoff.configure(text='On/Off', width=12)
        self.button_onoff.pack(pady=3, side="top")
        self.button_onoff.configure(command=self.cb_button_onoff_clicked)
        self.button_format = ttk.Button(
            self.frame_buttons_right, name="button_format")
        self.button_format.configure(text='Format Disk', width=12)
        self.button_format.pack(pady=3, side="top")
        self.button_format.configure(command=self.cb_button_format_clicked)
        self.button_upload = ttk.Button(
            self.frame_buttons_right, name="button_upload")
        self.button_upload.configure(text='Upload file(s)', width=12)
        self.button_upload.pack(pady=3, side="top")
        self.button_upload.configure(command=self.cb_button_upload_clicked)
        self.button_brighplus = ttk.Button(
            self.frame_buttons_right, name="button_brighplus")
        self.button_brighplus.configure(
            default="normal", text='Brightness+', width=12)
        self.button_brighplus.pack(pady=3, side="top")
        self.button_brighplus.configure(
            command=self.cb_button_brighplus_clicked)
        self.button_brighminus = ttk.Button(
            self.frame_buttons_right, name="button_brighminus")
        self.button_brighminus.configure(text='Brightness-', width=12)
        self.button_brighminus.pack(pady=3, side="top")
        self.button_brighminus.configure(
            command=self.cb_button_brighminus_clicked)
        self.button_cwadjust = ttk.Button(
            self.frame_buttons_right, name="button_cwadjust")
        self.button_cwadjust.configure(text='CW adjust', width=12)
        self.button_cwadjust.pack(pady=3, side="top")
        self.button_cwadjust.configure(command=self.cb_button_cwadjust_clicked)
        self.button_ccwadjust = ttk.Button(
            self.frame_buttons_right, name="button_ccwadjust")
        self.button_ccwadjust.configure(text='CCW adjust', width=12)
        self.button_ccwadjust.pack(pady="3 0", side="top")
        self.button_ccwadjust.configure(
            command=self.cb_button_ccwadjust_clicked)
        self.button_play = ttk.Button(
            self.frame_buttons_right, name="button_play")
        self.button_play.configure(text='Play', width=12)
        self.button_play.pack(pady="25 0", side="top")
        self.button_play.configure(command=self.cb_button_play_clicked)
        self.button_delete = ttk.Button(
            self.frame_buttons_right, name="button_delete")
        self.button_delete.configure(text='Delete', width=12)
        self.button_delete.pack(pady="20 0", side="top")
        self.button_delete.configure(command=self.cb_button_delete_clicked)
        self.button_quit = ttk.Button(
            self.frame_buttons_right, name="button_quit")
        self.button_quit.configure(text='Quit', width=12)
        self.button_quit.pack(pady="90 0", side="top")
        self.button_quit.configure(command=self.cb_button_quit_clicked)
        self.frame_buttons_right.pack(padx="10 0", side="top")
        self.frame_main_sub.pack(side="top")
        self.frame_main.pack(side="top")
        self.toplevel.bind("<KeyPress>", self.cb_key_pressed, add="")

        # Main widget
        self.mainwindow = self.toplevel

    def run(self):
        self.mainwindow.mainloop()

    def cb_button_lastone_clicked(self):
        pass

    def cb_button_singleloop_clicked(self):
        pass

    def cb_button_playpause_clicked(self):
        pass

    def cb_button_listloop_clicked(self):
        pass

    def cb_button_nextone_clicked(self):
        pass

    def cb_button_disconnect_clicked(self):
        pass

    def cb_button_connect_clicked(self):
        pass

    def cb_button_onoff_clicked(self):
        pass

    def cb_button_format_clicked(self):
        pass

    def cb_button_upload_clicked(self):
        pass

    def cb_button_brighplus_clicked(self):
        pass

    def cb_button_brighminus_clicked(self):
        pass

    def cb_button_cwadjust_clicked(self):
        pass

    def cb_button_ccwadjust_clicked(self):
        pass

    def cb_button_play_clicked(self):
        pass

    def cb_button_delete_clicked(self):
        pass

    def cb_button_quit_clicked(self):
        pass

    def cb_key_pressed(self, event=None):
        pass


if __name__ == "__main__":
    app = appUI()
    app.run()
