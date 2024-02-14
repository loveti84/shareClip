import os
import subprocess
import threading
import time
import tkinter as tk
import tracemalloc
from datetime import datetime
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import bluetooth
import pyperclip

import event
from event import Event
import clipboardHistory
import client
import Server
import shareClyp
from pynput import keyboard
import fileSender, pubsub
import var
folder_path = None
items = {}
closefunc = []


def display_devices():

    def searchDevices(tree):
        dev=bluetooth.discover_devices(lookup_names=True)
        for d in dev:
            tree.insert("", "end", text=d[1], values=(d[0]))

    # Create a new window
    window = tk.Toplevel()
    # Create a Treeview widget
    tree = ttk.Treeview(window)
    tree["columns"] = ("Name", "address")
    # Define the column headings
    tree.heading("#0", text="Time")
    tree.heading("type", text="Type")
    tree.heading("content", text="Content")


def display_history():
    # Create a new window
    def copycontent():
        selected_item = tree.focus()  # Get the selected item
        content = clipboardHistory.history[selected_item]['content']
        pyperclip.copy(content)

    def display_full_text(textfield):
        textfield.configure(state=tk.NORMAL)
        selected_item = tree.focus()  # Get the selected item
        content = clipboardHistory.history[selected_item]['content']  # Extract the "content" value
        textfield.delete("1.0", tk.END)
        textfield.insert(tk.END, content)

    window = tk.Toplevel()
    # Create a Treeview widget
    tree = ttk.Treeview(window)
    tree["columns"] = ("type", "content")
    # Define the column headings
    tree.heading("#0", text="Time")
    tree.heading("type", text="Type")
    tree.heading("content", text="Content")
    history = clipboardHistory.history

    # Insert the data from the history dictionary
    def readItems():
        for time, data in history.items():
            cont = ''
            if len(data["content"]) < 25:
                cont = data["content"]
            else:
                for s in range(len(data["content"])):
                    if data["content"][s] != "\n":
                        cont = data["content"][s:s + 100]
                        cont = cont.replace("\n", "-")
                        break
            if time not in tree.get_children():
                item = tree.insert("", "end", time, text=time, values=(data["type"], cont))

    readItems()
    # Adjust column widths
    tree.column("#0", width=100)
    tree.column("type", width=60)
    tree.column("content", width=400)
    fr = tk.Frame(window)
    text_field = tk.Text(window, height=4)
    but = tk.Button(fr, text="⟳", width=4, command=readItems)
    but.pack(anchor="center", expand=1)
    copycont = tk.Button(fr, text="⎘", width=4, command=copycontent)
    copycont.pack(anchor="center", expand=1)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=10)
    fr.grid(row=0, column=0, sticky='EW')
    tree.grid(row=0, column=1, sticky='ew')
    text_field.grid(row=1, column=0, columnspan=2, sticky='ew')
    tree.bind("<<TreeviewSelect>>", lambda ev: display_full_text(text_field))
    tree.tag_configure("multiline")



def interFace():
    window = tk.Tk()
    window.title("Function Launcher")

    # Create IP address label and input field
    entrygrid = tk.Frame(window)
    entrygrid.pack(expand=False)

    ip_label = tk.Label(entrygrid, text="IP address:")
    ip_label.grid(row=0, column=0, sticky='W')

    ip_entry = tk.Entry(entrygrid)
    # ip_entry.insert(0, '04:7F:0E:7D:D0:D9')  # Default IP address

    ip_entry.insert(0, "D0:39:57:F1:E7:92")  # Default IP address
    ip_entry.grid(row=0, column=1)
    portlabel = tk.Label(entrygrid, text="port:")
    portlabel.grid(row=1, column=0, sticky='W')
    port_entry = tk.Entry(entrygrid)
    port_entry.insert(0, "8")  # Default IP address
    port_entry.grid(row=1, column=1)

    host_var = tk.BooleanVar()
    host_checkbox = tk.Checkbutton(entrygrid, variable=host_var)
    # host_checkbox.pack()
    host_label = tk.Label(entrygrid, text="Host:")
    host_label.grid(row=2, column=0, sticky='W')
    host_checkbox.grid(row=2, column=1, sticky='W')

    log_var = tk.BooleanVar()
    host_checkbox = tk.Checkbutton(entrygrid, variable=log_var)
    # host_checkbox.pack()
    host_label = tk.Label(entrygrid, text="Log clipboard:")
    host_label.grid(row=3, column=0, sticky='W')
    host_checkbox.grid(row=3, column=1, sticky='W')


    start_button = tk.Button(window, text="Start",
                             command=lambda: run(ip_entry.get(), host_var.get(), int(port_entry.get()),log_var.get()))

    start_button.pack()

    name_var = tk.StringVar()
    name_var.set("not Connected")
    con_label = tk.Label(window, textvariable=name_var)
    con_label.config(text="")
    con_label.pack()

    emp = tk.Label(window)
    emp.pack()
    folder_path = tk.StringVar()
    folder_path.set(os.getcwd())
    var.PATH = folder_path.get()
    def filedialogHanler():
        dir = filedialog.askdirectory()
        folder_path.set(dir)
        var.PATH =dir

    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Add the Browse option
    file_menu.add_command(label="Browse", command=filedialogHanler)
    file_menu.add_command(label="See History", command=display_history)
    file_menu.add_command(label="Find Devices", command=lambda :show_treeview_window(window,ip_entry))


    mapitems = tk.Frame(window)
    mapitems.columnconfigure((0, 1), weight=1)
    mapitems.pack(expand=False)
    lbl1 = tk.Entry(master=mapitems, textvariable=folder_path)
    open = tk.Button(mapitems, text="→",
                     command=lambda: subprocess.Popen(r'explorer /select,"{}"'.format(folder_path.get())))

    lbl1.grid(row=0, column=0, columnspan=7)
    open.grid(row=0, column=7, sticky="we")

    copy_button = tk.Button(window, text="copy File from clipboard",
                            command=lambda: pubsub.publish(Event.COPYFILE))

    copy_button.pack()
    not_var = tk.StringVar()
    not_var.set("")
    not_label = tk.Label(window, textvariable=not_var)
    not_label.pack()

    pubsub.addListeners(Event.RECIEVING, lambda: not_var.set("Recieving File"))
    pubsub.addListeners(Event.RECIEVED, lambda: not_var.set("File Recieved at " + datetime.now().strftime("%H:%M:%S")))
    pubsub.addListeners(Event.SENDING, lambda: not_var.set("Sending File"))
    pubsub.addListeners(Event.SENDED, lambda: not_var.set("sended at" + datetime.now().strftime("%H:%M:%S")))
    pubsub.addListeners(Event.CONNECTED, lambda: name_var.set("connected"))
    pubsub.addListeners(Event.CONNECTING, lambda: name_var.set("Waiting for connection"))
    pubsub.addListeners(Event.NOTCONNECTED, lambda: name_var.set("Not connected"))
    pubsub.addListeners(Event.NOTIFICATION, lambda e: not_var.set(e))


    pubsub.addPublisher(Event.CLOSE)
    window.mainloop()
    pubsub.publish(Event.CLOSE,wait=True)


def show_treeview_window(root,varToSet):
    pubsub.publish(Event.NOTIFICATION,"Searching for device",wait=True)
    def wr():

        # Discover Bluetooth devices
        dev = bluetooth.discover_devices(lookup_names=True)
        treeview_window = tk.Toplevel(root)
        treeview_window.title("Treeview Window")
        def ondestroy():
            pubsub.publish(Event.NOTIFICATION, "")
            treeview_window.destroy()
        treeview_window.protocol("WM_DELETE_WINDOW",ondestroy)
        pubsub.publish(Event.NOTIFICATION,"Wait for selection",wait=True)
        # Create a Treeview widget
        treeview = ttk.Treeview(treeview_window, columns=("name",))
        treeview.heading("#0", text="Address")
        treeview.heading("name", text="Name")

        for address, name in dev:
            treeview.insert("", tk.END, text=address, values=(name,))

        treeview.pack(expand=True, fill=tk.BOTH)
        def select_item(var):
            selected_item = treeview.focus()  # Get the selected item
            if selected_item:
                selected_address = treeview.item(selected_item, "text")  # Get the text of the selected item
                var.insert(0,selected_address)  # Set the selected address to the variable
                var.delete(0, tk.END)
                var.insert(0, selected_address)
                treeview_window.destroy()  # Close the window

        select_button = tk.Button(treeview_window, text="Select", command=lambda: select_item(varToSet))
        select_button.pack()

    t=threading.Thread(target=wr)
    t.start()


def on_closing():
    for f in closefunc:
        f()


def run(ip, host, port,log):
    clipboardHistory.log=log
    s, conn = None, None
    tracemalloc.start()
    ConnectionClient = client.client()

    def wr():
        gett = lambda: datetime.now().strftime("%H:%M:%S")
        noConnection = True
        conn=None
        while noConnection:
            if host:
                pubsub.publish(event.Event.CONNECTING)

                conn = Server.serverConnectHandler(ip,port)
            else:
                conn = Server.clientConnectHandler(ip,port)
            try:
                conn.send(f"{'Host' if host else 'client'} has successfully connected to {host}:{port}")
                if conn is not None:
                    noConnection = False
                    print(f'{gett()} succ connection.')
            except Exception as e:
                print(f'{gett()} somting whent wrong', e)

        pubsub.publish(event.Event.CONNECTED)
        ConnectionClient.setConnection(conn)
        sc = shareClyp.shareClyp(ConnectionClient)
        pubsub.addListeners(event.Event.CLOSE,ConnectionClient.connection.close)

    t = threading.Thread(target=wr)
    t.start()


if __name__ == "__main__":
    interFace()

