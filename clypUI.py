import os
import subprocess
import threading
import time
import tkinter as tk
import tracemalloc
from datetime import datetime
from tkinter import filedialog
from tkinter import ttk

import pyperclip

import clipboardHistory
import client
import Server
import shareClyp
from pynput import keyboard

import fileSender, pubsub
folder_path =None
items = {}
closefunc=[]

def display_history():
    # Create a new window
    def copycontent():
        selected_item = tree.focus()  # Get the selected item
        content = clipboardHistory.history[selected_item]['content']
        pyperclip.copy(content)

    def display_full_text(textfield):
        textfield.configure(state=tk.NORMAL)
        selected_item = tree.focus()# Get the selected item
        content = clipboardHistory.history[selected_item]['content'] # Extract the "content" value
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
    history=clipboardHistory.history
    # Insert the data from the history dictionary
    def readItems():
        for time, data in history.items():
            cont=''
            if len(data["content"]) < 25:
                cont = data["content"]
            else:
                for s in range(len(data["content"])):
                    if data["content"][s] !="\n":
                        cont=data["content"][s:s+100]
                        cont=cont.replace("\n","-")
                        break
            if time not in tree.get_children():
                item = tree.insert("", "end",time, text=time,values=(data["type"], cont))

    readItems()
    # Adjust column widths
    tree.column("#0", width=100)
    tree.column("type", width=60)
    tree.column("content", width=400)
    fr = tk.Frame(window)
    text_field = tk.Text(window, height=4)
    but = tk.Button(fr, text="⟳",width=4, command=readItems)
    but.pack(anchor="center",expand=1)
    copycont = tk.Button(fr, text="⎘",width=4,command=copycontent)
    copycont.pack(anchor="center",expand=1)
    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=10)
    fr.grid(row=0,column=0,sticky='EW')
    tree.grid(row=0,column=1,sticky='ew')
    text_field.grid(row=1,column=0,columnspan=2,sticky='ew')
    tree.bind("<<TreeviewSelect>>", lambda ev: display_full_text(text_field))
    tree.tag_configure("multiline")

def interFace():
    window = tk.Tk()
    window.title("Function Launcher")

    # Create IP address label and input field
    entrygrid=tk.Frame(window)
    entrygrid.pack(expand=False)

    ip_label = tk.Label(entrygrid, text="IP address:")
    ip_label.grid(row=0,column=0,sticky='W')

    ip_entry = tk.Entry(entrygrid)
    ip_entry.insert(0, "D0:39:57:F1:E7:92")  # Default IP address
    ip_entry.grid(row=0,column=1)


    portlabel = tk.Label(entrygrid, text="port:")
    portlabel.grid(row=1,column=0,sticky='W')

    port_entry = tk.Entry(entrygrid)
    port_entry.insert(0, "1")  # Default IP address
    port_entry.grid(row=1,column=1)

    host_var = tk.BooleanVar()
    host_checkbox = tk.Checkbutton(entrygrid, variable=host_var)
    #host_checkbox.pack()
    host_label=tk.Label(entrygrid,text="Host:")
    host_label.grid(row=2,column=0,sticky='W')
    host_checkbox.grid(row=2,column=1,sticky='W')
    start_button = tk.Button(window, text="Start",
                             command=lambda: run(ip_entry.get(), host_var.get(), int(port_entry.get())))

    start_button.pack()


    name_var = tk.StringVar()
    name_var.set("not Connected")
    con_label = tk.Label(window, textvariable=name_var)
    con_label.config(text="")
    con_label.pack()

    emp = tk.Label(window)
    emp.pack()

    items['name_var'] = name_var
    window.protocol("WM_DELETE_WINDOW", lambda :on_closing(window))

    folder_path = tk.StringVar()
    folder_path.set(os.getcwd())
    pubsub.events["dir"] = [folder_path.get()]

    def filedialogHanler():
        dir = filedialog.askdirectory()
        folder_path.set(dir)
        pubsub.events["dir"]=[dir]

    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Add the Browse option
    file_menu.add_command(label="Browse", command=filedialogHanler)
    file_menu.add_command(label="See History", command=display_history)

    mapitems = tk.Frame(window)
    mapitems.columnconfigure((0, 1), weight=1)
    mapitems.pack(expand=False)
    lbl1 = tk.Entry(master=mapitems, textvariable=folder_path)
    open= tk.Button(mapitems,text="→", command=lambda :subprocess.Popen(r'explorer /select,"{}"'.format(folder_path.get())))

    lbl1.grid(row=0,column=0,columnspan=7)
    open.grid(row=0, column=7,sticky="we")


    copy_button = tk.Button(window, text="copy File from clipboard",
                            command=lambda :pubsub.invoke("copyfileclip"))

    copy_button.pack()
    not_var = tk.StringVar()
    not_var.set("")
    not_label = tk.Label(window, textvariable=not_var)
    not_label.pack()

    pubsub.setEvent('recieving', lambda: not_var.set("Recieving File"))
    pubsub.setEvent('recieved', lambda: not_var.set("File Recieved at " + datetime.now().strftime("%H:%M:%S")))
    pubsub.setEvent('sending', lambda: not_var.set("Sending File"))
    pubsub.setEvent('sended', lambda: not_var.set("sended at" + datetime.now().strftime("%H:%M:%S")))
    window.mainloop()




def on_closing(root):
    for f in closefunc:
        f()
    print("r")
    root.destroy()



def run(ip, host, port):
    s, fileServer = None, None
    tracemalloc.start()
    if host:
        s = Server.socketServer(ip, port, wait=True)
        fs= Server.socketServer(ip, port+2, wait=True)
        closefunc.append(s.stopServer)
        closefunc.append(fs.stopServer)
        textClient = Server.connect(ip, port)
        fileClient = Server.connect(ip, port+2)
        t = threading.Thread(target=lambda: connectionhandler(s, lambda :shareClyp.shareClyp(textClient)))
        t.start()
        t = threading.Thread(target=lambda: connectionhandler(fs, lambda :fileSender.filesender(fileClient)))
        t.start()
    else:
        while True:
            try:
                textClient1 = Server.connect(ip, port)
                fileClient = Server.connect(ip, port + 2)
                items['name_var'].set("Connected")
                break
            except:
                print("cant connect with the server")

        items['name_var'].set("Connected")
        sc=shareClyp.shareClyp(textClient1)
        fc=fileSender.filesender(fileClient)
        closefunc.append(textClient1.close)
        closefunc.append(fileClient.close)

def connectionhandler(s, initf):
    while True:
        if len(s.getClientConnection()) > 1:
            shclyp = initf()
            items['name_var'].set("Connected")
            break
        elif len(s.getClientConnection()) <= 1:
            items['name_var'].set("Connecting")
            time.sleep(0.5)

    # except:
    #   if s.getConnection()|(fileServer.getConnection()):
    #      s.getConnection().close()
    #     fileServer.getConnection().close()


if __name__ == "__main__":
    interFace()
