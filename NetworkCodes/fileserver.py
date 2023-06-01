import socket
import os
import PySimpleGUI as sg


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5003  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    # create GUI to select file to send
    layout = [
        [sg.Text("Select file to send")],
        [sg.Input(key="-FILE-"), sg.FileBrowse()],
        [sg.Button("Send"), sg.Button("Cancel")],
    ]

    window = sg.Window("File Sender", layout)

    while True:
        event, values = window.read()
        if event == "Send":
            filename = values["-FILE-"]
            if filename:
                filesize = os.path.getsize(filename)
                conn.send(f"{os.path.basename(filename)} {filesize}".encode())
                with open(filename, "rb") as f:
                    conn.sendfile(f)
                break
        elif event in (None, "Cancel"):
            break

    window.close()

    conn.close()  # close the connection


if __name__ == "__main__":
    server_program()
