from tkinter import *
from vidstream import StreamingServer
from vidstream import ScreenShareClient
import threading


class ClassroomApp:
    
    def __init__(self, master):
        self.master = master
        master.title("GUI 2")

        # create widgets for GUI 2
        self.label2 = Label(master, text="Teacher")
        self.button2 = Button(master, text="Click me in GUI 2", command=self.button2_click)
        self.label3 = Label(master, text="student")
        self.button3 = Button(master, text="Click me in GUI 2", command=self.button3_click)

        self.label2.grid(row=1, column=0)
        self.label3.grid(row=2, column=0)
        self.button2.grid(row=1, column=2)
        self.button3.grid(row=2, column=2)
        # layout widgets for GUI 2
       

    def button2_click(self):
        gui2 = Gui2(Toplevel(root))
    def button3_click(self):
        gui2 = Gui3(Toplevel(root))
class Gui2:
    def __init__(self, master):
        self.master = master
        master.title("Classroom App")

        # create labels
        self.teacher_label = Label(master, text="Teacher")
        self.student_label = Label(master, text="Student")

        # create entry boxes
        self.teacher_entry = Entry(master)
        self.student_entry = Entry(master)

        # create buttons
        self.connect_button = Button(
            master, text="Start Vewing ", command=self.connect1
        )
        self.connect2_button = Button(
            master, text="Start Sharing ", command=self.connect2
        )
        self.quit_button = Button(master, text="Quit", command=master.quit)

        # layout widgets
        self.teacher_label.grid(row=0, column=0)
        self.teacher_entry.grid(row=0, column=1)
        self.student_label.grid(row=1, column=0)
        self.student_entry.grid(row=1, column=1)
        self.connect_button.grid(row=2, column=0)
        self.connect2_button.grid(row=2 , column=3)
        self.quit_button.grid(row=2, column=1)

    def connect1(self):
        teacher_ip = self.teacher_entry.get()
        student_ip = self.student_entry.get()
        print(f"Connecting {student_ip} to {teacher_ip}")
        receiver = StreamingServer(teacher_ip,9000)

        t= threading.Thread(target=receiver.start_server)

        t.start()

        while input("") !='STOP':
            continue
        receiver.stop_server()
        
       
                


    def connect2(self):
            teacher_ip = self.teacher_entry.get()
            student_ip = self.student_entry.get()
            print(f"Connecting {student_ip} to {teacher_ip}")

            
            sender = ScreenShareClient(student_ip,9000)
            t= threading.Thread(target=sender.start_stream)

            t.start()

            while input("") !='STOP':
                continue
            sender.stop_stream()

class Gui3:
    def __init__(self, master):
        self.master = master
        master.title("Classroom App")

        # create labels
        self.teacher_label = Label(master, text="Teacher")
        self.student_label = Label(master, text="Student")

        # create entry boxes
        self.teacher_entry = Entry(master)
        self.student_entry = Entry(master)

        # create buttons
        self.connect_button = Button(
            master, text="Start Vewing ", command=self.connect1
        )
        self.connect2_button = Button(
            master, text="Start Sharing ", command=self.connect2
        )
        self.quit_button = Button(master, text="Quit", command=master.quit)

        # layout widgets
        self.teacher_label.grid(row=0, column=0)
        self.teacher_entry.grid(row=0, column=1)
        self.student_label.grid(row=1, column=0)
        self.student_entry.grid(row=1, column=1)
        self.connect_button.grid(row=2, column=0)
        self.connect2_button.grid(row=2 , column=3)
        self.quit_button.grid(row=2, column=1)

    def connect1(self):
        teacher_ip = self.teacher_entry.get()
        student_ip = self.student_entry.get()
        print(f"Connecting {student_ip} to {teacher_ip}")
        receiver = StreamingServer(teacher_ip,9000)

        t= threading.Thread(target=receiver.start_server)

        t.start()

        while input("") !='STOP':
            continue
        receiver.stop_server()
        
       
                


    def connect2(self):
            teacher_ip = self.teacher_entry.get()
            student_ip = self.student_entry.get()
            print(f"Connecting {student_ip} to {teacher_ip}")

            
            sender = ScreenShareClient(student_ip,9000)
            t= threading.Thread(target=sender.start_stream)

            t.start()

            while input("") !='STOP':
                continue
            sender.stop_stream()

           

                
root = Tk()
gui1 = ClassroomApp(root)


#my_classroom = ClassroomApp(root)
root.mainloop()
