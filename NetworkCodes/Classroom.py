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


########################################### THE START GUI ###################################################################
## initialization func that start everything in the ui
# each button has an event
################################################events ###########################################################
# in the run func  we have two buttons with two events one for the streaming classes and another for the file sharing class
# in the first event we call the events of the streaming (classroomapp)class
# in the second event we call the file1 class (which is the server starting ) and using the subprocess we start the client class
# seperated in the fileclient.py code
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
                sg.Button(
                    "    ",
                    size=(10, 200),
                    pad=(0 / 1, 1 / 1),
                    image_filename="icon5.png",
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
                sg.Text(
                    "receive files",
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
                File1.server_program()
            elif event == "    ":
                File2.client_program()
            self.window["time"].update(datetime.now().strftime("Time :%H:%M:%S"))

        self.window.close()


################################################streaming ###############################################################
## we have 3 classes for the streamingclassroomapp and gui2 and gui3
# in classroom app we have gui with two buttons  one for the teacher and one for the stuent
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
## this is the gui for the teacher we enter the ip we want to share to or veiw sharing from
# and then we press even the start sharing or viewing to call their event
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


## this is the gui for the student we enter the ip we want to share to or veiw sharing from
# and then we press even the start sharing or viewing to call their event
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


#################################################### gui el files #######################################################3
# in this class we we start the server with socket and hot and the port the client should connect to
# then the server listens to the clients that calling for that port
# and then starts the gui for sending the files


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
                        conn, address = server_socket.accept()  # accept new connection
                        print("Connection from: " + str(address))
                        filesize = os.path.getsize(filename)
                        conn.send(f"{os.path.basename(filename)} {filesize}".encode())
                        with open(filename, "rb") as f:
                            while True:
                                data = f.read(1024)
                                if not data:
                                    break
                                conn.sendall(data)
                        conn.close()  # close the connection
                        print("File sent successfully!")
                    except FileNotFoundError:
                        window.write("File not found!")
                    except OSError:
                        window.write("Error sending file!")
            elif event in (None, "Cancel"):
                break

        window.close()


class File2:
    def client_program():
        # create GUI to enter server IP address
        layout = [
            [sg.Text("Enter server IP address")],
            [sg.Input(key="-IP-")],
            [sg.Button("Connect"), sg.Button("Cancel")],
        ]

        window = sg.Window("File Receiver", layout)

        while True:
            event, values = window.read()
            if event == "Connect":
                host = values["-IP-"]
                if host:
                    break
            elif event in (None, "Cancel"):
                return

        window.close()

        port = 5003  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        # receive file from server
        data = client_socket.recv(1024).decode()
        filename, filesize = data.split()
        filesize = int(filesize)

        # specify the directory where the file should be saved
        save_dir = "D:\\testing"

        try:
            with open(os.path.join(save_dir, filename), "wb") as f:
                while filesize > 0:
                    data = client_socket.recv(1024)
                    f.write(data)
                    filesize -= len(data)
            client_socket.close()  # close the connection
            print("File received successfully!")
        except FileNotFoundError:
            print("File not found!")
        except OSError:
            print("Error saving file!")


if __name__ == "__main__":
    #  server_program().conn.close()  # close the connection
    app = start()
    app.run()
