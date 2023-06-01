import PySimpleGUI as sg
from vidstream import StreamingServer
from vidstream import ScreenShareClient
import threading
import socket
import os
import time
import queue


class start:
    def __init__(self):
        # Define the layout of the window
        layout = [
            [
                sg.Image("icon1.png", size=(500, 100), pad=(1, 1)),
            ],
            [sg.Text("Welcome to our Classroom!", font=("Arial", 16), pad=(100, 20))],
            [
                sg.Button(
                    " ",
                    image_filename="icon3.png",
                    pad=(100 / 1, 1 / 1),
                    image_size=(70, 70),
                    image_subsample=2,
                ),
                sg.Button(
                    "   ",
                    size=(10, 200),
                    pad=(0 / 1, 1 / 1),
                    image_filename="icon4.png",
                    image_size=(70, 70),
                    image_subsample=2,
                ),
            ],
            [
                sg.Text(
                    "Share Screen",
                    font=("Arial", 10),
                    pad=(100 / 1, 1 / 1),
                ),
                sg.Text(
                    "Share files",
                    font=("Arial", 10),
                ),
            ],
        ]

        # Create the window
        self.window = sg.Window("Classroom", layout)

    def run(self):
        q = queue.Queue()

        # Display and interact with the window
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break
            # Handle button clicks
            if event == " ":
                self.window.hide()
                classroom = ClassroomApp()
                classroom.run()

            elif event == "   ":
                file3 = File1(q)
                file4 = File2(q)
                threading.Thread(target=file3.server_program).start()
                threading.Thread(target=file4.client_program).start()

            try:
                data = q.get_nowait()
                # Process data from queue here
                # Update GUI as needed
            except queue.Empty:
                pass

        self.window.close()


class ClassroomApp:
    def __init__(self):
        layout = [
            [sg.Text("Teacher")],
            [sg.Button("I am a teacher")],
            [sg.Text("Student")],
            [sg.Button("I am a student")],
            [sg.Button("Back")],
        ]

        self.window = sg.Window("Classroom App", layout, size=(200, 200))

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event in (sg.WIN_CLOSED, "Back"):
                self.window.hide()
                classroom = start()
                classroom.run()
            elif event == "I am a teacher":
                self.window.hide()
                gui2 = Gui2()
                gui2.run()
                self.window.un_hide()
            elif event == "I am a student":
                self.window.hide()
                gui3 = Gui3()
                gui3.run()
                self.window.un_hide()

        self.window.close()


## GUi el streaming
class Gui2:
    def __init__(self):
        layout = [
            [sg.Text("Teacher")],
            [sg.Text("IP Addresses")],
            [sg.Multiline(key="teacher_ips", size=(40, 5))],
            [sg.Button("Start Viewing")],
            [sg.Button("Start Sharing")],
            [sg.Button("Stop")],
            [sg.Button("Quit")],
        ]

        self.window = sg.Window("Classroom App", layout)
        self.receivers = []
        self.senders = []

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "Quit"):
                break
            elif event == "Start Viewing":
                teacher_ips = values["teacher_ips"].split()
                for teacher_ip in teacher_ips:
                    print(f"Connecting to {teacher_ip}")
                    receiver = StreamingServer(teacher_ip, 9000)
                    self.receivers.append(receiver)

                    t = threading.Thread(target=receiver.start_server)
                    t.start()
            elif event == "Start Sharing":
                teacher_ips = values["teacher_ips"].split()
                for teacher_ip in teacher_ips:
                    print(f"Connecting to {teacher_ip}")

                    sender = ScreenShareClient(teacher_ip, 9000)
                    self.senders.append(sender)
                    t = threading.Thread(target=sender.start_stream)
                    t.start()
            elif event == "Stop":
                for receiver in self.receivers:
                    receiver.stop_server()
                for sender in self.senders:
                    sender.stop_stream()

        self.window.close()


class Gui3:
    def __init__(self):
        layout = [
            [sg.Text("Student")],
            [sg.Text("IP Addresses")],
            [sg.Multiline(key="student_ips", size=(40, 5))],
            [sg.Button("Start Viewing")],
            [sg.Button("Start Sharing")],
            [sg.Button("Stop")],
            [sg.Button("Quit")],
        ]

        self.window = sg.Window("Classroom App", layout)
        self.receivers = []
        self.senders = []

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "Quit"):
                break
            elif event == "Start Viewing":
                student_ips = values["student_ips"].split()
                for student_ip in student_ips:
                    print(f"Connecting to {student_ip}")
                    receiver = StreamingServer(student_ip, 9000)
                    self.receivers.append(receiver)

                    t = threading.Thread(target=receiver.start_server)
                    t.start()
            elif event == "Start Sharing":
                student_ips = values["student_ips"].split()
                for student_ip in student_ips:
                    print(f"Connecting to {student_ip}")

                    sender = ScreenShareClient(student_ip, 9000)
                    self.senders.append(sender)
                    t = threading.Thread(target=sender.start_stream)
                    t.start()
            elif event == "Stop":
                for receiver in self.receivers:
                    receiver.stop_server()
                for sender in self.senders:
                    sender.stop_stream()

        self.window.close()


## gui el files


class File1:
    def __init__(self, q):
        self.q = q

    def server_program(self):
        # get the hostname
        host = socket.gethostname()
        port = 5003  # initiate port no above 1024
        self.q.put("Data from server_program")

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(3)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        # create GUI to select file to send
        layout = [
            [sg.Text("Select file to send")],
            [sg.Input(key="-FILE-"), sg.FileBrowse()],
            [sg.Button("Send"), sg.Button("Cancel")],
        ]

        self.window = sg.Window("File Sender", layout)

        while True:
            event, values = self.window.read()
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

        self.window.close()

        conn.close()  # close the connection


class File2:
    def __init__(self, q):
        self.q = q

    def client_program(self):
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
    app = start()
    app.run()
