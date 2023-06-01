import socket
import os.path
import PySimpleGUI as sg


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5003  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # receive file from server
    data = client_socket.recv(1024).decode()
    filename, filesize = data.split()
    filesize = int(filesize)

    # specify the directory where the file should be saved
    save_dir = "D:\\networks project\\Classroom\\NetworkCodes\\client files"

    with open(os.path.join(save_dir, filename), "wb") as f:
        while filesize > 0:
            data = client_socket.recv(1024)
            f.write(data)
            filesize -= len(data)

    client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
