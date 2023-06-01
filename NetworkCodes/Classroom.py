import PySimpleGUI as sg
from vidstream import StreamingServer
from vidstream import ScreenShareClient
import threading
import socket
import os
import time
import queue
import subprocess
from datetime import datetime


class start:
    def __init__(self):
        # Define the layout of the window
        background_image = "icon5.png"
        sg.theme("DarkAmber")
        layout = [
            [
                sg.Image("icon1.png", size=(800, 100), pad=(1, 1)),
            ],
            [sg.Text("Welcome to our Classroom!", font=("Arial", 16), pad=(200, 20))],
            [
                sg.Button(
                    " ",
                    image_filename="icon3.png",
                    pad=(200 / 1, 1 / 1),
                    image_size=(100, 100),
                    image_subsample=2,
                ),
                sg.Button(
                    "   ",
                    size=(10, 200),
                    pad=(0 / 1, 1 / 1),
                    image_filename="icon4.png",
                    image_size=(100, 100),
                    image_subsample=2,
                ),
            ],
            [
                sg.Text(
                    "Share Screen",
                    font=("Arial", 10),
                    pad=(200 / 1, 1 / 1),
                ),
                sg.Text(
                    "Share files",
                    font=("Arial", 10),
                ),
            ],
            [
                sg.Text(
                    "", size=(20, 1), font=("Arial", 16), key="time", pad=(250, 50)
                ),
            ],
        ]

        # Create the window
        self.window = sg.Window(
            "Classroom",
            layout,
            size=(800, 500),
        )

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
                subprocess.Popen(["python", "fileclient.py"])
                File1.server_program()
            self.window["time"].update(datetime.now().strftime("Time :%H:%M:%S"))

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

        self.window = sg.Window("Classroom App", layout, size=(300, 300))

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
    def server_program():
        # get the hostname
        host = socket.gethostname()
        port = 5003  # initiate port no above 1024

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

        window = sg.Window("File Sender", layout)

        while True:
            event, values = window.read()
            if event == "Send":
                filename = values["-FILE-"]
                if filename:
                    try:
                        filesize = os.path.getsize(filename)
                        conn.send(f"{os.path.basename(filename)} {filesize}".encode())
                        with open(filename, "rb") as f:
                            conn.sendfile(f)
                    #     window.write('File sent successfully!')
                    except FileNotFoundError:
                        window.write("File not found!")
                    except OSError:
                        window.write("Error sending file!")
                    break
            elif event in (None, "Cancel"):
                break

        window.close()

        conn.close()  # close the connection


if __name__ == "__main__":
    #  server_program().conn.close()  # close the connection
    app = start()
    app.run()
